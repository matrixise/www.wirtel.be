---
title: "Frenchify Python ;-)"
draft: true
tags: ["cpython", "python", "pyconfr", "grammar"]
date: "2016-10-14T16:30:00"
slug: "frenchify-cpython-37"
---

# PyConFR 2016

During the PyConFR in Rennes (France), I have started a funny project, try to have a Python in French. Yes, you have well read, in French. And why ? Because we are at PyConFR in France ;-)

So, in this case, I have read the `Makefile` of the project and I have found a reference to the `Grammar/Grammar` file.

# Grammar

# Grammar/Grammar

# Parser/pgen

# Demo

1. Modify `Grammar/Grammar`
2. Compile `Parser/pgen` with `Makefile`
3. Execute `Parser/pgen`
4. Compile `Python` with the new grammar

{{< highlight bash >}}
> make Parser/pgen
> ./Parser/pgen Grammar/Grammar Include/graminit.h Parser/graminit.c
> make
> ./python /tmp/demo.py
{{< /highlight >}}





