# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains Stéphane Wirtel's personal blog and CV. It uses Hugo static site generator with a custom theme and includes automated CV generation from TOML data.

**Key Components:**
- **Blog**: Hugo-based static site using the Ghostwriter theme
- **CV**: Generated from LaTeX templates populated with YAML/TOML data
- **Deployment**: Netlify for the blog, AWS S3 for CV PDF
- **Content Integration**: Python scripts to convert Obsidian notes to Hugo posts

## Development Commands

### Hugo Site (Blog)

```bash
# Serve the site locally with drafts
task serve
# OR
hugo server --environment development --buildDrafts

# Build the production site
task build:site
# OR
hugo --gc --minify

# Create a new post
task new:post -- "Post Title Here"
# OR
hugo new content content/post/YYYY-MM-DD-title
```

### CV Generation

```bash
# Full CV rebuild (generate .tex from template, then build PDF)
task cv:from-scratch

# Generate .tex file from template and data
task generate:cv

# Build PDF from existing .tex file
task build:cv
```

### Python Environment Setup

```bash
# Initialize virtual environment
task init

# Install uv (pip replacement)
task dep:bootstrap

# Install all dependencies
task dep:install

# Update dependencies
task dep:compile
```

**Note**: The Python virtual environment is located in `.venv/` directory. You can run tools directly with `.venv/bin/python` or `.venv/bin/TOOL` without activating the environment.

### Obsidian to Hugo Migration

```bash
# Convert Obsidian notes to Hugo posts
python scripts/obsidian2hugo.py <source-path> [target-path]
```

This script:
- Converts Obsidian wikilinks `[[Target|Alias]]` to Hugo relref shortcodes
- Handles folder notes (directories with index.md)
- Preserves frontmatter with YAML formatting
- Copies associated images/assets

## Architecture

### Content Structure

```
content/
├── post/          # Blog posts (date-based permalinks: /post/YYYY/MM/DD/slug)
├── project/       # Projects showcase
├── talk/          # Conference talks and presentations
├── positions/     # Employment history (used for CV generation)
├── page/          # Static pages (About, etc.)
└── drafts/        # Unpublished content
```

### Configuration

- **Main config**: `config/_default/config.yaml` - Site settings, author info, permalinks
- **Dev config**: `config/development/config.yaml` - Development overrides
- **Netlify**: `netlify.toml` - Hugo version 0.148.2, build commands
- **Theme**: Dual theme setup: `original-ghostwriter` + `hugo-shortcode-gallery`

### CV Generation Pipeline

1. **Data sources**:
   - `content/positions/` - Employment history (frontmatter)
   - `content/talk/` - Conference talks (frontmatter)
   - `data/conferences.yml` - Conference metadata
   - `config/_default/config.yaml` - Personal info
   - `details.toml` - Additional CV details

2. **Template rendering**: `scripts/generate-cv.py` uses Jinja2 with custom delimiters (`[[var]]`, `[% block %]`) to render `templates/TemplateCV.tex`

3. **PDF compilation**: LaTeX (pdflatex) compiles the .tex file to PDF

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
├── partials/      # Reusable template components
├── post/          # Blog post layout overrides
├── project/       # Project page layouts
├── talk/          # Talk page layouts
├── position/      # Position page layouts
└── shortcodes/    # Custom Hugo shortcodes
```

## Important Notes

### Hugo Specifics
- Uses Go modules for theme management (`go.mod`)
- Permalinks for posts: `/post/:year/:month/:day/:slug`
- Main sections: `post` (shown on homepage)
- Google Analytics enabled (ID: G-BC0WC3PWS6)

### Docker Usage
- Old Makefile uses Docker for Hugo and LaTeX
- **Current workflow uses Task and native tools** - prefer Task commands over Docker

### Python Dependencies
- Virtual environment located in `.venv/` (run tools directly with `.venv/bin/python` or `.venv/bin/TOOL`)
- Managed via `uv` (faster pip alternative)
- Requirements defined in `scripts/requirements.in`
- Locked in `scripts/requirements.txt`
- Key deps: frontmatter, jinja2, pyyaml, pendulum, typer, awscli

### Deployment
- **Blog**: Netlify auto-deploys from `main` branch
- **CV**: GitHub Actions runs daily cron job to build and upload to S3
- Status badge: [![Netlify Status](https://api.netlify.com/api/v1/badges/c67c87b3-bc74-4667-b63f-d235ae5516fd/deploy-status)](https://app.netlify.com/sites/stephane-wirtel/deploys)
- Never mention Claude or Claude Code in your commits