from os import path

MODULE_PATH = path.abspath(path.dirname(__file__))
STATIC_PATH = path.join(MODULE_PATH, 'static')


def static_file(filename: str) -> str:
    """
    Return the full path to a static asset
    :param filename: the path to the static asset relative to the `static` directory
    :return: the full path to the given static asset
    """
    return path.join(STATIC_PATH, filename)
