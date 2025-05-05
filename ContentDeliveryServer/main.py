from flask import Flask, send_file, render_template_string
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


app = Flask(__name__)


def send_folder(path: Path) -> str:
    next_parent = path.relative_to(MEDIA_PATH.absolute())

    html = (f"<html><head>"
            f""
            f"</head><body>"
            f"<style>"
             "body {font-size: 22;}"
            f"</style>"
            f"<p><a href=..>..</a><p>"
            f"{''.join([(f"<p><a href=/{next_parent}/{str(x.relative_to(path))}>{str(x.relative_to(path))}</a></p>" 
                        if (not str(x.name).startswith(".") or not CONFIG_HIDDEN_FILES) else '') 
                        for x in path.iterdir()])}"
            f"</body></html>")

    return html


@app.route("/")
def base_folder():
    if not CONFIG_ALLOW_FOLDERS:
        return send_file(FALLBACK_IMAGE)

    return send_folder(MEDIA_PATH.absolute())


@app.route("/<path:filepath>")
def send_media(filepath: str):
    target_path = sanitize_path(filepath)
    actual_relative_path = Path(f"{MEDIA_PATH}/{target_path}")
    absolute_path = actual_relative_path.absolute()

    if not absolute_path.exists() or (absolute_path.is_dir() and not CONFIG_ALLOW_FOLDERS):
        return send_file(FALLBACK_IMAGE)
    elif absolute_path.is_dir():
        return send_folder(absolute_path)

    return send_file(absolute_path)


if __name__ == "__main__":
    import logging

    lumberjack = logging.getLogger("BnDLett/ContentDeliveryServer")
    lumberjack.warning("CAUTION: DO NOT RUN THIS SCRIPT DIRECTLY UNLESS YOU KNOW WHAT YOU ARE DOING.")

    app.run('0.0.0.0', 8080, debug=True)
