---
title: Utilisation d'Obsidian comme source pour Hugo
date: 2025-09-04
slug: use-obsidian-as-source-for-hugo
description: Centraliser ses notes dans Obsidian et publier avec Hugo grâce à un script
  maison. Un workflow fluide, automatisé et cohérent.
tags:
- obsidian
- hugo
- markdown
- folder-notes
- python
created: 2025-09-04T15:37:28+02:00
modified: 2025-09-04T20:50:54+02:00
obsidian-note-status:
- colorful:completed
Status: published
ContentType: post
author:
- Stéphane Wirtel

---

Au début juillet, dans mon précédent post [Utilisation d'Obsidian pour Hugo]({{< relref "Migration vers Hugo, réflexions et passage à Obsidian/index" >}}) , j’expliquais que je regardais comment utiliser [Obsidian] comme source pour mon blog. Jusqu’ici, j’écrivais mes posts dans VS Code ou NeoVim, mais comme [Hugo] repose sur du Markdown, l’idée d’utiliser directement Obsidian s’est imposée assez naturellement : tout centraliser dans un seul outil, mes notes et mes articles.

L’avantage est que j’ai toutes mes données dans un seul et unique endroit, donc je n’ai plus besoin de rechercher mes infos pour écrire mon article et l’écriture devient plus fluide, car tout est à portée de main.

## Les limites des outils existants

Alors oui, il existe déjà des solutions comme [Obsidian Export]. Le problème, c’est que ces outils ne vont pas assez loin. Ils fonctionnent pour la base, mais rencontrent des difficultés dès qu’on touche au **front matter** ou aux **Wikilinks**.
Par exemple :

- un Wikilink pointant vers un ancien article ne se convertit pas automatiquement en dans le [shortcode relref], la syntaxe attendue par Hugo ;
- un Wikilink dans un frontmatter n’est pas converti automatiquement ;
- le résultat « fait le job », mais pas comme je le souhaite, surtout si je veux garder une structure cohérente et bien intégrée à Hugo.

## La question des Folder Notes

Autre complexité : je mélange **Notes simples** et **[Folder Notes]**

- Les Folder Notes reposent sur un plugin Obsidian : un dossier = une note. Le fichier principal est alors `index.md` ou bien un fichier qui porte le nom du dossier avec l’extension `md`. Ce mode est pratique car il permet d’ajouter des images et pièces jointes sans encombrer l’espace de travail. Et surtout, cela colle parfaitement avec les **[Page Bundles]** de [Hugo].
- Les Notes classiques, elles, sont beaucoup plus simples : un fichier Markdown, quelques Wikilinks à convertir, et c’est tout.

Cette dualité Notes / Folder Notes est pratique dans Obsidian, mais elle complique un peu l’export vers Hugo.

## Ma solution : Obsidian2Hugo

Face à ces limites, j’ai développé mon propre script Python : **Obsidian2Hugo**.

Ce script :

- parcourt mes articles un par un ;
- corrige le front matter en ajoutant un `slug` si nécessaire ;
- corrige le Wikilink de image (utilisé par le thème ghostwriter) ;
- convertit les Wikilinks vers le [shortcode relref] ;
- copie les fichiers vers `content/post` dans la bonne structure.

Comme j’ai défini mes **permalinks** dans la config Hugo, j’obtiens automatiquement des URLs propres du type :

```toml
[Permalinks]
posts = post/:year/:month/:day/:slug
```

Résultat : j’ai enfin une chaîne complète et cohérente, depuis Obsidian jusqu’au rendu final dans Hugo, sans manipulations manuelles.

## Ce qu’il me reste à faire

Aujourd’hui, je peux écrire mes articles directement dans [Obsidian], profiter de la souplesse des Folder Notes, et générer des fichiers propres pour [Hugo]. C’est un énorme gain de temps.

Prochaine étape : appliquer cette logique à d’autres contenus, comme mon **CV**.

- Actuellement, mes données de CV viennent directement du site web, ce qui ne me satisfait pas vraiment.
- L’idée serait de maintenir la version complète (y compris mes expériences client) dans Obsidian, mais de n’exposer publiquement qu’une partie.
- Cela permettrait de gérer un équilibre **semi-public / semi-privé**, selon ce que je veux partager ou non.

C’est un chantier futur, mais la direction est claire : **tout centraliser dans Obsidian, et n’exporter que ce qui doit l’être**.

[Hugo]: https://gohugo.io
[Obsidian]: https://obsidian.md
[Obsidian Export]: https://github.com/zoni/obsidian-export
[Folder Notes]: https://lostpaul.github.io/obsidian-folder-notes/
[Page Bundles]: https://gohugo.io/content-management/page-bundles/
[shortcode relref]: https://gohugo.io/shortcodes/relref/