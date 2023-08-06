
from pathlib import Path as Pathlib


class Path:

    def __init__(self, path):
        self._path = path

    def __repr__(self):
        return f"<Path '{self.path}'>"

    @property
    def path(self):
        return self._path

    @property
    def pathlib(self):
        return Pathlib(self.path)

    @property
    def has_suffix(self):
        return self.pathlib.suffix != ''

    @property
    def exists(self):
        return self.pathlib.exists()

    @property
    def is_file_like(self):

        if self.has_suffix:
            return True

        return False

    @property
    def parent(self):
        parent_path = str(self.pathlib.parent)
        return Path(parent_path)

    def create_file(self):
        self.parent.create_dir()
        self.pathlib.touch()

    def create_dir(self):
        return self.pathlib.mkdir(parents=True, exist_ok=True)




