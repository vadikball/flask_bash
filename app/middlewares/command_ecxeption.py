"""Command Exception Middleware"""

import traceback
from functools import wraps
from typing import Any, Callable, TypeVar

from flask import jsonify
from werkzeug.exceptions import HTTPException

from app.exceptions.command_exception import CommandException
from app.logger import logger
from app.schemas.v1.schemas import ClientError

HandlerReturnType = TypeVar("HandlerReturnType")


def command_exception_middleware(
    api_handler: Callable[[...], HandlerReturnType]  # type: ignore
) -> Callable[[...], HandlerReturnType]:  # type: ignore
    @wraps(api_handler)
    def inner(*args: Any, **kwargs: Any) -> HandlerReturnType:
        try:
            return api_handler(*args, **kwargs)
        except CommandException as exc:
            logger.debug(traceback.format_exc())

            description = exc.args[0]

            error_response = jsonify(ClientError(name=exc.__class__.__name__, description=description).dict())
            error_response.status_code = 400
            raise HTTPException(description=description, response=error_response)

    return inner
