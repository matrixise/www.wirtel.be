---
title: "October - Week 40: Contributions to CPython"
date: 2018-10-19T12:23:28+02:00
description: "I start, again..."
tags: ["python", "contribution"]
slug: "2018-october-week40-contributions-to-cpython"

---

# My Contributions to CPython

Voilà, since the October 4th, I am contributing to CPython, and for one time, I
am really happy.

## Why?

It's really difficult to find a little bit of time for the CPython contributions
because I am freelance and I have a full-time schedule for my customers. At the
beginning I was afraid but with time and it is a success (for me) because
[my company](https://www.mgx.io) is 1 year old and has its first employee since some
months.

On the other side, I also have my family with my daughter and my wife where I
have to be present for them, so we can say this is a full-time job.

I also participate in some events, EuroPython, PyCon US, PyCon France, PyCon
Ireland, etc... I am also a co-organizer of EuroPython (I do not like this term
I prefer to say I am in the website work-group and than I try to work with the
other developers and improve the website ;-))

And lately, since April 2018, I started to prepare my Karate black belt, this
step of my life requires a lot of time. This step is really important for me,
because I began Karaté at the end of the 90s and I would like to pass my exam
and have the possibility to say "I did it". After that, I will continue, for me
Karate is respect, the discipline, and the sharing.

In October, I finished my missions for my customers, during 20 months I worked
for them. For 20 months I travel a lot, I was often on the road. And thus, I
decided to take a sabbatical month, without any customer. Just my family
and the #python community

Firstly, I fixed a lot of things at home ;-) now, my family is happy and me as
well because I finished all the boring stuff.

Secondly, I started to contribute to CPython and now I can say
I proposed [pull requests](https://github.com/python/cpython/pulls) and you can find
[all my merged PR](https://github.com/python/cpython/pulls?utf8=%E2%9C%93&q=is%3Amerged+is%3Apr+author%3Amatrixise+closed%3A2018-10-01..2018-11-01+)

| #bpo                                            | #pr                                                 | title                                                           |
|:------------------------------------------------|:----------------------------------------------------|:----------------------------------------------------------------|
| [bpo-23420](https://bugs.python.org/issue23420) | [9925](https://github.com/python/cpython/pull/9925) | Verify the value of '-s' when execute the CLI of cProfile       |
| [bpo-34967](https://bugs.python.org/issue34967) | [9827](https://github.com/python/cpython/pull/9827) | Sphinx is deprecating add_description_unit, use add_object_type |
| [bpo-34962](https://bugs.python.org/issue34962) | [9806](https://github.com/python/cpython/pull/9806) | make doctest in Doc now passes, and is enforced in CI           |
| [bpo-34913](https://bugs.python.org/issue34913) | [9782](https://github.com/python/cpython/pull/9782) | Document gzip command line interface                            |
| [bpo-23596](https://bugs.python.org/issue23596) | [9781](https://github.com/python/cpython/pull/9781) | Use argparse for the command line of gzip                       |
| [bpo-23596](https://bugs.python.org/issue23596) | [9775](https://github.com/python/cpython/pull/9775) | Add unit tests for the command line for the gzip module         |
| [bpo-34906](https://bugs.python.org/issue34906) | [9735](https://github.com/python/cpython/pull/9735) | Doc: Fix typos (2)                                              |
| [bpo-34906](https://bugs.python.org/issue34906) | [9712](https://github.com/python/cpython/pull/9712) | Doc: Fix typos                                                  |
| [bpo-24658](https://bugs.python.org/issue24658) | [1705](https://github.com/python/cpython/pull/1705) | Fix read/write on file with a size greater than 2GB on OSX      |


## On macOS, support the file where the size is greater than 2 GiB.

I am really proud of this PR because it's a very old pull request. In the past,
before the migration to GitHub, Ronald Oussoren had proposed a patch for Python
3.4 but the patch were never merged.

In 2016, I started to work on this patch for 3.5 and 3.6 but there was a problem
during the review, the patch must have been for the merge and with the several
reviews, I have completely rewritten it.

During the CPython sprints of PyCon US 2017, I have ported the patch to a pull
request in GitHub. Not really difficult, excepted there was a problem with
Travis, AppVeyor and some others tools, a problem with the memory, the worker is
limited to 3GB of RAM on Travis and the job for my PR was simply killed ;-)

Great, how my pull request could be merged if the worker kills the process? ;-)

Normally, once merged, this PR could fix this [numpy issue](https://github.com/numpy/numpy/issues/3858).

* bpo link: [open().write() fails on 2 GB+ data (OS X)](https://bugs.python.org/issue24658)

Thank you to [Victor Stinner](https://twitter.com/VictorStinner) for his review.

## make doctest in Doc now passes and is enforced in CI

Last week I was playing with Sphinx and the documentation located in the `Doc/`
directory of the project.

Just execute this command `make` and I saw there was a `doctest` target. I was
curious (it's really bad to be curious sometimes ;-)). So I type the command
`make doctest` and I see there were ~ 398 failed tests. What???

It's just impossible, I work on Python and normally Python is well tested, this
is true for the code, maybe not for the documentation. And I have started to
work on this issue with [Julien Palard](https://www.twitter.com/sizeof).

With this issue, we have updated Sphinx to the last version (1.8.1) because this
one supports a `:skipif:` option for the
[doctest](http://www.sphinx-doc.org/en/master/usage/extensions/doctest.html?highlight=skipif#directive-doctest)
directive.

In the case of the documentation, this is useful because we could execute the
tests excepted for turtle, and for that, we can use the directive with the
options:

```restructuredtext
.. testsetup::

    try:
        import tkinter as tk
    except ImportError:
        tk = None

.. doctest::
    :skipif: tk is None

``` 

Now, the documentation of CPython uses Sphinx 1.8.1 \o/ 

But with Sphinx 1.8.1, there was a [DeprecationWarning](https://docs.python.org/3/library/exceptions.html#DeprecationWarning).
[Julien](https://www.twitter.com/sizeof) has filled [an issue](https://bugs.python.org/issue34967) on the [bug tracker](https://bugs.python.org).

Here is the PR [9827](https://github.com/python/cpython/pull/9827) for this issue ;-)


* bpo link: [make doctest does not pass](https://bugs.python.org/issue34962)
* bpo link: [Sphinx is deprecating add_description_unit](https://bugs.python.org/issue34967)

Thank you to [Julien Palard](https://twitter.com/sizeof) for his review.

## Improve the CLI of Gzip with argparse.

Another surprise, I was looking for a new "easy" issue on [the bug tracker](https://bugs.python.org)
and I found on this one
[bpo-23596](https://bugs.python.org/issue23596). I see there is a patch from
Antony Lee, the patch was correct. But there was a problem, before the
integration of this patch, we need to have a unit test for the CLI.

The first step, write the test for the current CLI. Why do I need to write this
unit test? Because without a test, how can you validate that your patch works
fine?

So, I wrote my tests with a lot of `assert_python_ok`, `assert_python_failure`,
`subprocess.Popen`, etc...

At the end, I had one pull request with the tests, I was happy because this one
has been quickly merged.

The second step, take the patch of Antony Lee and try to improve it.
Once the patch converted to a pull request, this one has been merged.

The next step and the last one was the improvement of the documentation. Because
I do not know for you but I have discovered the CLI of gzip with this issue,
before I did not even know it existed ;-)

Thus a new CLI -> a new documentation and hello to the issue [bpo-34913](https://bugs.python.org/issue34913)

Finally, I am really glad to announce the [gzip](https://docs.python.org/3.8/library/gzip.html)
module has a documented and tested [CLI](https://docs.python.org/3.8/library/gzip.html#command-line-interface).

* bpo link: [Document gzip command line interface](https://bugs.python.org/issue34913)
* bpo link: [gzip argparse interface](https://bugs.python.org/issue23596)

Thank you to [Julien Palard](https://twitter.com/sizeof) for his review.

# Conclusion?

I can say I am just happy because I have fixed some issues and my oldest PR has been merged into master, 3.7 and 3.6.

And now, I have some Pull Requests to improve before merging.

| #bpo                                                | #pr                                                 | title                                                   |
|:----------------------------------------------------|:----------------------------------------------------|:--------------------------------------------------------|
| [bpo-34990](https://bugs.python.org/issue34990)     | [9892](https://github.com/python/cpython/pull/9892) | year 2038 problem in compileall.py                      |
| [bpo-34969](https://bugs.python.org/issue34969)     | [9833](https://github.com/python/cpython/pull/9833) | Add --fast, --best on the gzip CLI                      |
| [bpo-34839](https://bugs.python.org/issue34839)     | [9736](https://github.com/python/cpython/pull/9736) | Add a 'before 3.6' in the section 'warnings' of doctest |
| [bpo-1100942](https://bugs.python.org/issue1100942) | [5578](https://github.com/python/cpython/pull/5578) | Add datetime.time.strptime and datetime.date.strptime   |

Thank you,

Stéphane