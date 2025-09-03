import datetime
import typer
import typing
import pathlib
import shutil
import frontmatter as fm
from rich.pretty import pprint
from slugify import slugify
from ruamel.yaml import YAML

def is_folder_note(path: pathlib.Path):
    return path.is_dir() and (path / 'index.md').exists()

def ignore_folder_note(path, names):
    lpath = pathlib.Path(path)
    return [lpath.name]

def find_notes(parent_path: pathlib.Path) -> typing.Iterator[pathlib.Path]:
    for path in parent_path.glob('*'):
        if path.is_file() and path.name.endswith('.md'):
            yield path, False
        elif is_folder_note(path):
            yield path, True

class RuamYAMLHandler(fm.YAMLHandler):
    # def __init__(self):
    #     self.yaml = YAML()


    def load(self, fm, **kwargs):
        yaml = YAML()
        yaml.preserve_quotes = True
        return yaml.load(fm)
    
    def export(self, metadata, **kwargs):
        yaml = YAML()
        yaml.preserve_quotes = True
        import io
        s = io.StringIO()
        yaml.dump(metadata, s)
        return s.getvalue()


def main(
    parent_path: typing.Annotated[pathlib.Path, typer.Argument(exists=True, file_okay=True, dir_okay=True)],
    target_path: typing.Annotated[pathlib.Path, typer.Argument(exists=True, dir_okay=True)] = pathlib.Path('content/post'),
):
    for path, is_folder in find_notes(parent_path):

        if is_folder:
            markdown_document_path = path / 'index.md'
        else:
            markdown_document_path = path

        handler = RuamYAMLHandler()
        document = fm.load(markdown_document_path, handler=handler)
        date = document.metadata['date']#.strftime('%Y-%m-%d')
        if isinstance(date, str):
            date = datetime.datetime.fromisoformat(date)
            document.metadata['date'] = date

        computed_slug = slugify(document.metadata['title'])
        slug = document.metadata.get('slug', computed_slug)
        document.metadata['slug'] = slug


        if (image := document.metadata.get('image')) and image.startswith('![[') and image.endswith(']]'):
            document.metadata['image'] = image[3:-2]


        t_path = f"{date.strftime('%Y-%m-%d')}-{slug}"

        post = fm.Post(document.content, **document.metadata)

        dumped_post = fm.dumps(post, handler=handler)

        if not is_folder:
            final_path = target_path / f'{t_path}.md'
            print(f'{final_path=}')
            final_path.write_text(dumped_post, encoding='utf-8')
        else:
            final_path = target_path / t_path
            print(f'{final_path=}')
            final_path.mkdir(exist_ok=True)
            shutil.copytree(path, final_path, ignore=ignore_folder_note, dirs_exist_ok=True)
            (final_path / 'index.md').write_text(dumped_post, encoding='utf-8')


if __name__ == '__main__':
    typer.run(main)