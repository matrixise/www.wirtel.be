+++
title = "CPython - Speed the compilation step"
draft=true
date="2016-08-07T10:00:00+01:00"
comments=false
share=false
tags=["python", "cpython", "compilation", "ccache", "autoconf"]
+++

## Introduction


### Demo

Since some months/years (in fact, when I have time), I like to play with the source code of CPython, and of course, I need to compile it when I want to review a patch or just because I want to test a new feature, as the literal string interpolation [PEP498](https://www.python.org/dev/peps/pep-0498/)

In fact, these steps are really easy, you have to download the source, uncompress the archive, execute the configure script for the configuration and run the Makefile for the compilation.

Here are the normal steps when you compile CPython

{{< highlight text >}}
> hg clone https://hg.python.org/cpython
> cd cpython
> ./configure --prefix=$PWD-build -q
> make -s
{{< /highlight >}}


Download CPython
================

	
CCache
======

From the description of the site of ccache, ccache is a compiler. It speeds up recompilation by caching previous compilations and detecting when the same compilation is being done again.

https://ccache.samba.org/

Features
--------

* Keeps statistics on hits/misses
* Automatic cache size management
* Can cache compilations that generate warnings
* Easy installation
* Low overhead
* Optionally uses hard links where possible to avoid copies

Installation
------------

I use Fedora 24 and of course, the packaged version of ccache is 3.2.7 (released on 2016-07-20)

so, for the installation, just install it with dnf

{{< highlight text >}}
sudo dnf install ccache
{{< /highlight >}}

Once installed, you have to install it manually, the binaries are in the systems but not available.


./configure
===========

Example::

{{< highlight text >}}
> time -p make -j 4 -s
> time -p ./configure --prefix=$PWD-build -q
real 13.06
user 7.18
sys 6.51
> time -p ./configure --prefix=$PWD-build -q -C
real 12.76
user 6.87
sys 6.53
> time -p ./configure --prefix=$PWD-build -q -C
real 2.62
user 1.08
sys 1.87
{{< /highlight >}}
