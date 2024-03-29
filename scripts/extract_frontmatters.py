import frontmatter
import pendulum
import pathlib
import markdown
import mdx_latex
from pydantic import BaseModel
from typing import List
from pydantic_yaml import parse_yaml_raw_as

class PositionLoader:
    def __init__(self, directory: pathlib.Path):
        if isinstance(directory, str):
            directory = pathlib.Path(directory)
        self.directory = directory
        self.positions = []

    def get_current_positions(self):
        return [pos for pos in self.positions if pos['current']]

    def get_positions(self):
        return self.positions

    def get_other_positions(self):
        return [pos for pos in self.positions if not pos['current']]

    def load(self):
        positions = []

        for position_file in self.directory.glob('*.md'):
            position = frontmatter.load(position_file)
            if position.get('ignore'):
                continue
            position = self.format_position(position)
            positions.append(position)

        positions.sort(key=lambda position: position['stop-on'], reverse=True)
        self.positions = positions

    def format_position(self, position):
        position['start-on'] = pendulum.from_format(position['start-on'], 'YYYY/MM').date()
        try:
            position['stop-on'] = pendulum.from_format(position['stop-on'], 'YYYY/MM').date()
            position['current'] = False
        except KeyError:
            position['stop-on'] = pendulum.today('Europe/Brussels').end_of('month').date()
            position['current'] = True

        md = markdown.Markdown()
        latex_mdx = mdx_latex.LaTeXExtension()
        latex_mdx.extendMarkdown(md)
        out = md.convert(position.content)
        position.content = out.replace('<root>', '').replace('</root>', '').strip()
        return position

class TalkLoader:
    def __init__(self, directory: pathlib.Path):
        if isinstance(directory, str):
            directory = pathlib.Path(directory)
        self.directory = directory
        self.talks = []

    def load(self):
        talks = []

        for talk_file in self.directory.glob('*.md'):
            talk = frontmatter.load(talk_file)
            talks.append(talk)

        talks.sort(key=lambda obj: obj['date'], reverse=True)
        self.talks = talks


class ConferenceModel(BaseModel):
    years: List[int] = []
    positions: List[str] = []
    name: str

    @property
    def formatted_positions(self):
        return ', '.join(sorted(self.positions))

    @property
    def formatted_years(self):
        return ', '.join(map(str, sorted(self.years)))

    @property
    def title(self):
        if self.years:
            return f'{self.name} - {self.formatted_years}'
        return self.name



class Conferences(BaseModel):
    Conferences: List[ConferenceModel] = []

    @classmethod
    def load(cls, conference_file):
        return parse_yaml_raw_as(Conferences, pathlib.Path(conference_file).read_text())

def main():
    # loader = PositionLoader(pathlib.Path('content/positions'))
    # loader.load()
    # for position in loader.get_positions():
    #     print(f"{position['start-on']} {position['stop-on']} {position['title']}")

    # print(loader.get_current_positions())

    # loader = TalkLoader(pathlib.Path('content/talk'))
    # loader.load()

    # for talk in loader.talks:
    #     print(talk['title'], talk['date'], type(talk['date']))
    conferences = Conferences.load('data/conferences.yml')
    print(conferences)

if __name__ == '__main__':
    main()
