---
created: 2025-11-22T10:00:00+01:00
modified: 2026-01-14T07:49:15+01:00
tags:
- ai
- devops/automation
- event/pycon
- productivity
- python
- python/django
- python/wagtail
- tool/claude-code
- tool/mcp
- tool/obsidian
ContentType: post
title: "Claude Code : comment un assistant IA m'a fait gagner des jours de développement"
description: "Retour d'expérience sur l'utilisation de Claude Code pendant PyCon Ireland : automatisation de migrations Django/Wagtail, conversion de contenu scanné, et gain de productivité spectaculaire."
date: 2025-11-22
slug: claude-code-retour-experience-pycon-ireland
keywords:
language: fr
reading_time: 14
difficulty: intermediate
Status: published
author:
obsidian-note-status:

---

## TL;DR

Après une semaine d'utilisation intensive de Claude Code[^1] pendant PyCon Ireland et sur mes projets personnels, je suis complètement bluffé par les gains de productivité. L'outil m'a permis de migrer automatiquement le site Python Ireland de Django 5.0 vers 5.2 et Wagtail 6.2 vers 7.2, de développer un outil de conversion de livres scannés en 5 minutes, et de générer une documentation complète en quelques minutes. Contrairement à Cursor ou Windsurf, Claude Code s'intègre partout (PyCharm, VS Code, Zed, Neovim, ligne de commande), ce qui en fait un véritable game changer pour les développeurs professionnels.

## Table des matières

- [Introduction](#introduction)
- [Première découverte à PyCon Ireland](#première-découverte-à-pycon-ireland)
- [Révision automatisée d'un livre Python](#révision-automatisée-dun-livre-python)
- [Développement express : un outil de numérisation en 5 minutes](#développement-express--un-outil-de-numérisation-en-5-minutes)
- [Migration Django/Wagtail : le cas Python Ireland](#migration-djangowagtail--le-cas-python-ireland)
- [MCP GitHub : automatisation des issues et documentation](#mcp-github--automatisation-des-issues-et-documentation)
- [Polyvalence : l'avantage décisif face à la concurrence](#polyvalence--lavantage-décisif-face-à-la-concurrence)
- [Investissement et retour sur investissement](#investissement-et-retour-sur-investissement)
- [Points clés à retenir](#points-clés-à-retenir)
- [Ressources complémentaires](#ressources-complémentaires)
- [Conclusion](#conclusion)

## Introduction

Il y a une semaine, je n'utilisais pas Claude Code. Aujourd'hui, je ne peux plus m'en passer. Cette transformation radicale s'est produite pendant PyCon Ireland[^12] (15-16 novembre 2025) à UCD (University College Dublin[^13]), où j'ai commencé à utiliser cet outil littéralement le jour même de mon départ, un jeudi après-midi.

Ce qui m'a immédiatement frappé, c'est la capacité de Claude Code à accéder directement au filesystem via la ligne de commande. Cette fonctionnalité change complètement la donne par rapport aux assistants IA classiques comme ChatGPT, qui restent cantonnés à la génération de code sans interaction directe avec votre environnement de développement.

Dans cet article, je partage mon retour d'expérience après une semaine d'utilisation intensive : de la révision d'un livre sur Python 3.13 à la migration complète d'une application Django/Wagtail, en passant par le développement rapide d'outils personnalisés.

## Première découverte à PyCon Ireland

La première fois que j'ai lancé Claude Code, c'était pour analyser mon vault Obsidian[^2]. En quelques secondes, l'outil a parcouru mes notes, compris leur structure et généré une documentation complète de mon organisation personnelle. Cette première expérience m'a montré quelque chose de fondamental : Claude Code ne se contente pas de générer du code, il **comprend le contexte** de votre projet.

Concrètement, j'ai simplement lancé Claude Code dans mon répertoire de notes et initialisé le projet :

```bash
# Se placer dans le répertoire Obsidian
cd ~/obsidian-vault

# Lancer Claude Code
claude

# Initialiser le projet avec la commande slash
/init
```

Une fois initialisé, j'ai demandé à Claude Code d'analyser la structure de mon vault. L'outil a automatiquement :
- Identifié la structure des dossiers
- Analysé les liens entre les notes
- Détecté les tags et métadonnées
- Généré une documentation structurée

💡 **Astuce** : La capacité d'accès au filesystem de Claude Code le distingue des autres assistants IA. C'est ce qui permet des gains de productivité aussi spectaculaires.

## Révision automatisée d'un livre Python

Mon deuxième test a été encore plus impressionnant. J'avais commencé en juin-juillet à réviser un livre sur Python 3.13 que j'avais écrit il y a plusieurs années. Ce livre couvrait initialement Python 2.7 et 3.4 — une époque où les deux versions coexistaient dans l'écosystème.

J'ai demandé à Claude Code de m'aider à le mettre à jour. Voici ce qu'il a fait spontanément :

1. **Analyse du contenu** : détection automatique des versions Python obsolètes
2. **Découpage intelligent** : split du livre en plusieurs fichiers par chapitre
3. **Génération de frontmatter** : création de métadonnées YAML différentes pour chaque chapitre
4. **Proposition de modifications** : identification des sections nécessitant une mise à jour

Ce qui m'a vraiment bluffé, c'est que je lui ai demandé de **ne pas** modifier directement le livre, mais plutôt de proposer les modifications dans un fichier Markdown séparé. Résultat : j'ai pu réviser les suggestions sans risquer de perdre mon contenu original.

> 💻 **Approche utilisée** : Claude Code a créé un fichier `CHANGES.md` avec des suggestions structurées chapitre par chapitre, me permettant de valider ou rejeter chaque modification.

## Développement express : un outil de numérisation en 5 minutes

L'exemple le plus spectaculaire de gain de temps s'est produit dans le bus vers l'aéroport de Dublin. J'avais acheté un mois auparavant un scanner de livres (CZUR Shine Ultra Pro) pour numériser de vieux ouvrages de Karaté des années 70-80 (impossibles à trouver en ebook).

Mon workflow initial était le suivant :
1. Scanner les pages avec mon outil
2. Convertir les scans en Markdown avec Docling[^3]
3. Réviser manuellement le Markdown généré

Le problème : je n'avais pas d'outil pour faciliter l'étape 3. J'ai donc demandé à Claude Code :

> "Peux-tu me générer un outil avec Qt et Python pour m'aider à réviser et traduire des fichiers Markdown issus de scans OCR ?"

**Temps de développement : 5 à 10 minutes.**

L'outil génère automatiquement :
- Une interface Qt6 avec PyQt[^4]
- Un éditeur de texte avec coloration syntaxique Markdown
- Un système de validation et correction assistée

Ce qui m'aurait pris **2 jours de développement** a été fait en **10 minutes**, trajet en bus compris. Depuis, j'ai révisé une cinquantaine de pages sur la centaine scannée, et l'outil fonctionne parfaitement.

## Migration Django/Wagtail : le cas Python Ireland

Le cas le plus technique a été la modernisation complète du site web de Python Ireland[^5]. Le repository[^11] était resté sans maintenance pendant un an, avec des alertes de sécurité Dependabot[^6] non traitées depuis deux semaines.

Vendredi dernier, j'ai lancé Claude Code dans le repository et lui ai demandé d'analyser les problématiques de sécurité et de proposer un plan de modernisation. Voici le résultat de cette collaboration intensive.

### 📚 Documentation professionnelle

Claude Code a créé **2 364 lignes de documentation** de zéro, réparties en 3 guides complets :

- **CLAUDE.md** : Guide pour utiliser Claude Code sur ce projet (conventions, architecture, workflows)
- **CONTRIBUTING.md** : Guide complet pour les contributeurs avec process de PR, style de code, tests
- **DEVELOPMENT.md** : Documentation technique détaillée (setup local, structure, déploiement)

Cette documentation que je repoussais depuis des mois par manque de temps est maintenant d'une qualité professionnelle. Mes collègues de Python Ireland pourront reprendre le projet facilement.

### 📦 Montées de version majeures

Claude Code a orchestré plusieurs migrations complexes en parallèle :

**Stack applicative :**
```bash
Wagtail : 6.2 → 7.2
Django  : 5.0 → 5.2
Python  : 3.13.9
```

**Infrastructure :**
```bash
PostgreSQL : 13 → 17
```

**Breaking changes gérés :**
- Migration vers la nouvelle API `STORAGES` (Django 5.1+)
- Adaptation des modèles Wagtail pour la 7.2
- Mise à jour des settings PostgreSQL

### 🔧 Outillage développeur

Claude Code a ajouté **16 nouvelles commandes** dans le Taskfile pour améliorer le workflow :

**Commandes Heroku :**
```yaml
heroku:logs        # Afficher les logs en temps réel
heroku:restart     # Redémarrer l'application
heroku:migrate     # Lancer les migrations en production
heroku:rollback    # Rollback vers une version précédente
heroku:maintenance # Activer/désactiver le mode maintenance
```

**Outils qualité :**
```yaml
code:lint           # Linting avec ruff
code:check          # Vérifications complètes (types, format)
dependencies:security  # Scan de vulnérabilités avec pip-audit
dependencies:tree   # Visualisation de l'arbre des dépendances
```

### 🎨 Commande slash personnalisée

Claude Code a également créé une commande slash personnalisée pour générer des commits conventionnels avec emoji :

```bash
/commit-message

# Génère automatiquement un message de commit au format :
# ✨ feat: Ajouter la gestion des événements récurrents
#
# - Implémentation du modèle RecurringEvent
# - Interface d'administration Wagtail
# - Tests unitaires et fonctionnels
```

### 🐛 Corrections et sécurité

Au cours de la modernisation, Claude Code a identifié et corrigé plusieurs problèmes :

**Sécurité :**
- Vulnérabilité dans la dépendance `requests` (mise à jour vers version patchée)
- Ajout de `pip-audit` pour scan automatique des vulnérabilités

**Bugs :**
- Fix cascade delete : `PROTECT` sur les ForeignKey pour éviter les suppressions accidentelles
- Fix warnings timezone dans les tests (utilisation de `timezone.now()`)
- Correction des fichiers statiques pour Django 5.2

### 📋 Amélioration continue

Claude Code a documenté **23 améliorations** à apporter dans un fichier TODO structuré :
- Bugs identifiés avec reproduction steps
- Améliorations de qualité de code
- Tests manquants
- Optimisations de performance

### 🎯 Bilan

**En chiffres :**
- **23 commits** réalisés
- **~3 000 lignes** ajoutées (dont 2 364 de documentation)
- **Stack complètement modernisée** en une journée
- **0 régression** grâce aux tests existants

Ce qui m'aurait pris **plusieurs jours voire une semaine** de travail a été réalisé en **quelques heures** avec Claude Code. L'outil ne s'est pas contenté de faire les migrations : il a documenté, testé, amélioré et sécurisé le projet.

## MCP GitHub : automatisation des issues et documentation

L'une des fonctionnalités les plus puissantes de Claude Code est le support des **Model Context Protocol (MCP)**[^9]. Le MCP GitHub permet d'interagir directement avec GitHub sans quitter Claude Code : lire les issues, ajouter des commentaires, les fermer, tout cela de manière conversationnelle.

Sur le projet Python Ireland, j'ai utilisé le MCP GitHub pour traiter plusieurs issues ouvertes depuis des mois. Voici les résultats concrets.

### Issue #127 - Update README.md ✅ FERMÉE

**Contexte** : L'issue demandait une mise à jour complète de la documentation du projet.

**Action de Claude Code** :
1. Analyse du repository et de l'architecture
2. Création de 4 fichiers de documentation (2 364 lignes au total) :
   - **README.md** : Vue d'ensemble, installation, déploiement
   - **CLAUDE.md** : Guide pour utiliser Claude Code sur le projet
   - **CONTRIBUTING.md** : Processus de contribution, PR, style de code
   - **DEVELOPMENT.md** : Setup local, structure technique, debugging
3. Ajout d'un commentaire récapitulatif sur l'issue via MCP
4. Fermeture automatique de l'issue

**Résultat** : Documentation professionnelle créée en quelques heures au lieu de plusieurs jours. L'issue est résolue et fermée.

### Issue #110 - Add more tests 💬 COMMENTÉE

**Contexte** : Le projet manquait de tests unitaires et fonctionnels.

**Action de Claude Code** via MCP :
1. Analyse de la couverture de tests existante
2. Ajout d'un commentaire détaillé avec :
   - Guide complet pour améliorer la couverture
   - Recommandations d'outils (coverage, Factory Boy)
   - Structure de tests recommandée par app
   - Exemples de code pour :
     - Tests de modèles Django
     - Tests de Wagtail pages
     - Tests de management commands

**Extrait du commentaire généré** :

````markdown
## Recommandations pour améliorer la couverture de tests

### 1. Outils à installer

```bash
pip install coverage factory-boy pytest-django
```

### 2. Structure recommandée

```
website/
├── core/
│   └── tests/
│       ├── test_models.py
│       ├── test_views.py
│       └── factories.py
├── events/
│   └── tests/
│       ├── test_models.py
│       └── test_wagtail_pages.py
```

### 3. Exemple de test avec Factory Boy

```python
# core/tests/factories.py
import factory
from core.models import Event

class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    title = factory.Faker('sentence')
    datetime = factory.Faker('future_datetime')
```
````

**Résultat** : L'issue reste ouverte mais dispose maintenant d'un guide complet pour la résoudre. Les contributeurs ont toutes les informations nécessaires.

### Issue #111 - Support Timezone in DateTimeField 🔧 FIX PARTIEL

**Contexte** : Des warnings timezone apparaissaient dans les tests.

**Action de Claude Code** :
1. Identification du problème dans les tests
2. Application d'un fix (commit `e84fa12`) : remplacement de `datetime.now()` par `timezone.now()`
3. Documentation du fix complet dans `TODO.md` pour traiter tous les cas
4. Commentaire sur l'issue expliquant le fix partiel

**Résultat** : Fix appliqué pour les tests. L'issue reste ouverte pour le fix complet documenté dans le TODO.

### Avantages du MCP GitHub

**Productivité** :
- Interaction directe avec GitHub sans quitter l'éditeur
- Pas de switch entre terminal, navigateur et IDE
- Workflow conversationnel naturel

**Qualité** :
- Commentaires en anglais professionnel (crucial pour un non-anglophone)
- Code contextualisé aux bonnes versions (Python 3.13, Django 5.2, Wagtail 7.2)
- Références à la documentation pertinente

**Traçabilité** :
- Toutes les actions sont tracées sur GitHub
- Commentaires détaillés avec exemples de code
- Liens entre commits et issues

💡 **Astuce** : Le MCP GitHub transforme Claude Code en véritable gestionnaire de projet. Vous pouvez triager, commenter, et résoudre des issues sans jamais quitter votre terminal.

## Polyvalence : l'avantage décisif face à la concurrence

Beaucoup me demanderont : "Pourquoi pas Cursor[^10] ou Windsurf ?" La réponse est simple : **la polyvalence**.

### Comparaison des outils d'IA pour développeurs

| Outil | Intégrations | Ligne de commande | Accès filesystem | Prix mensuel |
|-------|--------------|-------------------|------------------|--------------|
| **Claude Code** | PyCharm, VS Code, Zed, Neovim[^14], CLI | ✅ Oui | ✅ Complet | 20-180€ |
| Cursor | VS Code fork | ⚠️ Limité | ⚠️ Partiel | ~20€ |
| Windsurf | Propriétaire | ❌ Non | ⚠️ Partiel | ~25€ |
| GitHub Copilot | VS Code, JetBrains | ❌ Non | ❌ Non | ~10€ |

### Mes cas d'usage réels

**Avec PyCharm** : développement du site Python Ireland
- Refactoring automatique
- Génération de tests
- Migration Django/Wagtail

**Avec Zed** : révision du livre Python 3.13
- Édition Markdown
- Génération de documentation
- Restructuration de contenu

**En ligne de commande** : automatisation et scripts
- Analyse de vaults Obsidian
- Génération d'outils Qt
- Gestion des repositories Git

**Avec Neovim** : édition rapide de fichiers de configuration
- Mise à jour de Taskfile
- Correction de YAML/TOML
- Modifications ponctuelles

💡 **Astuce** : La possibilité d'utiliser Claude Code partout signifie que je ne suis pas "marié" à un éditeur spécifique. Je peux choisir le meilleur outil pour chaque tâche sans perdre mon assistant IA.

## Investissement et retour sur investissement

Soyons honnêtes : Claude Code n'est pas gratuit. J'ai choisi l'abonnement **Max à 180€/mois** plutôt que l'abonnement de base à 17€/mois.

### Pourquoi cet investissement ?

1. **Gain de temps massif** : ce qui prenait 2 jours prend maintenant 10 minutes
2. **Qualité du code** : génération de code conforme aux meilleures pratiques
3. **Documentation automatique** : plus d'excuses pour ne pas documenter
4. **Polyvalence** : un seul outil pour tous mes besoins

### Calcul du ROI

En une semaine, Claude Code m'a fait gagner :
- **2 jours** sur le développement de l'outil de numérisation
- **5-7 jours** sur la modernisation complète de Python Ireland (migrations + 2 364 lignes de doc + outillage)
- **Plusieurs heures** sur la révision du livre Python 3.13

**Total : ~10 jours de développement économisés en une semaine.**

Au tarif freelance moyen d'un développeur Python senior (~500€/jour), cela représente **5000€ de valeur créée** pour un investissement de 180€.

🚧 **Attention** : Ces chiffres sont basés sur mon expérience personnelle. Votre retour sur investissement dépendra de vos projets et de votre façon d'utiliser l'outil.

## Points clés à retenir

- ✅ **Accès filesystem** : Claude Code interagit directement avec vos fichiers, contrairement aux assistants IA classiques
- ✅ **Polyvalence** : fonctionne avec PyCharm, VS Code, Zed, Neovim et en ligne de commande
- ✅ **Migrations automatisées** : capable de gérer des migrations complexes (Django 5.0→5.2, Wagtail 6.2→7.2)
- ✅ **Documentation instantanée** : génération de README, CONTRIBUTING et autres docs en minutes
- ✅ **MCP** : intégration native avec GitHub, Obsidian et autres services via Model Context Protocol
- ⚠️ **Investissement** : l'abonnement Max (180€/mois) est rentabilisé si vous l'utilisez intensivement
- 💡 **Game changer** : les développeurs qui n'adoptent pas ce type d'outils vont rapidement être dépassés

## Ressources complémentaires

- 📘 [Documentation officielle Claude Code](https://docs.anthropic.com/claude/docs)
- 🎥 [Introduction à Model Context Protocol (MCP)](https://www.anthropic.com/mcp)
- 🔗 [Taskfile : gestionnaire de tâches moderne](https://taskfile.dev)
- 🔗 [Toast : orchestration Docker](https://github.com/stepchowfun/toast)
- 🔗 [Factory Boy : fixtures Django](https://factoryboy.readthedocs.io/)

## Conclusion

Après une semaine d'utilisation intensive, je peux affirmer sans hésitation que Claude Code est un **game changer** pour les développeurs professionnels. L'outil ne remplace pas le développeur — il le rend exponentiellement plus productif.

Ce qui m'a le plus impressionné, c'est la capacité de Claude Code à **comprendre le contexte global** d'un projet. Il ne se contente pas de générer du code : il analyse, propose, corrige, documente et automatise.

Pour les développeurs qui hésitent encore, ma conclusion est claire : **Pour moi, Claude Code est devenu indispensable**. Chaque développeur devra trouver son propre équilibre avec l'IA. Ce n'est pas une question de savoir si vous allez adopter ces outils, mais quand.

Claude Code doit absolument faire partie de votre toolkit professionnel en 2025/2026.

---

💬 **Questions ou retours ?** N'hésitez pas à me contacter sur [Twitter/X](https://x.com/matrixise) ou sur mon compte [LinkedIn](https://www.linkedin.com/in/stephanewirtel/).

---

[^1]: https://claude.ai/code
[^2]: https://obsidian.md
[^3]: https://github.com/DS4SD/docling
[^4]: https://riverbankcomputing.com/software/pyqt/
[^5]: https://python.ie
[^6]: https://github.com/dependabot
[^7]: https://taskfile.dev
[^8]: https://github.com/stepchowfun/toast
[^9]: https://www.anthropic.com/mcp
[^10]: https://cursor.sh
[^11]: https://github.com/PythonIreland/website
[^12]: https://pycon.ie/pycon-2025/
[^13]: https://www.ucd.ie/
[^14]: https://github.com/coder/claudecode.nvim