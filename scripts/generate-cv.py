#!/usr/bin/env python
import pathlib

import yaml
from jinja2 import Environment, FileSystemLoader
from yaml import SafeLoader
import argparse

import frontmatter
import pendulum
from extract_frontmatters import PositionLoader

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('template')
    parser.add_argument('output')

    return parser.parse_args()


def main():
    args = parse_args()

    template = pathlib.Path(args.template)

    position_loader = PositionLoader('content/positions')
    position_loader.load()

    env = Environment(
        variable_start_string='[[', variable_end_string=']]',
        block_start_string='[%', block_end_string='%]',
        loader=FileSystemLoader(template.parent),
        autoescape=False
    )
    env.globals.update(position_loader=position_loader)
    template = env.get_template(template.name)
    with pathlib.Path('config.yaml').open() as fp:
        config = yaml.load(fp, Loader=SafeLoader)
    content = template.render(config=config)
    pathlib.Path(args.output).write_text(content)


if __name__ == '__main__':
    main()
