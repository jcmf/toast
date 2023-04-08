#!/usr/bin/python3

import functools;
import mimetypes;
import os;
import re;
import shlex;
import shutil;
import subprocess;
import sys;


RCS_URL = f'https://ftp.gnu.org/gnu/rcs/rcs-5.10.1.tar.lz'

URLS = ['/toast/']

mydir = os.path.dirname(__file__)
outdir = os.path.join(mydir, 'site_root')


def prep_rcs():
    if shutil.which('co'):
        return

    rcsdir = os.path.abspath(os.path.join(mydir, 'rcs'))
    bindir = os.path.join(rcsdir, 'bin')
    if not shutil.which('co', path=bindir):
        if os.path.exists(rcsdir):
            shutil.rmtree(rcsdir)
        os.mkdir(rcsdir)
        subprocess.run(
            f'curl {shlex.quote(RCS_URL)} | tar x',
            shell=True,
            check=True,
            cwd=rcsdir,
        )
        [srcdir] = (entry.path for entry in os.scandir(rcsdir))
        subprocess.run(['./configure', '--prefix=/'], check=True, cwd=srcdir)
        subprocess.run(['make', '-C', srcdir], check=True)
        subprocess.run(
            ['make', '-C', srcdir, 'install', f'DESTDIR={rcsdir}'],
            check=True,
        )
        shutil.rmtree(srcdir)

    os.environ['PATH'] = f'{os.environ["PATH"]}:{bindir}'
    assert shutil.which('co')


def get_script():
    proc = subprocess.run(
        ['co', '-q', '-p', os.path.join(mydir, 'www')],
        check=True,
        stdout=subprocess.PIPE,
    )
    return proc.stdout.replace(b'/home/zaphod/toast/', f'{os.path.abspath(mydir)}/'.encode('utf8'))


class Page:
    def __init__(self, url, response):
        self.url = url
        self.response = response

    @functools.cached_property
    def header_len(self):
        result = self.response.find(b'\n\n')
        assert result >= 0, self.response
        return result

    @property
    def body(self):
        return self.response[self.header_len+2:]

    @functools.cached_property
    def header_dict(self):
        header = self.response[:self.header_len]
        result = {}
        for line in header.decode('utf8').splitlines():
            k, v = line.split(':', 1)
            result[k.strip().lower()] = v.strip()
        return result

    @property
    def out_path(self):
        mime_type = self.header_dict.get('content-type')
        suffix = mimetypes.guess_extension(mime_type) or '' if mime_type else ''
        if self.url.endswith(suffix):
            suffix = ''
        assert self.url.startswith('/'), url
        index = 'index' if self.url.endswith('/') else ''
        return f'{outdir}{self.url}{index}{suffix}'

    @property
    def links(self):
        return ()  # XXX TODO implement


class Fetcher:
    def __init__(self, script=None):
        self.script = get_script() if script is None else script

    def fetch_page(self, url):
        m = re.fullmatch(r'(/toast)(/.*)', url)
        assert m, url
        env = {
            'SCRIPT_NAME': m.group(1),
            'PATH_INFO': m.group(2),
            'SERVER_NAME': 'XXX',
            **os.environ,
        }
        proc = subprocess.run(
            ['perl'],
            check=True,
            input=self.script,
            stdout=subprocess.PIPE,
            cwd=mydir,
            env=env,
        )
        return Page(url=url, response=proc.stdout)

    def emit_html(self, urls=URLS):
        seen = set(urls)
        pending = list(reversed(urls))
        while pending:
            url = pending.pop()
            page = self.fetch_page(url)
            os.makedirs(os.path.dirname(page.out_path), exist_ok=True)
            with open(page.out_path, 'wb') as f:
                f.write(page.body)
            for u in page.links:
                if u in seen:
                    continue
                seen.add(u)
                pending.append(u)


def main():
    prep_rcs()
    Fetcher().emit_html()


if __name__ == '__main__':
    main()
