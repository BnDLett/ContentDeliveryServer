from flask import Flask, send_file, render_template
from pathlib import Path
from os import chdir, getenv
from os.path import realpath
from sys import argv
from configparser import ConfigParser

from utilities import sanitize_path

SCRIPT_PATH = Path(realpath(__file__))
ROOT_DIRECTORY = SCRIPT_PATH.parent.parent
FALLBACK_IMAGE = Path(f"{ROOT_DIRECTORY}/static/unknown_path.png")
MEDIA_PATH = Path("media/")
CONFIG_PATH = Path(f"{Path(x if (x := getenv('CDS_CONFIG_ROOT')) is not None else 'cds_config')}/config.ini")

chdir(ROOT_DIRECTORY)

if (len(argv) != 1) and (__name__ == "__main__"):
    parent_path = Path(argv[1])

    if not parent_path.exists():
        raise ValueError("The parent path provided in the command-line argument is invalid.")

    chdir(parent_path)

MEDIA_PATH.mkdir(exist_ok=True)

CONFIG = ConfigParser()
CONFIG.read(CONFIG_PATH.absolute())

# access
CONFIG_ALLOW_FOLDERS = CONFIG.get('access', 'allow_folder_access', fallback='').lower() == 'true'
CONFIG_HIDDEN_FILES = CONFIG.get('access', 'hidden_files', fallback='true').lower() == 'true'


app = Flask(__name__, template_folder=f'{ROOT_DIRECTORY}/templates', static_folder=f'{ROOT_DIRECTORY}/static')


def render_folder(real_path: Path) -> str:
    folder_name = real_path.name
    relative_path = real_path.relative_to(MEDIA_PATH.absolute())

    final_html = ''

    file: Path
    for file in real_path.iterdir():
        if file.name.startswith(".") and CONFIG_HIDDEN_FILES:
            continue

        file_type = 'directory' if file.is_dir() else 'file'
        button_text = 'Open directory' if file.is_dir() else 'Open file'

        file_html = (f'<form class="{file_type}" action="/{file.relative_to(MEDIA_PATH.absolute())}">'
                     f'    <img src="/static/icons/{file_type}.svg" alt="{file_type}" height=40px class="icon">'
                     f'    <p class="file_name">{file.name}</p>'
                     f'    <button type="submit">{button_text}</button>'
                     f'</form>')
        final_html += file_html

    return render_template(
        'folder.html',
        FOLDER_NAME=folder_name,
        BASE_PATH=str(relative_path.parent),
        FILES=final_html
    )


@app.route("/test")
def test_route():
    return render_template('folder.html', FOLDER_NAME = 'ROOT', BASE_PATH='/test')


@app.route("/")
def base_folder():
    if not CONFIG_ALLOW_FOLDERS:
        return send_file(FALLBACK_IMAGE)

    return render_folder(MEDIA_PATH.absolute())


@app.route("/<path:filepath>")
def send_media(filepath: str):
    target_path = sanitize_path(filepath)
    actual_relative_path = Path(f"{MEDIA_PATH}/{target_path}")
    absolute_path = actual_relative_path.absolute()

    if not absolute_path.exists() or (absolute_path.is_dir() and not CONFIG_ALLOW_FOLDERS):
        return send_file(FALLBACK_IMAGE)
    elif absolute_path.is_dir():
        return render_folder(absolute_path)

    return send_file(absolute_path)


if __name__ == "__main__":
    import logging

    lumberjack = logging.getLogger("BnDLett/ContentDeliveryServer")
    lumberjack.warning("CAUTION: DO NOT RUN THIS SCRIPT DIRECTLY UNLESS YOU KNOW WHAT YOU ARE DOING.")

    app.run('0.0.0.0', 8080, debug=True)
