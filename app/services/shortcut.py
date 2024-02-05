"""Shortcut Service"""

from functools import wraps
from typing import Any, Callable, Iterable, Optional, Self

from flask import Blueprint, Response, jsonify
from flask_pydantic_spec import FlaskPydanticSpec  # type: ignore
from flask_pydantic_spec.types import RequestBase, ResponseBase  # type: ignore
from pydantic import BaseModel

from app.middlewares.command_ecxeption import command_exception_middleware


class ShortCut:
    def __init__(self, router: Blueprint, api_spec: FlaskPydanticSpec):
        self._router = router
        self._api_spec = api_spec
        self._handlers: list[Callable] = []

    def route(self, rule: str, **options: Any) -> Self:
        def inner(func: Callable) -> Callable:
            return self._router.route(rule, **options)(func)

        self._handlers.append(inner)
        return self

    def validate(
        self,
        query: type[BaseModel] | None = None,
        body: RequestBase | type[BaseModel] | None = None,
        headers: type[BaseModel] | None = None,
        cookies: type[BaseModel] | None = None,
        resp: Optional[ResponseBase] = None,
        tags: Iterable[str] = (),
        deprecated: bool = False,
        before: Callable | None = None,
        after: Callable | None = None,
    ) -> Self:
        def inner(func: Callable) -> Callable:
            return self._api_spec.validate(query, body, headers, cookies, resp, tags, deprecated, before, after)(func)

        self._handlers.append(inner)
        return self

    def middleware(self, func: Callable) -> Callable:
        inner_handler = wraps(func)(command_exception_middleware(func))
        for callback in self._handlers[::-1]:
            inner_handler = callback(inner_handler)

        self._handlers = []
        return inner_handler

    def ok_response(self) -> Self:
        def inner(func: Callable) -> Callable:
            @wraps(func)
            def _inner(*args: Any, **kwargs: Any) -> Response:
                func(*args, **kwargs)
                return jsonify(status="ok")

            return _inner

        self._handlers.append(inner)
        return self
