+++
title = "Francisez Python ;-)"
draft = true
tags = ["cpython", "python", "pyconfr", "grammar"]
date = "2016-10-14T16:30:00"
+++

# PyConFR 2016

Durant la PyConFR qui s'est deroulee a Rennes (en France), j'ai demarre un tout petit projet amusant, essayer d'avoir un Python en Francais. Oui, vous avez bien lu, en Francais. Et pourquoi ? Juste parce que nous etions a PyConFR en France ;-)

Dans ce cas, j'ai lu le `Makefile` du projet et j'ai trouve une reference vers le fichier `Grammar/Grammar`.

# Grammar

# Grammar/Grammar

# Parser/pgen

# Demo

1. Modifier `Grammar/Grammar`
2. Compiler `Parser/pgen` avec `Makefile`
3. Executer `Parser/pgen`
4. Compiler `Python` avec la nouvelle grammaire

{{< highlight bash >}}
> make Parser/pgen
> ./Parser/pgen Grammar/Grammar Include/graminit.h Parser/graminit.c
> make
> ./python /tmp/demo.py
{{< /highlight >}}
