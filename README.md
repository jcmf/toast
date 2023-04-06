# toast
packageless package manager for Unix systems and non-root users

## What is going on here?

I first published toast in 2003, though it is somewhat older than
that. With any luck, you can still find it in its original location
at [toastball.net/toast](http://toastball.net/toast/). If you are
new to toast, that page might be a good place to start. Or perhaps
you might try reading [this blog article about
toast](https://jf64.wordpress.com/2009/10/04/a-brief-history-of-toastball/)
that a much younger me wrote a long time ago.

The repository you are looking at now is an archival copy of the
original revision control history of toast and some closely associated
projects, such as the toast web site, the toast linux distribution,
and some related tools. Much of this stuff is obscure and/or
previously unpublished. I now tend to think of them as relics of a
bygone era.

## Is any of this meant to be usable?

Not really? If you actually want to use toast, you're much better
off looking at the toast web site above than looking here. But, you
know, if that site were to disappear someday and someone wanted to
resurrect it for some reason, this might be a useful starting point
at least.

## Is toast itself still useful?

I haven't used it myself in years, but in principle, yeah, I think
it's retained quite a bit of the potential usefulness it still had
when I last used it actively. There may even still be other people
using it somewhere! But it's far less necessary than it was when I
started on it. There weren't many good alternatives then. Now there
are lots.

## What about toast linux?

I don't think it ever reached the point of usefulness for its
original purpose, no. Even at the time, getting toast linux to
actually build was nigh-impossible. Too many scattered dependencies
made it incredibly brittle. A caching HTTP proxy was an absolute
necessity, but far from sufficient. Trying to coax it into doing
anything nowadays would be far more difficult than it was then.

## Why does the toast website only go back to version 1.169?

Because that was the first version that was able to package itself
as a tarball for distribution. Older versions didn't know how to
do that and thus are not forward-compatible with the current www
script. This repository contains older, previously unreleased
versions of the tool.

## So the oldest version of toast dates to 2002?

I did a major rewrite of toast in 2002, from which the current
version is directly descended. What you're seeing in this repo dates
back only to that rewrite. If I find anything older I'll be sure
to add it here -- but I don't think any older versions still exist
anywhere. First version calling itself "toast" and performing the
same basic function might have been around 1997 perhaps, plus or
minus a year or two. The pre-2002 incarnation was much less
sophisticated, relying mainly on Makefile-rewriting to trick packages
into doing its bidding.

## Why publish this now?

I've been sort of meaning to do it for a long time now. As I write
this in April 2023, I'm in the process of updating my web site,
which only ever seems to happen during the rare times when I am
looking for a new job. I have vague plans to convert the web site,
including toast's portion thereof, into static pages that would be
simpler to host than the current dynamically-generated site. Assuming
that happens, I hope to store the static site generator in this
repository, alongside its inputs. I'm thinking I might try to wrap
something around the existing www script rather than try to extend
or update it.

## What the heck are these foo,v files? Shouldn't the comma be a dot?

There's this thing called
(RCS)[https://en.wikipedia.org/wiki/Revision_Control_System] that
wangles them. It's a bit like if git could only store one file per
repository. Pretend each `,v` file is a repository, and each
repository contains exactly one file.

I mean, yes, it's possible (and, I dare say, expected) to use RCS
to version-control more than one file. That's basically what CVS
is. And so much of why CVS is such a pain to deal with is precisely
because of that. But RCS itself is actually very nice to work with
-- provided you don't need to synchronize changes across more than
one source file!

RCS is the main reason I wrote each of these projects as a single
file. Many of which have other files embedded within them. I also
did it that way because making things self-contained is kind of
fun.

Nesting the `,v` files in a git repository is a little gross, but
it makes sense from an archival point of view, and it's also way
easier than trying to, say, convert it all into some more modern
form and still preserve all the commit messages and timestamps and
such. Plus the www script still expects to be able to use `rlog`,
`co`, and friends to operate on the bare `,v` files.

## So what's the license?

Great question. It's a bit of a mess! Some of these individual
files/projects have licenses attached to them, some don't. (Many
were never distributed.) If you would like a license for something
in here that doesn't have one, please don't hesitate to reach out!
