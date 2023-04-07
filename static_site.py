#!/usr/bin/python3

import os;
import shlex;
import shutil;
import subprocess;
import sys;


RCS_URL = f'https://ftp.gnu.org/gnu/rcs/rcs-5.10.1.tar.lz'

mydir = os.path.dirname(__file__)


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


def main():
    prep_rcs()


if __name__ == '__main__':
    main()
