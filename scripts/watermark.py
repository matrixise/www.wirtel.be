#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import List, Optional
import platform

import typer
from PIL import Image, ImageDraw, ImageFont

app = typer.Typer(add_completion=False, help="Ajoute un texte en bas à droite sur des images.")

# --- Chargement de la police ---
def _load_font(font_path: Optional[Path], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if font_path and Path(font_path).exists():
        return ImageFont.truetype(str(font_path), size=size)

    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", size=size)
        elif system == "Windows":
            return ImageFont.truetype("arial.ttf", size=size)
        else:  # Linux
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=size)
    except Exception:
        return ImageFont.load_default()

# --- Calcul taille texte ---
def _text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont):
    try:
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        return right - left, bottom - top
    except Exception:
        return draw.textsize(text, font=font)

# --- Application watermark ---
def _watermark_image(
    img: Image.Image,
    text: str,
    font: ImageFont.ImageFont,
    margin_x: int,
    margin_y: int,
    stroke_width: int,
    fill: str,
    stroke_fill: str,
) -> Image.Image:
    im = img.convert("RGBA")
    layer = Image.new("RGBA", im.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(layer)

    tw, th = _text_size(draw, text, font)
    x = im.width - tw - margin_x
    y = im.height - th - margin_y

    draw.text(
        (x, y),
        text,
        font=font,
        fill=fill,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )
    return Image.alpha_composite(im, layer)

# --- Génération nom sortie ---
def _out_path(src: Path, output_dir: Optional[Path]) -> Path:
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / src.name
    stem = src.stem + "_credits"
    ext = src.suffix if src.suffix else ".jpg"
    return src.with_name(stem + ext)

# --- Commande Typer ---
@app.command("add")
def add_text(
    files: List[Path] = typer.Argument(..., exists=True, readable=True, help="Fichiers image à traiter"),
    text: str = typer.Option(..., "--text", "-t", help='Texte à apposer (ex: "Crédits: Les Rêves de Baie de Somme")'),
    font_path: Optional[Path] = typer.Option(None, "--font", help="Chemin vers une police .ttf/.otf"),
    size: int = typer.Option(24, "--size", "-s", help="Taille de police"),
    margin_x: int = typer.Option(12, "--margin-x", help="Marge horizontale depuis le bord droit (px)"),
    margin_y: int = typer.Option(12, "--margin-y", help="Marge verticale depuis le bord bas (px)"),
    fill: str = typer.Option("white", "--fill", help="Couleur du texte"),
    stroke_width: int = typer.Option(2, "--stroke-width", help="Épaisseur du contour"),
    stroke_fill: str = typer.Option("black", "--stroke-fill", help="Couleur du contour"),
    output_dir: Optional[Path] = typer.Option(None, "--out-dir", "-o", help="Dossier de sortie"),
    overwrite: bool = typer.Option(False, "--overwrite", help="Écraser les fichiers existants"),
):
    """
    Ajoute un texte en bas à droite de chaque image listée.
    """
    font = _load_font(font_path, size)
    errors = 0

    for src in files:
        try:
            with Image.open(src) as im:
                out_img = _watermark_image(im, text, font, margin_x, margin_y, stroke_width, fill, stroke_fill)
                dst = _out_path(src, output_dir)

                if dst.exists() and not overwrite:
                    typer.echo(f"[SKIP] {dst} existe déjà (utilisez --overwrite pour écraser).")
                    continue

                fmt = im.format or "PNG"
                if fmt.upper() in {"JPEG", "JPG"}:
                    out_img = out_img.convert("RGB")
                    fmt = "JPEG"

                out_img.save(dst, format=fmt)
                typer.echo(f"[OK] {src} -> {dst}")
        except Exception as e:
            errors += 1
            typer.echo(f"[ERR] {src}: {e}")

    if errors:
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
