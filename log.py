import logging
from os import path

logger = logging.getLogger("Progress")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(path.abspath(path.join(".", "progress.log")))
formatter = logging.Formatter("%(asctime)s %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
fh.setFormatter(formatter)
logger.addHandler(fh)


def debug(message):
    logger.debug(message)
