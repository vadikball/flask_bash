"""Configured application logger."""

import logging
import sys
from functools import partial
from typing import TYPE_CHECKING, Callable

from loguru import logger as _logger

from app.settings import settings

if TYPE_CHECKING:  # To avoid circular import
    from loguru import Logger


# This code copied from loguru docs, ignoring all linters warnings
# https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
class InterceptHandler(logging.Handler):
    def emit(self, record):  # type: ignore
        # Get corresponding Loguru level if it exists
        try:
            level = _logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS352, WPS609
            frame = frame.f_back  # type: ignore [assignment]
            depth += 1

        _logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


logger_handler = InterceptHandler()


def setup_logger() -> "Logger":
    # Remove every logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # Intercept everything at the root logger

    logging.basicConfig(handlers=[logger_handler], level=0)

    handler_config: Callable = partial(dict, level=logging.DEBUG if settings.DEBUG else logging.INFO, enqueue=True)

    # Setup loguru main logger
    _logger.configure(
        handlers=[
            handler_config(sink=sys.stdout),
            handler_config(sink="flask_bash.log"),
        ],
    )

    return _logger


logger = setup_logger()
