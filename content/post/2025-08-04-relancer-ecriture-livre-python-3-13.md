---
title: Relancer l'écriture de mon livre *Introduction à Python 3.13*
description: Relancer l’écriture de mon livre _Introduction à Python 3.13_ en m’appuyant
  sur Obsidian, Pandoc, Typst et une chaîne d’outils moderne et fluide.
date: 2025-08-04
updated: 2025-08-04
ContentType: post
Status: published
tags:
- python
- formation
- écriture
- livre-technique
- obsidian
- pandoc
- typst
modified: 2025-08-05T08:42:33
author:
- Stéphane Wirtel
slug: relancer-lecriture-de-mon-livre-introduction-a-python-3-13

---

# ✍️ Écrire (et réécrire) mon livre *Introduction à Python 3.13*

Quand j’ai commencé mon parcours en tant qu’indépendant, mon objectif était limpide : **donner des formations sur [Python](https://www.python.org)**. Expliquer comment l’utiliser, comment le comprendre, le structurer, le manipuler. Bref, **transmettre avec passion** tout ce que j’avais appris au fil des années.

À cette époque, Python 2 était encore bien présent, mais **Python 3 commençait à faire doucement son chemin**. En 2014, on utilisait la version 3.4, et dès 2015, la 3.5 était disponible.

Comme je tenais à proposer des formations de qualité, il me fallait un **support de cours solide**, fiable, clair — un document sur lequel m’appuyer pour accompagner les participants tout au long de l’apprentissage.

Mon format de prédilection, c’était les petits groupes : **10 participants maximum**. Cela favorisait les échanges, permettait une vraie interaction, et laissait le temps à chacun de poser ses questions.
Pour accompagner ces sessions, je voulais un **support de cours digne de ce nom**. Alors j’ai commencé à écrire un **livret pédagogique**, que je faisais imprimer via [Lulu](https://www.lulu.com). Le titre était simple et sans prétention : *Introduction à Python*.

J’en ai distribué plusieurs exemplaires lors de mes formations. Les retours étaient enthousiastes : les participant·es repartaient avec **un document concret**, clair, qu’ils pouvaient consulter à tête reposée ou annoter librement. Et moi, j’en étais **vraiment fier**.

Techniquement, j’utilisais [Sphinx](https://www.sphinx-doc.org) pour rédiger le contenu en **RestructuredText**, que je convertissais ensuite en PDF via une transcription en **LaTeX**.
Et malgré la complexité de LaTeX, il faut bien reconnaître une chose : ses rendus sont superbes. Les documents générés étaient soignés, bien structurés, avec une typographie élégante. Bref, **du travail propre**, comme j’aime.

Mais le temps a passé. Progressivement, **l’offre et la demande ont changé** : les demandes de formation se sont espacées, tandis que les **missions de consultance devenaient plus fréquentes** et plus longues. J’ai donc commencé à **me concentrer majoritairement sur la consultance**, parfois par choix, parfois par nécessité.

Naturellement, j’ai laissé de côté les formations.
J’en ai fait de moins en moins.
Et à force, **le projet de livre est passé au second plan**.
Le document, les fiches, le support… tout est resté en plan.

## 🔁 2025, retour aux sources

Nous sommes en 2025.
Cela fait maintenant près de dix ans que je me consacre principalement à la consultance.
Les formations se sont espacées, laissant place à des missions techniques variées et exigeantes.

J’ai eu l’occasion de contribuer à de nombreux projets, d’accompagner des équipes, et d’apporter une réelle plus-value.
J’en suis fier, et je sais que ce travail a laissé une empreinte positive auprès de mes clients.

Mais voilà, **l’envie de transmettre est revenue**.
J’ai envie de me replonger dans les formations Python.
Et pour ça, il me fallait **remettre la main sur mon ancien support** : ce petit livre que j’avais rédigé et imprimé pour mes sessions.

J’avais toujours un **exemplaire papier à la maison**, alors je me suis dit : pourquoi ne pas le **scanner**, et utiliser un **OCR** pour en récupérer le texte ?
Mais très vite, je me suis rendu compte que **scanner une centaine de pages**, puis passer chaque image à l’OCR, puis corriger à la main… ça allait être long. Très long.

C’est **durant cette étape de scan laborieuse** que j’ai repensé à [Lulu](https://www.lulu.com).
Je me suis connecté à mon compte, et j’ai eu une bonne surprise : **le projet du livre était encore là**, et avec lui, le **fichier PDF original** que j’avais envoyé à l’impression.

Une vraie bouffée d’air. Je pouvais partir de là.

## 🧪 Conversion et résurrection

Avec ce **fichier PDF de 2015** enfin retrouvé, je me suis lancé dans la mission suivante :
le convertir proprement en **Markdown**, pour pouvoir le retravailler dans Obsidian.

J’ai d’abord tenté les classiques : `pdf2latex`, `pdf2txt`, …
Mais les résultats étaient très aléatoires. Certaines pages passaient bien, d’autres étaient un fouillis complet.
Les titres étaient mélangés, les sauts de ligne mal gérés, et la structure globale devenait vite inutilisable.
Bref, rien de vraiment exploitable sans passer plusieurs soirées à tout remettre à plat à la main.

En creusant un peu plus, je suis tombé sur une bibliothèque Python prometteuse : [EasyOCR](https://www.jaided.ai/easyocr/).
Et c’est en fouillant autour d’[EasyOCR](https://www.jaided.ai/easyocr/) que j’ai découvert [Docling](https://docling-project.github.io/docling/), un outil plus complet, pensé pour **analyser des documents PDF ou images**, détecter les blocs de texte avec OCR, et les convertir directement en **Markdown**.

Et là, ça a tout changé.
[Docling](https://docling-project.github.io/docling/) m’a permis de traiter mon PDF d’un coup, page après page, pour en extraire un Markdown structuré.

Voici la commande que j’ai utilisée :
```sh
docling –from pdf –to md –verbose fichier.pdf
```

Le résultat s’est retrouvé dans un fichier `fichier.md`.
Propre. Exploitable. Prêt à être ouvert dans **Obsidian**, mon outil favori pour organiser mes notes, projets, idées… et maintenant, pour reprendre l’écriture de mon livre.

À partir de ce moment-là, tout s’est remis en mouvement.



## 🧰 Obsidian, Longform, Pandoc, Typst

Je travaille déjà quotidiennement dans **Obsidian**, où je centralise toutes mes connaissances.
C’est là que je note tout ce que j’apprends, ce que je découvre, ce que je veux approfondir.
Et comme tout est en Markdown, cela m’a paru naturel d’y importer le fichier généré par [Docling](https://docling-project.github.io/docling/) et de l’exploiter directement.

Ce qui a vraiment déclenché la reprise de l’écriture, c’est un plugin : **[Longform](https://github.com/kevboh/longform)**.
Ce plugin est spécialement conçu pour écrire des livres ou des projets structurés.
Il me permet de :
- découper mon ancien PDF en chapitres (un fichier Markdown par section),
- ajouter des métadonnées YAML utiles pour le suivi,
- générer un **manuscrit final**, concaténé automatiquement.

Ce système commence vraiment à me convenir : je peux travailler **chapitre par chapitre**, sans me disperser, tout en gardant une vision claire du projet dans son ensemble.

Une fois le manuscrit généré, je le passe dans **[Pandoc](https://pandoc.org/)**, qui se charge de le convertir en PDF en utilisant **[Typst](https://typst.app)** — un moteur de rendu bien plus rapide et souple que LaTeX, surtout pour mon usage.

```bash
pandoc IntroductionPython.md \
    --metadata-file metadata.yaml \
    --pdf-engine=typst \
    --template=template.typ \
    -o IntroductionPython.pdf
```

Grâce aux templates de **[Pandoc](https://pandoc.org/)**, je peux utiliser un modèle Typst, le personnaliser à ma guise : ajouter des styles, une page de garde, une page de fin, structurer la typographie… exactement comme je le souhaite.
C’est simple, élégant, et ça me permet de me concentrer sur **le fond**, pas sur **la mise en page**.



## 🧠 Organisation et productivité

À ce stade, j’ai donc réussi à :
- récupérer l’intégralité du contenu de mon PDF de 2014,
- le convertir proprement en Markdown,
- le structurer dans Obsidian avec Longform,
- l’exporter avec Pandoc, en utilisant un template Typst pour produire un PDF personnalisé.

Je peux maintenant travailler **chapitre par chapitre**, sans distraction ni surcharge.
Chaque fichier dispose d’un bloc YAML (les fameux *frontmatters*) contenant des métadonnées utiles.

Je vais pouvoir les exploiter avec le plugin [Dataview](https://blacksmithgu.github.io/obsidian-dataview/), afin de **suivre l’avancement du projet** : ce qui est rédigé, ce qui reste à relire, ce qui doit encore être mis à jour, etc.
Un vrai tableau de bord, directement dans Obsidian.

Et puisque tout est en Markdown, je peux également échanger avec **ChatGPT directement depuis Obsidian**, via des plugins intégrés.
Très pratique pour relire un chapitre, reformuler un paragraphe, ou repérer des incohérences.

Et soyons honnêtes : entre Python 3.4 et Python 3.13 (et bientôt 3.14), **les évolutions sont énormes**, donc un peu d'aide sera toujours la bienvenue.

Le système de typage, l’adoption généralisée d’`asyncio`, l’apparition de `match/case`, sans parler de toutes les nouvelles fonctionnalités du langage.

Donc oui, il y a **beaucoup de travail**.
Mais franchement… **ça me motive**.


## 📘 Le manuscrit, et après ?

Avec tous les chapitres structurés dans Obsidian et réunis via Longform, je peux générer un manuscrit complet en Markdown.
Une fois converti avec Pandoc et stylisé avec Typst, j’obtiens un PDF de qualité professionnelle.

Aujourd’hui, le livre fait environ 60 pages, mais il est encore en construction.
Je dois y intégrer plusieurs éléments essentiels pour être à jour :
- des exemples avec `requests` et `numpy`, `pandas`,
- l’usage de asyncio en situation réelle, `httpx`, `aiohttp`
- le `match/case` et d’autres nouveautés du langage.

Le gros avantage, c’est que tout mon flux est maintenant en place.
Je n’ai plus à réfléchir à l’outillage, je peux me concentrer uniquement sur le contenu.

## 📚 Et après Introduction à Python ?

En explorant mes anciennes notes, je suis retombé sur plusieurs projets mis de côté :
- Introduction à SQLAlchemy,
- Introduction à Flask,
- Introduction à Django.

Mais aujourd’hui, j’ai d’autres priorités et envies.
Je souhaite plutôt me diriger vers :
- Création d’API web avec Python et FastAPI,
- Utilisation de DuckDB et Pandas pour l’analyse de données,
- Profiling, debugging en Python,
- PostgreSQL avancé,
- Écriture de modules C pour Python.
- Écriture de modules Rust pour Python

Et tout ça pourra s’appuyer sur la même logique : notes en Markdown, centralisation dans Obsidian, structuration avec Longform, puis génération propre avec Typst + Pandoc.

## 💡 Les bons outils, au bon moment

Ce qui me frappe en 2025, c’est la maturité de l’écosystème.
Des outils comme Obsidian, Pandoc, Typst, GPT… tout est là, robuste, extensible, prêt à l’emploi.

Dans le passé, j’avais déjà bricolé mes propres scripts pour générer des supports de conférences.
Mais aujourd’hui, je sens que j’ai enfin une chaîne cohérente et fiable pour écrire vite et bien.

Et surtout, je n’ai plus besoin de me battre avec LaTeX pour obtenir un résultat propre.
Typst est rapide, souple, agréable.

## 🧰 Les outils utilisés

Voici les outils qui composent ma chaîne d’écriture et de publication :

- [Python](https://www.python.org) — Le langage que j’enseigne et que j’utilise au quotidien.
- [Obsidian](https://obsidian.md) — Mon outil central pour organiser les chapitres et mes notes.
- [Longform](https://github.com/kevboh/longform) — Plugin Obsidian pour organiser et compiler les chapitres d’un livre.
- [Dataview](https://blacksmithgu.github.io/obsidian-dataview/) — Plugin Obsidian pour visualiser l’état d’avancement à partir des métadonnées.
- [Pandoc](https://pandoc.org/) — Le convertisseur universel Markdown → PDF, via Typst.
- [Typst](https://typst.app) — Moteur de mise en page moderne, rapide et élégant.
- [Docling](https://docling-project.github.io/docling/) — Outil OCR pour convertir des PDF ou images en Markdown structuré.
- [EasyOCR](https://www.jaided.ai/easyocr/) — Moteur OCR performant pour la reconnaissance de texte dans les scans.
- [Lulu](https://www.lulu.com) — Plateforme d’impression à la demande utilisée pour mes premières impressions papier.
- [Sphinx](https://www.sphinx-doc.org) — Utilisé à l’origine pour la documentation en ReStructuredText.
- [ChatGPT](https://openai.com/chatgpt) — Mon assistant pour reformuler, relire ou améliorer les chapitres.


## 📦 Et la publication ?

Pour commencer, je pense proposer Introduction à Python 3.13 en accès libre.
Un peu comme un produit d’appel : bien fait, utile, mais gratuit.
Et ensuite, si l’accueil est positif, je publierai d’autres titres plus avancés, éventuellement sur Amazon ou Lulu.com.

Je réfléchis aussi à utiliser GPT ou Claude pour traduire certains contenus.
L’idée serait de garder mon style tout en touchant un public plus large, sans y passer un temps déraisonnable.

## 🎯 Ce qui compte vraiment

Je suis content de ce que j’ai remis en place.
Les outils fonctionnent, le rythme revient, et surtout : l’envie est là.

Je compte écrire une petite série d’articles expliquant :
- comment récupérer du contenu depuis un PDF,
- comment organiser l’écriture dans Obsidian avec Longform,
- comment styliser proprement avec Typst et générer un PDF final.

Ce sera modeste, mais j’espère utile.

On verra d’ici quelques mois où cela mène.
Mais franchement, je suis motivé.

Merci d’avoir pris le temps de me lire 🙏
Je vous souhaite beaucoup de belles idées, de projets bien menés, et de plaisir à coder.

Moi, je poursuis sur cette lancée… et aussi sur ma plateforme viticole 🍷
À très vite !

— Stéphane