---
title: "Va debugger ton Python"
date: 2017-09-23
tags: ["cpython", "gdb", "pdb"]
conferences: [
    "PyCon France 2017"
]
---

## A propos

Saviez-vous qu'il existe plusieurs manières de résoudre un problème en Python,
par exemple, il existe la fonction `print` que nous pouvons utiliser, mais aussi
le module `logging`. 

Ces deux méthodes fonctionnent bien dans certains cas, malheureusement dans
d'autres cas beaucoup plus 'tricky', ces deux options ne suffisent pas. Il faut
donc un autre outil, et quand j'ai commencé à développer, je ne connaissais pas
d'outils. Heureusement avec le temps et l'expérience, j'ai trouvé des outils, le
premier était `gdb` et le second `pdb`.

**GDB** est un débugger complet pour du code C, C++, etc... par contre, **PDB**
est axé pour [Python](https://www.python.org).

Dans cette présentation que j'ai donné à la PyCon 2017 de Toulouse, je vous
présente ces deux outils.

Je vous souhaite une très bonne lecture.

{{< speakerdeck "matrixise/va-debugger-ton-python" >}}
