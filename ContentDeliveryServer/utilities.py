from pathlib import Path
from os import path


# https://stackoverflow.com/a/66950540
def sanitize_path(filepath: str | Path) -> Path:
    """
    Sanitize a path against directory traversals
    """
    if isinstance(filepath, Path):
        filepath = str(filepath)

    # - pretending to chroot to the current directory
    # - cancelling all redundant paths (/.. = /)
    # - making the path relative
    return Path(path.relpath(path.normpath(path.join("/", filepath)), "/"))
