#!/usr/bin/env bash
set -euo pipefail

# Vérification arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 <fichier1> [fichier2 ...]"
    exit 1
fi

# Dossier de sortie
OUTDIR="out"
mkdir -p "$OUTDIR"

# Police par défaut (macOS, à adapter si besoin)
FONT="/System/Library/Fonts/Supplemental/Arial.ttf"

# Boucle sur tous les fichiers passés en argument
for f in "$@"; do
    if [ ! -f "$f" ]; then
        echo "⏭️  SKIP: $f (pas un fichier)"
        continue
    fi

    uuid=$(uuidgen)  # Génère un nom unique

    magick "$f" -auto-orient \
        -resize '2048x2048>' \
        -font "$FONT" -pointsize 32 \
        -fill white \
        -gravity southeast -annotate +20+20 "Crédits: Stéphane Wirtel & Anne Stévenne" \
        -strip -quality 100 -interlace JPEG \
        "$OUTDIR/$uuid.jpg"

    echo "✅ $f -> $OUTDIR/$uuid.jpg"
done
