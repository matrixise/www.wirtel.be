#!/usr/bin/env python
import pathlib

import yaml
from jinja2 import Environment, FileSystemLoader
from yaml import SafeLoader
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--template')
    parser.add_argument('--output')

    return parser.parse_args()

def main():
    args = parse_args()

    env = Environment(variable_start_string='[[', variable_end_string=']]',
                      loader=FileSystemLoader('templates'),
                      autoescape=False)
    template = env.get_template(args.template)
    with pathlib.Path('config.yaml').open() as fp:
        config = yaml.load(fp, Loader=SafeLoader)
    content = template.render(config=config)
    pathlib.Path(args.output).write_text(content)


if __name__ == '__main__':
    main()
