import os
import typer
import metatype
import urllib

from . import settings


app = typer.Typer()

DRIVER = __name__.split('.', 1)[0]


class User(metatype.Dict):
    pass


class Item(metatype.Dict):
    pass


@app.command()
def collect(url: str, name: str = 'default', path: str = ""):

    driver = DRIVER + '-' + urllib.parse.urlparse(url).hostname

    DRIVE = f'{driver}:{name}'

    # EXAMPLE DATA:

    FEED = {
        "items": [
            {'a': 1, 'url': 'https://example.com/1'},
            {'b': 2, 'url': 'https://example.com/2'}]}

    if path:
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            metatype.config.DATA_DIR = os.path.join(path, 'data')
        except:
            print("Can't create on selected path.")
    else:
        METADRIVE_DIR = os.path.expanduser(settings.BASE_DIR)
        metatype.config.DATA_DIR = os.path.join(METADRIVE_DIR, 'data')


    # ITERATING AND SAVING:

    for item in FEED['items']:
        item['@'] = DRIVE
        item['-'] = item['url']
        item['!'] = '2000-01-11T11:01:18.653404'

        Item(item).save()


    typer.echo("DONE: " + str(Item(item).get_filedir()))

if __name__ == "__main__":
    app()
