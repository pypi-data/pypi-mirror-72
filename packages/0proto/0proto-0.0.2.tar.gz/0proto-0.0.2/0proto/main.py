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


def login(name: str = 'default', client_id: str = '', client_secret: str =''):
    '''
    Logs in, and saves session to BASE_DIR/sessions
    '''

    driver = DRIVER
    DRIVE = f'{driver}:{name}' # e.g., 1proto:default

    print(f"Credentials for {DRIVE}:")

    credentials = {
        # 'key': 'value',
    }

    METADRIVE_DIR = os.path.expanduser(settings.BASE_DIR)
    SESSIONS_DIR =  os.path.join(METADRIVE_DIR, 'sessions')

    session_dir = os.path.join(SESSIONS_DIR, DRIVE)

    if not os.path.exists(session_dir):
        os.makedirs(session_dir)

    session_file = os.path.join(session_dir, 'credentials.yaml')

    with open(session_file, 'w') as f:
        f.write(json.dumps(credentials))
        print('New credentials successfully saved.')


@app.command()
def collect(url: str, name: str = 'default', path: str = ""):

    driver = DRIVER + '-' + urllib.parse.urlparse(url).hostname

    DRIVE = f'{driver}:{name}'


    # EXAMPLE ACCESS:

    # METADRIVE_DIR = os.path.expanduser(settings.BASE_DIR)
    # SESSIONS_DIR =  os.path.join(METADRIVE_DIR, 'sessions')
    # session_dir = os.path.join(SESSIONS_DIR, DRIVE)
    # session_file = os.path.join(session_dir, 'credentials.yaml')
    #
    # # LOGGING IN:
    # if not os.path.exists(session_file):
    #     login(name)
    #
    # credentials = json.load(open(session_file, 'r'))
    # # with credentials:
    # #     FEED = ...


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

    instance = None
    for item in FEED['items']:
        item['@'] = DRIVE
        item['-'] = item['url']
        item['!'] = '2000-01-11T11:01:18.653404'

        instance = Item(item)
        instance.save()


    if instance:
        typer.echo("DONE: " + str(instance.get_filedir()))

if __name__ == "__main__":
    app()
