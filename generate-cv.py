#!/usr/bin/env python
import pathlib

import yaml
from jinja2 import Environment, FileSystemLoader
from yaml import SafeLoader


def main():
    env = Environment(variable_start_string='[[', variable_end_string=']]',
                      loader=FileSystemLoader('layouts'),
                      autoescape=False)
    template = env.get_template('TemplateCV.tex')
    with pathlib.Path('config.yaml').open() as fp:
        config = yaml.load(fp, Loader=SafeLoader)
    content = template.render(config=config)
    pathlib.Path('StephaneWirtel.tex').write_text(content)


if __name__ == '__main__':
    main()
