import logging
from artichoqe.commands import aws


def main() -> None:
    logging.basicConfig(format='%(message)s')
    logging.getLogger(__package__).setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Artichoqe is coming !')
