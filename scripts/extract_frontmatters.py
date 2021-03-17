import frontmatter
import pendulum
import pathlib

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
            position['start-on'] = pendulum.from_format(position['start-on'], 'YYYY/MM').date()
            try:
                position['stop-on'] = pendulum.from_format(position['stop-on'], 'YYYY/MM').date()
                position['current'] = False
            except KeyError:
                position['stop-on'] = pendulum.today().end_of('month').date()
                position['current'] = True
            positions.append(position)

        positions.sort(key=lambda position: position['stop-on'], reverse=True)
        self.positions = positions

def main():
    loader = PositionLoader(pathlib.Path('content/positions'))
    loader.load()
    for position in loader.get_positions():
        print(f"{position['start-on']} {position['stop-on']} {position['title']}")

    print(loader.get_current_positions())

if __name__ == '__main__':
    main()