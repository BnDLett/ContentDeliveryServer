from flask import Flask, send_file
from pathlib import Path
from os import chdir
from os.path import realpath
from sys import argv

from utilities import sanitize_path

SCRIPT_PATH = Path(realpath(__file__))
ROOT_DIRECTORY = SCRIPT_PATH.parent.parent
FALLBACK_IMAGE = Path(f"{ROOT_DIRECTORY}/static/unknown_path.png")
MEDIA_PATH = Path("media/")

chdir(ROOT_DIRECTORY)

if (len(argv) != 1) and (__name__ == "__main__"):
    parent_path = Path(argv[1])

    if not parent_path.exists():
        raise ValueError("The parent path provided in the command-line argument is invalid.")

    chdir(parent_path)

MEDIA_PATH.mkdir(exist_ok=True)
app = Flask(__name__)


@app.route("/<path:filepath>")
def send_media(filepath: str):
    target_path = sanitize_path(filepath)
    actual_relative_path = Path(f"{MEDIA_PATH}/{target_path}")
    absolute_path = actual_relative_path.absolute()

    if not absolute_path.exists() or not absolute_path.is_file():
        return send_file(FALLBACK_IMAGE)

    return send_file(absolute_path)


if __name__ == "__main__":
    app.run('0.0.0.0', 8080)
