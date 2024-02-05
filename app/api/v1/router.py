"""V1 API Router"""

from functools import partial

from flask import Blueprint, Response as FlaskResponse, jsonify, request
from flask_pydantic_spec import Response  # type: ignore

from app.schemas.v1.schemas import ChmodIn, ChownIn, ClientError, LsOut, MkdirIn, OkStatus, PathBase, RmIn, TouchIn
from app.services import command_service, pydantic_spec
from app.services.shortcut import ShortCut

router = Blueprint("v1", __name__, url_prefix="/v1")

shortcut = ShortCut(router, pydantic_spec.api_spec)
OkResponse = partial(Response, HTTP_200=OkStatus, HTTP_400=ClientError)
LsResponse = Response(HTTP_200=LsOut, HTTP_400=ClientError)


@router.get("/")
def common_handler() -> str:
    return "Hello, I am very fast and efficient application!"


@shortcut.route("/ls", methods=["GET"]).validate(query=PathBase, resp=LsResponse).middleware
def ls_handler() -> FlaskResponse:
    """
    Получить содержимое директории

    Имя директории, содержимое которой необходимо получить, должно быть передано как query, например:
    /ls?path=~
    """
    query: PathBase = request.context.query  # type: ignore
    return jsonify(dir_items=command_service.command_service.ls(query.path))


@shortcut.route("/rm", methods=["DELETE"]).validate(body=RmIn, resp=OkResponse()).ok_response().middleware
def rm_handler() -> None:
    """Удалить файл или директорию, имя которой было передано через object_name"""
    body: RmIn = request.context.body  # type: ignore
    command_service.command_service.rm(body.object_name)


@shortcut.route("/touch", methods=["POST"]).validate(body=TouchIn, resp=OkResponse()).ok_response().middleware
def touch_handler() -> None:
    """Создать файл с определённым именем и по определённому пути"""
    body: TouchIn = request.context.body  # type: ignore
    command_service.command_service.touch(body.file_name, body.path)


@shortcut.route("/mkdir", methods=["POST"]).validate(body=MkdirIn, resp=OkResponse()).ok_response().middleware
def mkdir_handler() -> None:
    """Создать директорию с определённым именем и по определённому пути"""
    body: MkdirIn = request.context.body  # type: ignore
    command_service.command_service.mkdir(body.dir_name, body.path)


@shortcut.route("/chmod", methods=["POST"]).validate(body=ChmodIn, resp=OkResponse()).ok_response().middleware
def chmod_handler() -> None:
    """Изменить маску разрешений файла или директории"""
    body: ChmodIn = request.context.body  # type: ignore
    command_service.command_service.chmod(body.object_name, body.mask)


@shortcut.route("/chown", methods=["POST"]).validate(body=ChownIn, resp=OkResponse()).ok_response().middleware
def chown_handler() -> None:
    """Изменить владельца файла или директории"""
    body: ChownIn = request.context.body  # type: ignore
    command_service.command_service.chown(body.object_name, body.owner)
