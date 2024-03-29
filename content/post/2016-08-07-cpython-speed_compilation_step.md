---
title: "CPython - Speed the compilation step"
draft: true
date: "2016-08-07T10:00:00+01:00"
comments: false
share: false
tags: ["python", "cpython", "compilation", "ccache", "autoconf"]
series: ["Welcome to CPython"]
slug: "cpython-speed_compilation_step"
---

## Introduction

I like to play with the source code of CPython, and of course, I need to compile it when I want to review a patch or test a new feature, as the literal string interpolation [PEP498](https://www.python.org/dev/peps/pep-0498).

In fact, these steps are really easy

* You have to download the sources.
* Uncrompress the archive
* Execute the `configure` script
* Run the `Makefile` for the compilation

Here are the normal steps

{{< highlight text >}}
> hg clone https://hg.python.org/cpython
> cd cpython
> ./configure --prefix=$PWD-build -q
> make -s
> ./python
{{< /highlight >}}

Ok, in this logic, the compilation of Python is easy, we have the sources, we compile them and just test it.

If you need to compile CPython with a new patch, just apply the patch and execute the `make` command, `make` will compile the updated files and will update the binary file (`python` in this case).

But sometimes, you have executed `make clean` and the binaries and the `.pyc` files are just removed from the working directory of CPython. In this case, you want to compile the source, you have to wait after some minutes for the compilation step.

In this post, I am going to explain you how to use ``ccache`` and the `cache` of `./configure`.

## ./configure

`./configure` is the script in the root directory of CPython, but this script is used for the configuration of the compilation step, it will interact with the installed libraries of your system and will inform you if you can or not, compile your CPython. This script has been generated by the `autotools`.

But I don't want to explain how to use the `autotools` and how to generate this `./configure` script. Just explain one argument `-C`.



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

## CCache

From the description of the site of ccache, ccache is a compiler. It speeds up recompilation by caching previous compilations and detecting when the same compilation is being done again.

https://ccache.samba.org/

### Features


* Keeps statistics on hits/misses
* Automatic cache size management
* Can cache compilations that generate warnings
* Easy installation
* Low overhead
* Optionally uses hard links where possible to avoid copies

### Installation

I use Fedora 24 and of course, the packaged version of ccache is 3.2.7 (released on 2016-07-20)

so, for the installation, just install it with dnf

{{< highlight text >}}
sudo dnf install ccache
{{< /highlight >}}

Once installed, you have to install it manually, the binaries are in the systems but not available.


## ./configure

