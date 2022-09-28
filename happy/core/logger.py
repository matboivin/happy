"""Main logger."""

from logging import Logger

import coloredlogs
from verboselogs import VerboseLogger

DEFAULT_LOG_LEVEL: str = "DEBUG"
DEBUG_FORMATTING: str = (
    "%(asctime)s - %(name)s - %(levelname)s - "
    "%(filename)s:%(lineno)d %(funcName)s() - %(message)s"
)


def init_logger(
    name: str,
    formatting: str = "%(asctime)s - %(name)s [%(levelname)s] %(message)s",
) -> Logger:
    """Initialize a logger instance.

    Parameters
    ----------
    name : str
        The logger's name.
    formatting : str, optional
        The desired log formatting.

    Returns
    -------
    logging.Logger
        The logger.

    """
    logger: Logger = VerboseLogger(name)

    coloredlogs.install(
        logger=logger,
        level=DEFAULT_LOG_LEVEL,
        fmt=formatting,
        isatty=True,
    )

    return logger


api_logger: Logger = init_logger("Happy")
