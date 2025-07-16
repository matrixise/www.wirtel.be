---
title: Génial, un bug fixé rapidement
description: Une issue ouverte sur GitHub, une réponse rapide du mainteneur, et une mise à jour du thème Ghostwriter compatible avec Hugo 0.148.0. Vive l'open source !
date: 2025-07-16
tags:
  - hugo
  - ghostwriter
  - theme
  - static-site
  - github
  - open-source
  - git
  - submodule
---

L’Open Source, c’est vraiment cool.

La semaine dernière, je vous expliquais que j’avais dû mettre à jour mon site, ce qui incluait une montée de version du thème que j’utilise. À cette occasion, j’ai ouvert [une issue](https://github.com/jbub/ghostwriter/issues/126) sur le dépôt GitHub du thème, en signalant un problème lié au support du nouveau système de commentaires introduit par [Hugo](https://gohugo.io).

Ce matin, j’ai reçu un message du développeur du projet : le thème est désormais compatible avec Hugo `0.148.0`.

Évidemment, je me suis empressé de le remercier. J’avais l’impression que le projet était en pause, mais non : il est bien actif.

J’ai donc récupéré la dernière version du thème, et commencé à l’intégrer dans mon projet.

## Passage au dépôt officiel

J’utilisais jusque-là un fork. J’ai donc basculé vers le dépôt officiel en quelques lignes :

```
git submodule set-url themes/original-ghostwriter https://github.com/jbub/ghostwriter.git
git submodule update --remote themes/original-ghostwriter
```

Ensuite, pour vérifier que tout s’est bien mis à jour :
```
git submodule status
```

Puis, un petit commit pour intégrer le changement :

```
git add .gitmodules themes/original-ghostwriter
git commit -m "Mise à jour du thème Ghostwriter vers la version officielle"
```

Encore merci à [@jbub](https://github.com/jbub) pour sa réactivité et sa réponse rapide.

Ce genre d’interaction rappelle pourquoi j’aime autant le logiciel libre.

  

Vive les logiciels libres !