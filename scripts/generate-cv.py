#!/usr/bin/env python
import pathlib
from typing import Annotated

import typer
import yaml
from jinja2 import Environment, FileSystemLoader
from yaml import SafeLoader

from extract_frontmatters import PositionLoader, TalkLoader, Conferences


def main(
    template: Annotated[
        pathlib.Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Path to the LaTeX template file (Jinja2 format)",
        ),
    ],
    output: Annotated[
        typer.FileTextWrite,
        typer.Argument(
            help="Output .tex file path to generate",
        ),
    ],
) -> None:
    """
    Generate LaTeX CV from template and content data.

    Loads position data, talk data, and conference information from the Hugo
    content directory and renders a LaTeX CV using Jinja2 templating.
    """
    try:
        content_dir = pathlib.Path('content')
        position_loader = PositionLoader(content_dir / 'positions')
        position_loader.load()

        talk_loader = TalkLoader(content_dir / 'talk')
        talk_loader.load()

        conferences = Conferences.load('data/conferences.yml')

        # Load profile data (skills, memberships, interests, sports, python_contribs)
        with pathlib.Path('data/profile.yml').open() as fp:
            profile = yaml.load(fp, Loader=SafeLoader)

        env = Environment(
            variable_start_string='[[', variable_end_string=']]',
            block_start_string='[%', block_end_string='%]',
            loader=FileSystemLoader(template.parent),
            autoescape=False
        )
        env.globals.update(
            position_loader=position_loader,
            talk_loader=talk_loader,
            conferences=conferences,
            profile=profile
        )

        def split_filter(value: str, separator: str ='/') -> list[str]:
            return [v for v in value.split(separator) if v]

        env.filters['split'] = split_filter

        jinja_template = env.get_template(template.name)
        with pathlib.Path('config/_default/config.yaml').open() as fp:
            config = yaml.load(fp, Loader=SafeLoader)
        content = jinja_template.render(config=config)

        output.write(content)
        typer.echo(f"✓ Successfully generated CV: {output.name}")

    except FileNotFoundError as e:
        typer.echo(f"Error: File not found - {e}", err=True)
        raise typer.Exit(code=1)
    except yaml.YAMLError as e:
        typer.echo(f"Error: Failed to parse YAML - {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


if __name__ == '__main__':
    typer.run(main)
