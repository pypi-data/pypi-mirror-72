import logging
import sys

AUTODL_LOGGER = None


def get_logger(verbosity_level):
    """Set logging format to something like:
       2019-04-25 12:52:51,924 INFO model.py: <message>
    """
    global AUTODL_LOGGER
    if AUTODL_LOGGER is None:
        logger = logging.getLogger(__file__)
        logging_level = getattr(logging, verbosity_level)
        logger.setLevel(logging_level)
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(filename)s: %(message)s"
        )
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging_level)
        stdout_handler.setFormatter(formatter)
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.WARNING)
        stderr_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)
        logger.addHandler(stderr_handler)
        logger.propagate = False
        AUTODL_LOGGER = logger
    return AUTODL_LOGGER
