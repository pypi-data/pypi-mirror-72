
from path_util.path import Path


def create_path(path):

    path = Path(path)

    if path.is_file_like:
        path.create_file()
    else:
        path.create_dir()

    return True


