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
from typing import Optional, Callable


def is_folder_note(path: pathlib.Path):
    return path.is_dir() and (path / "index.md").exists()


def ignore_folder_note(path, names):
    lpath = pathlib.Path(path)
    return [lpath.name]


def find_notes(parent_path: pathlib.Path) -> typing.Iterator[pathlib.Path]:
    for path in parent_path.glob("*"):
        if path.is_file() and path.suffix.lower() == ".md":
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

def parse_inner(inner: str) -> tuple[str, Optional[str], Optional[str], Optional[str]]:
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

def build_target_with_fragment(target: str, heading: Optional[str], block: Optional[str]) -> str:
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
    transform_target: Optional[Callable[[str], str]] = None,
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
):
    console = Console()
    for path, is_folder in find_notes(parent_path):
        path: pathlib.Path
        is_folder: bool
        # console.rule(f'Source: {path.relative_to(parent_path)}')
        if is_folder:
            markdown_document_path = path / "index.md"
        else:
            markdown_document_path = path

        document = fm.load(markdown_document_path, handler=YAML_HANDLER)

        # title = document.metadata['title']
        # date = parse_date(document.metadata['date'])

        # console.print(f'Date: {date}')
        # console.print(f'Title: {title}')

        print(f'{is_folder=} {path.name}')

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
            final_path.write_text(dumped_post, encoding="utf-8")
        else:
            directory_path = target_path / path.name
            final_path = directory_path / "index.md"
            directory_path.mkdir(exist_ok=True)
            shutil.copytree(
                path, directory_path, ignore=ignore_folder_note, dirs_exist_ok=True
            )
            final_path.write_text(dumped_post, encoding="utf-8")


        # console.rule(f"Target: {final_path.relative_to(target_path)}")


if __name__ == "__main__":
    typer.run(main)
