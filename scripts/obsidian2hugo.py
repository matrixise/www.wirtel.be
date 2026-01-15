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


def is_folder_note(path: pathlib.Path):
    return path.is_dir() and (path / "index.md").exists()


def ignore_folder_note(path, names):
    lpath = pathlib.Path(path)
    return [lpath.name]


def find_notes(parent_path: pathlib.Path) -> typing.Iterator[pathlib.Path]:
    for path in parent_path.glob("*"):
        if path.is_file() and path.suffix.lower() == ".md":
            # Ignore CLAUDE.md files (Claude Code configuration)
            if path.name == "CLAUDE.md":
                continue
            yield path, False
        elif is_folder_note(path):
            yield path, True

def parse_date(value) -> datetime.datetime:
    if isinstance(value, datetime.datetime):
        return value
    if isinstance(value, datetime.date):
        return datetime.datetime(value.year, value.month, value.day)
    if isinstance(value, str):
        # essais classiques + fallback ISO
        fmts = ("%Y-%m-%d",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S%z")
        for f in fmts:
            try:
                return datetime.datetime.strptime(value, f)
            except ValueError:
                pass
        return datetime.datetime.fromisoformat(value)
    raise TypeError(f"Unsupported date type: {type(value)!r}")

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

# --- Conversion principale ---

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
    errors = []
    skipped = []

    for path, is_folder in find_notes(parent_path):
        path: pathlib.Path
        is_folder: bool
        # console.rule(f'Source: {path.relative_to(parent_path)}')
        if is_folder:
            markdown_document_path = path / "index.md"
        else:
            markdown_document_path = path

        try:
            document = fm.load(markdown_document_path, handler=YAML_HANDLER)
        except Exception as e:
            console.print(f"\n[bold red]❌ YAML Parse Error:[/bold red]", style="red")
            console.print(f"   File: [bold]{markdown_document_path}[/bold]")
            console.print(f"   Error: {str(e)[:200]}")
            errors.append((markdown_document_path, e))
            continue

        try:
            # title = document.metadata['title']
            # date = parse_date(document.metadata['date'])

            # console.print(f'Date: {date}')
            # console.print(f'Title: {title}')

            print(f'{is_folder=} {path.name}')

            if "title" not in document.metadata:
                console.print(f"\n[bold red]❌ Missing Title:[/bold red]", style="red")
                console.print(f"   File: [bold]{markdown_document_path}[/bold]")
                errors.append((markdown_document_path, "Missing 'title' field"))
                continue

            computed_slug = slugify(document.metadata["title"])
            slug = document.metadata.get("slug", computed_slug)
            document.metadata["slug"] = slug

            if (
                (image := document.metadata.get("image"))
                and image.startswith("![[")
                and image.endswith("]]")
            ):
                document.metadata["image"] = image[3:-2]

            # slug_path = f"{date.strftime('%Y-%m-%d')}-{slug}"

            content = convert_wikilinks_to_relref(document.content)
            post = fm.Post(content, **document.metadata)

            dumped_post = fm.dumps(post, handler=YAML_HANDLER)

            if not is_folder:
                final_path = target_path / path.name
                if final_path.exists() and not force:
                    console.print(f"⏭️  Skipping existing file: {path.name}", style="yellow")
                    skipped.append(path.name)
                    continue
                final_path.write_text(dumped_post, encoding="utf-8")
            else:
                directory_path = target_path / path.name
                final_path = directory_path / "index.md"
                if directory_path.exists() and not force:
                    console.print(f"⏭️  Skipping existing directory: {path.name}", style="yellow")
                    skipped.append(path.name)
                    continue
                directory_path.mkdir(exist_ok=True)
                shutil.copytree(
                    path, directory_path, ignore=ignore_folder_note, dirs_exist_ok=True
                )
                final_path.write_text(dumped_post, encoding="utf-8")

            # console.rule(f"Target: {final_path.relative_to(target_path)}")
        except Exception as e:
            console.print(f"\n[bold red]❌ Processing Error:[/bold red]", style="red")
            console.print(f"   File: [bold]{markdown_document_path}[/bold]")
            console.print(f"   Error: {str(e)[:200]}")
            errors.append((markdown_document_path, e))
            continue

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
