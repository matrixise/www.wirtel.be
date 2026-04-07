---
title: "Ce livre Python que je voulais juste mettre à jour"
date: 2026-04-07
slug: livre-python-reconstruction
description: "Ce qui devait être une mise à jour rapide vers Python 3.14.3 s'est transformé en refonte complète — du pipeline de build au workflow d'écriture, en passant par dix ans d'évolution Python à rattraper."
tags:
- python
- obsidian
- pandoc
- typst
- claude-code
- livre
- formation
ContentType: post
Status: published
author:
- Stéphane Wirtel
modified: 2026-04-07T17:42:27+02:00

---

# Ce livre Python que je voulais juste mettre à jour

En août dernier, j'annonçais la relance de ce livre avec une certaine naïveté : j'avais retrouvé mon PDF de 2014, extrait le Markdown avec Docling, et assemblé un pipeline Longform → Pandoc → Typst. Je me disais que ce serait l'affaire de quelques semaines — mettre à jour les versions, ajouter quelques chapitres, boucler.

Huit mois plus tard, le périmètre a triplé, la chaîne d'outils a été réécrite, et la façon dont je travaille a complètement changé. Ce n'est pas ce que j'avais prévu. C'est mieux.

## À qui s'adresse le livre ?

Autant poser le cadre tout de suite. Ce livre vise des **développeurs qui savent déjà programmer** — en JS, Java, C++, Go, peu importe — et qui veulent apprendre Python correctement. Pas un cours d'initiation à la programmation, pas non plus un deep dive dans les internals de CPython. Le juste milieu : comprendre le langage, ses idiomes, son outillage moderne, avec les bons réflexes dès le départ.

Concrètement, c'est le profil d'un développeur backend qui débarque sur un projet Python et qui veut être opérationnel rapidement, sans traîner les mauvaises habitudes d'un tutoriel vite fait. Quelqu'un qui sait ce qu'est une classe, une exception, un test unitaire — mais qui ne connaît pas encore les dataclasses, le pattern matching, ou la différence entre `threading` et `asyncio`.

C'était déjà le public de mes formations en 2014. Ça n'a pas changé.

## Le pipeline a mûri

La première version du build s'appuyait sur **Longform**, un plugin Obsidian pensé pour l'écriture longue. Très bien pour démarrer, mais au fil du travail, j'ai eu besoin de plus de contrôle : savoir exactement quels fichiers entrent dans le PDF, dans quel ordre, avec quelles transformations appliquées.

J'ai fini par écrire ma propre chaîne. Le point de départ, c'est un fichier `SUMMARY.md` — même format que mdBook — qui sert de table des matières de référence :

```markdown
- [1. Premier contact](01-first-contact.md)
- [2.1 Syntaxe de base](02-python-language/02-01-syntax-basics.md)
- [2.2 Types de données](02-python-language/02-02-data-types.md)
  ...
- [7. Projet fil rouge](07-projet-fil-rouge.md)
```

Un script Python (`build-single-md.py`) lit ce fichier, fusionne tous les chapitres dans un seul Markdown, vire les frontmatters YAML, résout les variables de version comme `{{python_version}}`, et produit un gros Markdown propre. Pandoc prend le relais avec un filtre Lua qui gère les sauts de page entre chapitres. Et le template Typst s'occupe de toute la mise en forme : page de titre, typographie soignée, table des matières générée automatiquement.

La commande finale :

```bash
uv run scripts/build-pdf.py
```

C'est un pipeline déterministe. Je sais ce qui entre, je sais ce qui sort. Ça peut sembler anodin formulé comme ça, mais quand on travaille sur un document de sept chapitres qui doit rester cohérent d'un bout à l'autre, cette prévisibilité change vraiment la donne. Plus de surprises à la génération du PDF, plus de chapitres manquants ou dans le mauvais ordre.

## Pourquoi 3.14.3 et pas 3.13

Quand j'ai relancé le projet en 2025, la cible était Python 3.13. Sauf que pendant que j'écrivais, Python 3.14 est sorti — avec des nouveautés qui méritent clairement leur place dans un livre d'introduction. Les **t-strings** (PEP 750) apportent un nouveau type de chaîne de caractères avec le préfixe `t"..."`, qui retourne un objet `Template` au lieu d'évaluer immédiatement l'expression. L'évaluation différée des annotations (PEP 649) change la façon dont Python traite les type hints. Et le REPL est désormais coloré par défaut. Autant viser juste.

La version de référence dans tout le livre est donc **3.14.3** — dans le code, dans les exemples, dans les URLs de documentation. Une variable centrale dans `book.toml` garantit la cohérence partout : quand la prochaine version sortira, un seul changement mettra tout à jour.

## Superwhisper et Claude Code dans la boucle

C'est probablement le changement le plus significatif de ces derniers mois. J'ai intégré **Claude Code** directement dans le workflow de modernisation du livre — et plus largement dans toute ma façon d'écrire.

Une grosse partie du texte que vous lisez, je la **dicte**. Superwhisper ouvert, je parle, j'explique, je digresse parfois. Le résultat brut est souvent redondant — je me répète, je reprends un sujet sous un angle différent sans m'en rendre compte, j'oublie un mot ou je tronque une phrase. Un LLM passe ensuite sur le texte : il supprime les doublons, reformule ce qui est bancal, corrige sans trahir le sens. Ce n'est pas lui qui écrit — c'est moi qui parle, et lui qui élagage.

Pour la modernisation du contenu technique, le fonctionnement est différent, plus structuré. J'ouvre des issues GitHub sur le repository du livre — une par thème à traiter. Par exemple : *"Ajouter l'opérateur walrus `:=` dans le chapitre Structures de contrôle"*, ou *"Clarifier ExceptionGroup et `except*` dans le chapitre Exceptions"*. Puis je lance des agents Claude Code autonomes qui vont, chacun dans leur coin, travailler sur leur issue :

1. Lire l'issue et les fichiers Markdown concernés
2. Créer un worktree Git isolé (`git worktree add`)
3. Modifier le chapitre, écrire ou mettre à jour les exemples Python
4. Ajouter ou corriger les tests correspondants
5. Valider avec `pytest` et reconstruire le PDF pour vérifier que tout compile
6. Créer un fragment changelog via towncrier
7. Commiter, pusher, ouvrir une PR

Je peux lancer plusieurs agents en parallèle sur des issues indépendantes. De la gestion de projet logiciel appliquée à l'écriture d'un bouquin. Ça a l'air un peu overkill dit comme ça, mais en pratique, ça fonctionne remarquablement bien. Les PRs arrivent propres, les tests passent, le PDF se génère. Je relis, j'ajuste, je merge. Le rythme de modernisation a accéléré d'un coup.

## Dix ans d'évolution à rattraper

Entre Python 3.4 (la version du livre original) et Python 3.14, il y a une décennie d'évolution du langage. Pas juste des ajustements cosmétiques — des changements fondamentaux dans la façon dont on écrit du Python au quotidien. Voici les ajouts majeurs que le livre couvre désormais, chacun avec sa version d'introduction.

**Côté langage :**

- L'**opérateur walrus** `:=` (3.8, PEP 572) — des assignment expressions dans les conditions et les boucles
- Les **type hints** avec generics natifs : `list[str]`, `dict[str, int]` sans passer par `typing` (3.9)
- Les **union types** avec `|` : `str | None` plutôt que `Optional[str]` (3.10, PEP 604)
- Le **pattern matching** `match`/`case` (3.10, PEP 634)
- `except*` et **`ExceptionGroup`** — le vrai regroupement d'exceptions (3.11, PEP 654), à ne pas confondre avec le classique `except (A, B)` qui capture plusieurs types mais existe depuis Python 2
- Les **f-strings** améliorées : `f"{x=}"` pour le debug (3.8), expressions imbriquées sans restriction (3.12)
- Les **t-strings** `t"..."` — des template strings qui ne s'évaluent pas immédiatement (3.14, PEP 750)

**Côté outillage :**

En 2014, MyPy n'existait pas. Ruff non plus. uv non plus. Pip était lent, les environnements virtuels étaient un rituel pénible, et le type checking était une idée exotique que quelques équipes Google pratiquaient en interne. Dix ans plus tard, l'écosystème s'est profondément transformé — et en grande partie grâce à [Astral](https://astral.sh), qui a eu l'idée simple mais dévastatrice de réécrire les outils Python en Rust :

- **MyPy** — le type checker qui a tout lancé, présenté à PyCon Montréal en 2015, devenu incontournable
- **ty** — le nouveau type checker d'Astral, en Rust : sur un projet moyen, il est dix à cent fois plus rapide que MyPy
- **Ruff** — le linter d'Astral qui a tué flake8, isort et black en un seul outil ; j'ai arrêté de configurer trois outils séparément le jour où je l'ai essayé
- **uv** — le gestionnaire de paquets et d'environnements d'Astral ; `pip install` sur un gros projet prenait 40 secondes, avec uv c'est 2 secondes
- **Typer** — CLIs modernes et élégantes, adieu l'argparse manuel
- **pytest** — avec les fixtures, `unittest.mock`, les marqueurs, et tout l'écosystème de plugins
- **pdb / `breakpoint()`** — parce que déboguer, ça s'apprend aussi

**Côté bibliothèques :**

- **HTTPX** aux côtés de `requests` — quand on travaille avec asyncio, `requests` bloque la boucle événementielle, HTTPX non
- **pathlib** partout où il y avait du `os.path` — plus lisible, plus pythonique
- **tomllib** dans la stdlib (3.11) — fini les dépendances externes pour lire du TOML
- **`@dataclass`** (3.7) avec ses options modernes : `slots=True` et `kw_only=True` ajoutés en 3.10

**Côté concurrence :**

Le chapitre asyncio était déjà là, avec threading et multiprocessing. Ce qui est nouveau, c'est le **free-threading expérimental** (PEP 703) : depuis Python 3.13, on peut désactiver le GIL pour obtenir du vrai parallélisme entre threads. C'est le sujet le plus suivi et le plus commenté dans la communauté CPython depuis deux ans. Le livre en parle, avec les nuances qui s'imposent — c'est encore expérimental en 3.14, mais c'est un tournant majeur pour l'avenir du langage.

## GitHub Actions, Docker, et la productivité au quotidien

En 2014, on parlait déjà de CI/CD — Jenkins était omniprésent — et Docker venait tout juste de sortir. Mais mettre ça en place demandait une infrastructure dédiée, un ops disponible, et pas mal de patience. Aujourd'hui, GitHub Actions a tout changé : un fichier YAML dans le repo, et n'importe quel projet Python a un pipeline de CI complet en dix minutes, gratuitement.

J'ai vécu cette transition. À l'époque je configurais Jenkins à la main sur un serveur dédié, j'écrivais des Dockerfiles approximatifs qui finissaient avec des images de 2 Go parce que personne ne savait encore ce que c'était qu'un multi-stage build. Aujourd'hui le minimum viable est beaucoup plus haut — et beaucoup plus simple à atteindre.

Ces deux sujets rejoignent le chapitre 5 (Outils de développement). L'idée n'est pas d'en faire un cours DevOps — c'est hors scope — mais de montrer les fondamentaux qui servent au quotidien.

Pour **GitHub Actions**, ça tient en peu de choses : un workflow qui lance ruff, mypy et pytest à chaque push, avec une matrix sur plusieurs versions Python, et l'intégration native avec uv via `astral-sh/setup-uv`. Et le Trusted Publishing pour publier sur PyPI sans gérer de token manuellement.

```yaml
jobs:
  ci:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13", "3.14"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync
      - run: uv run ruff check .
      - run: uv run pytest -v
```

Pour **Docker**, le point d'entrée c'est le multi-stage build — séparer l'étape de build de l'image finale. Les images `ghcr.io/astral-sh/uv` sont une base commode pour ça. Quelques règles qui évitent les mauvaises surprises : `python:3.14-slim` plutôt qu'`alpine` (les wheels binaires ne compilent pas toujours sur musl), ne pas tourner en root, soigner le `.dockerignore` pour ne pas copier le `.venv` dans l'image.

Ce ne sont pas des sujets glamour. Mais c'est ce qui fait la différence entre un projet qui tourne sur ta machine et un projet qui tourne en production.

## Avancement

Sept chapitres, tous présents, tous fonctionnels. Je dirais qu'on est autour de **80%**. Deux chapitres restent trop légers par rapport à leur importance : le **Packaging** (uv, pyproject.toml, distribution — il y a plus à dire) et les **Structures de contrôle** (compréhensions, générateurs — trop synthétique pour l'instant). Ce sera la prochaine étape.

Et puis un livre, ça ne se finit pas vraiment — ça s'arrête. Il y aura des retouches au fil de la relecture, des exemples à affiner, des formulations à reprendre. C'est la nature du truc. L'objectif n'est pas la perfection, c'est d'avoir quelque chose de solide et d'honnête à mettre entre les mains d'un développeur.

Le **projet fil rouge** ferme le livre : un gestionnaire de tâches CLI baptisé `pytodo`, qui mobilise l'essentiel des concepts vus dans les chapitres précédents — dataclasses, pathlib, argparse, pytest, packaging. Un fil conducteur concret, pas juste un exercice isolé, pour que le lecteur consolide ses acquis sur un vrai petit projet de bout en bout.

## La chaîne complète aujourd'hui

- [Obsidian](https://obsidian.md) — rédaction, organisation, suivi de l'avancement via frontmatter et Dataview
- [Claude Code](https://claude.ai/code) — agents autonomes pour moderniser le livre chapitre par chapitre
- [Pandoc](https://pandoc.org/) — conversion Markdown vers PDF via Typst
- [Typst](https://typst.app) — mise en page moderne, rapide, bien plus agréable que LaTeX pour mon usage
- [uv](https://docs.astral.sh/uv/) — gestion de l'environnement Python du projet
- [towncrier](https://towncrier.readthedocs.io/) — gestion du changelog par fragments, une entrée par PR
- GitHub — versioning, issues, PRs (repository privé, projet Mgx.io)

## Publication

Le livre sera disponible **gratuitement** sur [mgx.io](https://mgx.io), en téléchargement direct. Ce n'est pas un produit commercial — c'est un document pédagogique, un point de départ solide pour apprendre Python tel qu'il se pratique en 2026.

Si vous développez en Python ou que vous envisagez de vous y mettre sérieusement, c'est fait pour vous. Pour être prévenu à la sortie, le plus simple reste de me suivre sur [LinkedIn](https://www.linkedin.com/in/stephanewirtel/) ou de garder un œil sur ce blog.

Derrière, j'ai déjà une liste de sujets qui attendent leur tour : FastAPI, DuckDB et Pandas pour l'analyse de données, profiling et debugging avancé en Python, peut-être un jour l'interopérabilité avec Rust. Mais d'abord, finir celui-ci.

L'outillage est en place. Les agents tournent. Le PDF se génère.

Il ne reste plus qu'à écrire — et cette fois, je sais exactement ce qui manque.

Stéphane