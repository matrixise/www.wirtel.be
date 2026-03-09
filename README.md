# wirtel.be

Personal blog and CV of Stéphane Wirtel. Built with Hugo and deployed on Netlify.

## Project Overview

**Key Components:**
- **Blog**: Hugo-based static site using the Ghostwriter theme
- **Search**: Full-text search powered by Pagefind
- **CV**: Generated from LaTeX templates populated with YAML/TOML data
- **Deployment**: Netlify for the blog, AWS S3 for CV PDF
- **Content Integration**: Python scripts to convert Obsidian notes to Hugo posts

[![Netlify Status](https://api.netlify.com/api/v1/badges/c67c87b3-bc74-4667-b63f-d235ae5516fd/deploy-status)](https://app.netlify.com/sites/stephane-wirtel/deploys)

## Requirements

- [Hugo](https://gohugo.io/) >= 0.152.2 (extended)
- [Task](https://taskfile.dev/) (task runner)
- Python >= 3.10 (for CV generation and scripts)
- LaTeX / pdflatex (for CV PDF compilation)
- Node.js / npx (for Pagefind indexing)

## Development Commands

### Hugo Site (Blog)

```bash
# Serve the site locally with drafts (builds Pagefind index first)
task serve

# Build the production site (Hugo + Pagefind index)
task build:site

# Create a new post
task new:post -- "Post Title Here"
```

The `serve` task:
1. Builds the site with drafts enabled
2. Runs Pagefind to generate the local search index into `static/pagefind/`
3. Starts the Hugo development server

The `build:site` task runs `hugo --gc --minify` then indexes the output with Pagefind.

The Netlify production build command is:
```
hugo --gc --minify && npx -y pagefind --site public --glob "post/**/*.html"
```

### CV Generation

```bash
# Rebuild the CV from scratch (generate .tex + compile PDF)
task local:cv:rebuild

# Generate the .tex file from template and data
task local:cv:generate-tex

# Compile the .tex file to PDF using pdflatex
task local:cv:build-pdf

# Upload the CV PDF to AWS S3
task s3:cv:upload

# Trigger CV build on GitHub Actions
task github:cv:build
```

### Python Environment Setup

```bash
# Initialize virtual environment
task init

# Install uv (pip replacement)
task dep:bootstrap

# Install all dependencies
task dep:install

# Compile locked dependencies from requirements.in
task dep:compile

# Upgrade and recompile all dependencies
task dep:upgrade
```

The Python virtual environment is located in `.venv/`. You can run tools directly without activating it:

```bash
.venv/bin/python scripts/generate-cv.py ...
```

### Obsidian to Hugo Migration

```bash
# Convert Obsidian notes to Hugo posts
task migrate:obsidian OBSIDIAN_VAULT_PATH=/path/to/vault
# OR directly:
python scripts/obsidian2hugo.py <source-path> [target-path]
```

This script:
- Converts Obsidian wikilinks `[[Target|Alias]]` to Hugo relref shortcodes
- Handles folder notes (directories with index.md)
- Preserves frontmatter with YAML formatting
- Copies associated images/assets

### Repository Maintenance

```bash
# Clean untracked files (safe — respects .gitignore)
task clean

# Clean ALL untracked files including ignored ones (⚠️  DANGEROUS)
# Will delete .envrc, .venv/, and all ignored files — prompts for confirmation
task clean:all
```

## Architecture

### Content Structure

```
content/
├── post/          # Blog posts (date-based permalinks: /post/YYYY/MM/DD/slug)
├── project/       # Projects showcase
├── talk/          # Conference talks and presentations
├── positions/     # Employment history (used for CV generation)
├── page/          # Static pages (About, Search, etc.)
└── drafts/        # Unpublished content
```

### Configuration

- **Main config**: `config/_default/config.yaml` — Site settings, author info, permalinks
- **Dev config**: `config/development/config.yaml` — Development overrides
- **Netlify**: `netlify.toml` — Hugo version 0.152.2, build commands, security headers
- **Theme**: Dual theme setup: `original-ghostwriter` + `hugo-shortcode-gallery`

### Frontend Assets

FontAwesome 6 is self-hosted (no external CDN). Only the solid and brands subsets are included to keep the payload small. The files live in `static/vendor/fontawesome/`.

Google Analytics is loaded via Hugo's built-in template. The analytics script is deferred until the browser is idle using `requestIdleCallback`.

### CV Generation Pipeline

1. **Data sources**:
   - `content/positions/` — Employment history (frontmatter)
   - `content/talk/` — Conference talks (frontmatter)
   - `data/conferences.yml` — Conference metadata
   - `config/_default/config.yaml` — Personal info
   - `details.toml` — Additional CV details

2. **Template rendering**: `scripts/generate-cv.py` uses Jinja2 with custom delimiters (`[[var]]`, `[% block %]`) to render `templates/TemplateCV.tex`

3. **PDF compilation**: LaTeX (pdflatex) compiles the .tex file to PDF (run twice for correct cross-references)

4. **Deployment**: GitHub Actions runs daily, uploads PDF to S3

### Custom Scripts

- **`scripts/obsidian2hugo.py`**: Migrates Obsidian notes to Hugo, converting wikilinks to relref shortcodes
- **`scripts/generate-cv.py`**: Generates LaTeX CV from templates and content
- **`scripts/extract_frontmatters.py`**: Extracts frontmatter data from positions, talks, and conferences
- **`scripts/watermark.py`**: Adds watermarks to images

### Layouts and Customization

Hugo layouts override theme defaults:

```
layouts/
├── partials/      # Reusable template components (header, footer, JSON-LD, OG, etc.)
├── post/          # Blog post layout overrides
├── project/       # Project page layouts
├── talk/          # Talk page layouts
├── position/      # Position page layouts
├── page/          # Static page layouts (search, about)
└── shortcodes/    # Custom Hugo shortcodes
```

Structured data (JSON-LD) partials are included for `Person`, `WebSite`, `BlogPosting`, `FAQPage`, and `BreadcrumbList` schemas.

## Important Notes

### Hugo Specifics
- Uses Go modules for theme management (`go.mod`)
- Hugo version: **0.152.2** (defined in `netlify.toml` and `go.mod`)
- Permalinks for posts: `/post/:year/:month/:day/:slug`
- Main sections: `post` (shown on homepage)
- Google Analytics enabled (ID: G-BC0WC3PWS6)
- `CLAUDE.md` is excluded from Hugo processing via `ignoreFiles` in `config.yaml`

### Python Dependencies
- Virtual environment located in `.venv/` (run tools directly with `.venv/bin/python` or `.venv/bin/TOOL`)
- Managed via `uv` (faster pip alternative)
- Requirements defined in `scripts/requirements.in`
- Locked in `scripts/requirements.txt`
- Key deps: frontmatter, jinja2, pyyaml, pendulum, typer, awscli

### Deployment
- **Blog**: Netlify auto-deploys from `main` branch
- **CV**: GitHub Actions runs daily cron job to build and upload to S3
- Security headers (X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy) are set via `netlify.toml`
