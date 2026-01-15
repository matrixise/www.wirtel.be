import datetime
import typer
import typing
import pathlib
import shutil
import frontmatter as fm
from rich.pretty import pprint
from rich.console import Console
from slugify import slugify
from ruamel.yaml import YAML
import io
from typing import Optional
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Note:
    """Représente une note Obsidian avec ses métadonnées."""
    path: pathlib.Path                    # Chemin source (fichier ou dossier)
    is_folder: bool                       # True si folder note
    markdown_document_path: pathlib.Path  # Chemin du fichier .md à lire
    document: fm.Post | None = None       # Document frontmatter (None si pas encore chargé)


def is_folder_note(path: pathlib.Path):
    return path.is_dir() and (path / "index.md").exists()


def ignore_folder_note(path, names):
    lpath = pathlib.Path(path)
    return [lpath.name]


def find_notes(parent_path: pathlib.Path) -> typing.Iterator[Note]:
    """Découvre toutes les notes Markdown dans un répertoire.

    Retourne des objets Note sans document chargé (document=None).
    """
    for path in parent_path.glob("*"):
        if path.is_file() and path.suffix.lower() == ".md":
            # Ignore CLAUDE.md files (Claude Code configuration)
            if path.name == "CLAUDE.md":
                continue
            markdown_path = path
            yield Note(path=path, is_folder=False, markdown_document_path=markdown_path)
        elif is_folder_note(path):
            markdown_path = path / "index.md"
            yield Note(path=path, is_folder=True, markdown_document_path=markdown_path)


def load_documents(
    notes: typing.Iterator[Note],
    console: Console,
    errors: list[tuple[pathlib.Path, Exception | str]]
) -> typing.Iterator[Note]:
    """Charge les documents frontmatter pour chaque note.

    Gestion d'erreur: Les notes avec erreur de parsing YAML sont loggées
    dans errors[] et skippées (pas yieldées).
    """
    for note in notes:
        try:
            document = fm.load(note.markdown_document_path, handler=YAML_HANDLER)
            # Créer une nouvelle Note avec le document chargé
            yield Note(
                path=note.path,
                is_folder=note.is_folder,
                markdown_document_path=note.markdown_document_path,
                document=document
            )
        except Exception as e:
            console.print(f"\n[bold red]❌ YAML Parse Error:[/bold red]", style="red")
            console.print(f"   File: [bold]{note.markdown_document_path}[/bold]")
            console.print(f"   Error: {str(e)[:200]}")
            errors.append((note.markdown_document_path, e))
            # Skip cette note (pas de yield)
            continue


def validate_notes(
    notes: typing.Iterator[Note],
    console: Console,
    errors: list[tuple[pathlib.Path, Exception | str]]
) -> typing.Iterator[Note]:
    """Valide que chaque note a un titre dans les métadonnées.

    Gestion d'erreur: Les notes sans titre sont loggées dans errors[]
    et skippées (pas yieldées).
    """
    for note in notes:
        if note.document is None:
            # Sécurité: ne devrait jamais arriver si load_documents() a été appelé
            console.print(f"\n[bold red]❌ Internal Error:[/bold red]", style="red")
            console.print(f"   File: [bold]{note.markdown_document_path}[/bold]")
            console.print("   Document not loaded")
            errors.append((note.markdown_document_path, "Document not loaded"))
            continue

        if "title" not in note.document.metadata:
            console.print(f"\n[bold red]❌ Missing Title:[/bold red]", style="red")
            console.print(f"   File: [bold]{note.markdown_document_path}[/bold]")
            errors.append((note.markdown_document_path, "Missing 'title' field"))
            continue

        yield note


def transform_note(note: Note) -> Note:
    """Applique les transformations à une note: slug, wikilinks, image embed.

    Retourne une nouvelle Note avec le document modifié.
    """
    document = note.document
    assert document is not None, "Document should be loaded"

    # 1. Compute/set slug
    computed_slug = slugify(document.metadata["title"])
    slug = document.metadata.get("slug", computed_slug)
    document.metadata["slug"] = slug

    # 2. Convert image embed syntax
    if (image := document.metadata.get("image")) and image.startswith("![[") and image.endswith("]]"):
        document.metadata["image"] = image[3:-2]

    # 3. Convert wikilinks to relref
    converted_content = convert_wikilinks_to_relref(document.content)
    transformed_document = fm.Post(converted_content, **document.metadata)

    return Note(
        path=note.path,
        is_folder=note.is_folder,
        markdown_document_path=note.markdown_document_path,
        document=transformed_document
    )


def write_note(
    note: Note,
    target_path: pathlib.Path,
    force: bool,
    console: Console,
    skipped: list[str],
    errors: list[tuple[pathlib.Path, Exception | str]]
) -> None:
    """Écrit une note transformée dans le répertoire cible.

    Gère les cas fichier simple vs folder note, et le flag --force.
    """
    try:
        dumped_post = fm.dumps(note.document, handler=YAML_HANDLER)

        if not note.is_folder:
            # Fichier simple
            final_path = target_path / note.path.name
            if final_path.exists() and not force:
                console.print(f"⏭️  Skipping existing file: {note.path.name}", style="yellow")
                skipped.append(note.path.name)
                return
            final_path.write_text(dumped_post, encoding="utf-8")
        else:
            # Folder note
            directory_path = target_path / note.path.name
            final_path = directory_path / "index.md"
            if directory_path.exists() and not force:
                console.print(f"⏭️  Skipping existing directory: {note.path.name}", style="yellow")
                skipped.append(note.path.name)
                return
            directory_path.mkdir(exist_ok=True)
            shutil.copytree(
                note.path, directory_path, ignore=ignore_folder_note, dirs_exist_ok=True
            )
            final_path.write_text(dumped_post, encoding="utf-8")
    except Exception as e:
        console.print(f"\n[bold red]❌ Processing Error:[/bold red]", style="red")
        console.print(f"   File: [bold]{note.markdown_document_path}[/bold]")
        console.print(f"   Error: {str(e)[:200]}")
        errors.append((note.markdown_document_path, e))


def parse_date(value) -> datetime.datetime:
    """Parse une date et retourne un datetime naive (sans timezone)."""
    result = None

    if isinstance(value, datetime.datetime):
        result = value
    elif isinstance(value, datetime.date):
        result = datetime.datetime(value.year, value.month, value.day)
    elif isinstance(value, str):
        # essais classiques + fallback ISO
        fmts = ("%Y-%m-%d",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S%z")
        for f in fmts:
            try:
                result = datetime.datetime.strptime(value, f)
                break
            except ValueError:
                pass
        if result is None:
            result = datetime.datetime.fromisoformat(value)
    else:
        raise TypeError(f"Unsupported date type: {type(value)!r}")

    # Normaliser en naive (sans timezone) pour permettre les comparaisons
    if result.tzinfo is not None:
        result = result.replace(tzinfo=None)

    return result

class RuamelYAMLHandler(fm.YAMLHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.yaml = YAML()
        self.yaml.preserve_quotes = True

    def load(self, fm, **kwargs):
        return self.yaml.load(fm)

    def export(self, metadata, **kwargs):
        s = io.StringIO()
        self.yaml.dump(metadata, s)
        return s.getvalue()

YAML_HANDLER = RuamelYAMLHandler()


ParentPath = typing.Annotated[
    pathlib.Path,
    typer.Argument(exists=True, file_okay=True, dir_okay=True),
]

TargetPath = typing.Annotated[
    pathlib.Path,
    typer.Argument(
        exists=True,
        dir_okay=True
    ),
]

import re
from dataclasses import dataclass
WIKILINK_RE = re.compile(r'(!?)\[\[([^\]]+)\]\]')

@dataclass
class WikiLink:
    raw: str
    is_embed: bool
    target: str
    alias: str | None
    heading: str | None
    block: str | None

def parse_inner(inner: str) -> tuple[str, str | None, str | None, str | None]:
    """
    inner = 'Target|Alias' ou 'Target#Heading' ou 'Target^block'
    Retourne (target, alias, heading, block)
    """
    alias = heading = block = None

    # On sépare alias si présent
    if "|" in inner:
        left, alias = inner.split("|", 1)
    else:
        left = inner

    # Gestion heading/block sur la partie gauche
    if "#" in left:
        target, heading = left.split("#", 1)
    elif "^" in left:
        target, block = left.split("^", 1)
    else:
        target = left

    return target.strip(), (alias or None), (heading or None), (block or None)

def build_target_with_fragment(target: str, heading: str | None, block: str | None) -> str:
    """
    Construit la cible finale pour relref, en conservant l'ancre si fournie.
    Pour les block ids (^xyz), on les mappe en fragment '#^xyz' (Hugo peut
    gérer un fragment si tu l’utilises côté rendu).
    """
    if heading:
        return f"{target}#{heading}"
    if block:
        return f"{target}#^{block}"
    return target

def convert_wikilinks_to_relref(
    text: str,
    *,
    transform_target: Callable[[str], str] | None = None,
    use_markdown_link_syntax: bool = False,
) -> str:
    """
    Remplace les wikilinks texte par des relref Hugo.

    - Par défaut (conforme à ton exemple) :
        [[Titre|Alias]] -> [Alias]{{% relref "Titre" $}}
        [[Titre]]       -> [Titre]{{% relref "Titre" $}}

    - Si use_markdown_link_syntax=True, utilise la forme :
        [Alias]({{< relref "Titre" >}})
      (plus classique en Hugo, mais tu as explicitement demandé la variante sans parenthèses)

    - transform_target(target) te permet de mapper 'Titre' vers un chemin Hugo
      (ex: slugify, 'blog/...' etc.)
    """
    def _repl(m: re.Match) -> str:
        bang, inner = m.group(1), m.group(2)
        is_embed = bool(bang)
        # On ignore les embeds ![[...]] (images/attachments)
        if is_embed:
            return m.group(0)

        target, alias, heading, block = parse_inner(inner)
        final_target = build_target_with_fragment(target, heading, block)
        if transform_target:
            final_target = transform_target(final_target)

        label = (alias or target).strip()

        if use_markdown_link_syntax:
            # Variante classique : [label]({{< relref "path" >}})
            return f'[{label}]({{< relref "{final_target}" >}})'
        else:
            # Variante demandée : [label]{{% relref "path" $}}
            return f'[{label}]({{{{< relref "{final_target}" >}}}})'

    return WIKILINK_RE.sub(_repl, text)


def main(
    parent_path: ParentPath,
    target_path: TargetPath = pathlib.Path('content/post'),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing files in target directory"),
):
    console = Console()
    errors: list[tuple[pathlib.Path, Exception | str]] = []
    skipped: list[str] = []

    # Phase 1: Pipeline LAZY (streaming)
    pipeline = validate_notes(
        load_documents(
            find_notes(parent_path),
            console,
            errors
        ),
        console,
        errors
    )

    # Phase 2: MATÉRIALISATION + TRI par date
    validated_notes = list(pipeline)
    validated_notes.sort(
        key=lambda n: parse_date(n.document.metadata.get('date', datetime.datetime.min))
    )

    # Phase 3: TRAITEMENT FINAL (transformation + écriture)
    for note in validated_notes:
        transformed_note = transform_note(note)
        write_note(transformed_note, target_path, force, console, skipped, errors)

    # Print summary
    console.print("\n" + "="*80)
    if errors:
        console.print(f"\n[bold yellow]⚠️  Migration completed with {len(errors)} error(s)[/bold yellow]")
        console.print("\n[yellow]Files that failed:[/yellow]")
        for path, error in errors:
            console.print(f"  • {path.name}")

    if skipped:
        console.print(f"\n[bold yellow]⏭️  Skipped {len(skipped)} existing file(s)[/bold yellow]")
        console.print("\n[yellow]Files that were skipped (use --force to overwrite):[/yellow]")
        for name in skipped:
            console.print(f"  • {name}")

    if not errors and not skipped:
        console.print("\n[bold green]✅ Success! All files migrated successfully.[/bold green]")
    elif not errors:
        console.print("\n[bold green]✅ Migration completed successfully.[/bold green]")


if __name__ == "__main__":
    typer.run(main)
