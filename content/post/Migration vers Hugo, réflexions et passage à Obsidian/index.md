---
title: Migration Hugo et passage à Obsidian
description: Retour sur la migration technique de mon site vers Hugo 0.148.1, l’abandon
  de getJSON, et une réflexion sur Obsidian comme source unique pour le contenu et
  le CV.
date: 2025-07-10
tags:
- hugo
- obsidian
- automation
- cv
- llm
- static-site
- developer-tools
ContentType: post
slug: migration-hugo-obsidian-cv
image: obsidian2hugo.png
obsidian-note-status:
- colorful:completed
modified: 2025-09-02T18:34:11+02:00
Status: published
author:
- Stéphane Wirtel

---

Rien de spectaculaire à signaler, si ce n'est que je viens de migrer mon site vers la dernière version stable de [Hugo]. L’outil reste toujours aussi impressionnant : ultra performant, aucun souci de vitesse ni de compilation.

En revanche, le [thème que j’utilise](https://github.com/jbub/ghostwriter) – toujours maintenu – ne suit pas entièrement les dernières évolutions de Hugo. Résultat : quelques blocages et ajustements à faire moi-même.

## Quelques problèmes rencontrés

1. **Commentaires internes non pris en charge**  
   Le thème ne supporte pas le nouveau système de commentaires intégré à Hugo. Dommage, surtout quand on veut rester sur une solution native.
2. **Google Analytics obsolète**  
   Je dois migrer vers une version plus récente. Honnêtement, je me demande encore comment mon site arrivait à afficher des stats… peu intéressantes, il faut l’avouer (mais bon, ce blog n’est pas très lu — et la faute m’en revient totalement 😅).
3. **Corrections de bugs liés aux entités HTML**  
   J’utilisais certaines entités HTML directement dans le contenu, ce qui posait problème avec les nouvelles versions. J’ai fait le ménage.

## 💡 Changement technique : adieu `getJSON`, bonjour `resources.GetRemote`


L’un des changements les plus concrets concerne l’utilisation de `getJSON` dans certains shortcodes — notamment pour [SpeakerDeck](https://speakerdeck.com). Depuis [Hugo 0.123](https://github.com/gohugoio/hugo/releases/tag/v0.123.0), [getJSON](https://gohugo.io/functions/data/getjson/) est déprécié, remplacé par `resources.GetRemote` couplé à `transform.Unmarshal`.

Voici le diff :  

```diff
-{{ $id := .Get "id" | default (.Get 0) }}
-{{- $item := getJSON "https://speakerdeck.com/oembed.json?url=https://speakerdeck.com/" $id -}}
-{{ $item.html | safeHTML }}
+{{ $id := .Get "id" | default (.Get 0) }}
+{{ $url := printf "https://speakerdeck.com/oembed.json?url=https://speakerdeck.com/%s" $id }}
+{{ $remote := resources.GetRemote $url }}
+{{ $json := $remote | transform.Unmarshal }}
+{{ $json.html | safeHTML }}
```

Ce changement rend le shortcode compatible avec les versions récentes de Hugo, et permet une meilleure intégration au système de cache. Simple, mais nécessaire.

## **✍️ Réflexion : Obsidian comme source unique**

Pendant cette mise à jour, je suis retombé sur un [article très inspirant de Jacob Kaplan-Moss](https://jacobian.org/til/hugo-obsidian/) où il explique comment il utilise **Obsidian comme source principale** pour alimenter son site statique généré avec Hugo.

Et là, je me suis dit: ce que je voulais faire depuis longtemps est désormais à portée de main.

### **Pourquoi je vais passer à Obsidian pour générer mon site (et mon CV)**

1. **J’utilise déjà Obsidian quotidiennement** — pour mes notes pro, perso, techniques, etc.    
2. **Centraliser tout** (connaissances, brouillons, idées d’articles, contenu de mon site) dans un même espace me semble évident.
3. **Je gagne du temps** :
	- J’écris mes articles directement dans mes notes.
    - Je peux automatiser l’export vers Hugo (posts/, projects/, cv/, etc.)
    - Je peux m’aider de **LLM** pour structurer ou améliorer le style (parce que soyons honnête : je suis développeur, pas rédacteur).
4. **Mon CV** est actuellement généré en LaTeX, via un pre-processing Python qui lit les fichiers markdown de mon blog et qui utilise un template latex pour ensuite générer le PDF définitif. Problème: dans mes Github Actions, je dois installer Python, puis charger une image Docker assez lourde pour compiler le tout.

-> Objectif : stocker toutes les données de mon CV dans Obsidian et générer dynamiquement mon site **et** un export PDF.

## **🔜 Prochaine étape : workflow nvim → Obsidian**

Je prépare donc une migration progressive de mon flux `nvim` / `VSCode` vers un système **Obsidian + automatisation**:
- **Templates de post** gérés via le plugin Templater
- **Notes liées aux projets** et aux expériences pro
- **Script d’export vers Hugo** 

## **🎯 Objectifs de cette transition**

- Gagner du temps
- Réduire le nombre d’outils et de formats
- Produire plus facilement du contenu structuré
- Et surtout, **valoriser mes compétences** (parce que oui, j’en ai — même si je galère encore à les exprimer correctement, en français comme en anglais)

Bref, un simple `hugo upgrade` qui déclenche une réorganisation complète de ma production de contenu.

La suite au prochain épisode 😉