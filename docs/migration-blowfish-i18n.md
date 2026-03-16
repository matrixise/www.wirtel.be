# Migration Blowfish + i18n (fr/en)

Date : 2026-03-16
Branche : `worktree-curried-gliding-hinton`

## Objectif

Migrer le site wirtel.be du thème Ghostwriter (monolingue) vers **Blowfish** (Tailwind CSS, dark mode, TOC, search Fuse.js) avec support bilingue **fr/en** natif via Hugo Modules.

---

## Ce qui a été fait

### 1. Thème Blowfish via Hugo Modules

- `go.mod` : ajout de `github.com/nunocoracao/blowfish/v2 v2.100.0`
- `go.mod` : conservation de `github.com/mfg92/hugo-shortcode-gallery v1.3.0` (utilisé dans un post FR)
- `go.sum` régénéré via `hugo mod get` + `hugo mod tidy`

**Problèmes rencontrés :**
- Le module Blowfish déclare `module github.com/nunocoracao/blowfish/v2` dans son propre `go.mod` mais n'a pas de tags semver v2.x — résolu en utilisant `v2.100.0` (tag réel du repo)
- Blowfish v2.100.0 référence `_internal/opengraph.html` supprimé dans Hugo 0.148+ — résolu avec un shim `layouts/_internal/opengraph.html` qui délègue à notre partial custom

### 2. Configuration Hugo multilingue

**`config/_default/config.yaml`** — réécriture complète :
- `defaultContentLanguage: en`
- `defaultContentLanguageInSubdir: true` → URLs `/en/` et `/fr/`
- `languages.en.contentDir: content/en` et `languages.fr.contentDir: content/fr` (**clé critique** : sans `contentDir`, Hugo double-neste les URLs en `/en/en/post/`)
- Import du module Blowfish via `module.imports`
- Suppression : ancien `theme`, `menu`, `build.buildStats`, `services.googleAnalytics`

**Nouveaux fichiers de config créés :**

| Fichier | Contenu |
|---------|---------|
| `config/_default/params.toml` | Paramètres Blowfish (colorScheme, search, TOC, homepage profile, analytics GA) |
| `config/_default/languages.en.toml` | Auteur EN (nom, bio, liens sociaux) |
| `config/_default/languages.fr.toml` | Auteur FR (traductions) |
| `config/_default/menus.en.toml` | Navigation EN (Posts, Projects, Talks, About, Consulting) |
| `config/_default/menus.fr.toml` | Navigation FR (Articles, Projets, Conférences, À propos, Consulting) |

### 3. Réorganisation du contenu

Structure cible :
```
content/
├── en/
│   ├── post/       (54 posts EN)
│   ├── project/
│   ├── talk/
│   ├── positions/
│   └── page/       (about, search)
└── fr/
    └── post/       (9 posts FR)
```

**Posts FR identifiés** (champ `language: fr` en frontmatter) :
- `2017-08-23-je-parle-a-pycon-fr-2017.md`
- `2025-08-04-relancer-ecriture-livre-python-3-13.md`
- `2025-08-11-les-reves-de-baie-de-somme/`
- `2025-11-22-claude-code-retour-experience-pycon-ireland.md`
- `Formation Dev IA chez Alyra.md`
- `Génial, un bug fixé rapidement/`
- `Ce-que-je-fabrique-pendant-mes-vacances/`
- `Migration vers Hugo, réflexions et passage à Obsidian/`
- `Utilisation d'Obsidian comme source pour Hugo.md`

**Nettoyage frontmatter :** champ `lang:` (deprecated Hugo 0.144+) supprimé de 12 anciens posts EN.

**Fichiers `_index.md`** créés : `content/en/`, `content/fr/`, `content/en/post/`, `content/fr/post/`.

### 4. Layouts

**Supprimés** (remplacés par Blowfish natif) :
- `layouts/post/single.html`, `layouts/page/single.html`, `layouts/page/search.html`
- `layouts/project/single.html`, `layouts/talk/single.html`
- `layouts/position/single.html`, `layouts/position/list.html`
- `layouts/taxonomy/list.html`, `layouts/term/list.html`
- `layouts/404.html`
- `layouts/partials/header.html`, `footer.html`, `intro.html`
- `layouts/partials/google-analytics.html`, `extra-in-head.html`, `extra-in-foot.html`
- `layouts/partials/post-consulting-cta.html`, `post-content.html`, `post-footer.html`, `post-stub.html`
- `layouts/partials/project-footer.html`, `related-posts.html`, `talk-conferences.html`

**Conservés / créés :**

| Fichier | Rôle |
|---------|------|
| `layouts/partials/extend-head.html` | Hook Blowfish `<head>` — vide (Blowfish passe `.Site` comme contexte, pas la page) |
| `layouts/partials/extend-article-link.html` | Hook Blowfish post-article : JSON-LD BlogPosting + Breadcrumb + Consulting CTA |
| `layouts/partials/jsonld-*.html` | Partials JSON-LD conservés tels quels |
| `layouts/partials/opengraph.html` | Custom OG conservé |
| `layouts/_internal/opengraph.html` | Shim Hugo 0.148+ (voir §1) |
| `layouts/shortcodes/speakerdeck.html` | Conservé tel quel |
| `layouts/shortcodes/image.html` | Conservé tel quel |
| `assets/css/custom.css` | CSS custom (tag cloud, dark mode CTA) — migré depuis `static/css/` |

**Point d'attention — `extend-head.html`** : Blowfish appelle ce partial via `partialCached "extend-head.html" .Site`, donc le contexte est `.Site` (pas la page courante). Les JSON-LD page-spécifiques ont donc été déplacés dans `extend-article-link.html` qui reçoit bien le contexte page.

### 5. Build system

- **`netlify.toml`** : build simplifié (`hugo --gc --minify`), suppression de `npm install` + Pagefind, Hugo 0.148.0
- **`postcss.config.js`** : remplacé par un no-op (PurgeCSS était pour FontAwesome Ghostwriter)
- **`package.json`** : suppression des devDependencies PostCSS/PurgeCSS

### 6. `scripts/obsidian2hugo.py`

- `--language` / `--lang` option ajoutée (défaut : `en`)
- `target_path` devient optionnel, défaut calculé : `content/{language}/post`
- Le répertoire cible est créé automatiquement si absent
- Le champ `language:` est injecté dans le frontmatter si absent

Usage :
```bash
python scripts/obsidian2hugo.py <source> --language fr
# → écrit dans content/fr/post/
python scripts/obsidian2hugo.py <source> --language en
# → écrit dans content/en/post/
```

### 7. Correctifs divers

- `content/fr/post/2025-08-11-les-reves-de-baie-de-somme/index.md` : ajout de `{{< /gallery >}}` (Hugo 0.157 strict sur les shortcodes non fermés)

---

## État final

```
$ hugo --environment development --buildDrafts
Pages  │ EN: 228  │ FR: 79
Total in ~430 ms
```

Aucune erreur. Articles visibles sur `/en/` et `/fr/`.

---

## Ce qui reste à faire (optionnel)

- [ ] Profil homepage : ajouter `assets/img/avatar.png` pour la photo (Blowfish layout `profile`)
- [ ] JSON-LD homepage (WebSite + Person) : nécessite un override du template home, `extend-head.html` ne peut pas l'injecter (contexte `.Site` seulement)
- [ ] Page About FR (`content/fr/page/about/`)
- [ ] Redirects Netlify pour les anciennes URLs `/post/YYYY/MM/DD/slug` → `/en/post/slug/`
- [ ] Supprimer `static/css/custom.css` et `static/css/taxonomy.css` (remplacés par `assets/css/custom.css`)
- [ ] Supprimer le dossier `themes/` (thèmes locaux obsolètes, tout passe par Hugo Modules)
