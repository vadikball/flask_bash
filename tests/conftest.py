"""Test Config"""

import traceback
from typing import Iterable

from flask.testing import FlaskClient
from pytest import fixture

from app.app import create_app
from app.exceptions.command_exception import CommandException
from app.logger import logger
from app.services.command_executor import CommandExecutor


@fixture
def test_client() -> FlaskClient:
    return create_app().test_client()


@fixture
def v1_prefix() -> str:
    return "/api/v1{0}"


@fixture
def command_executor() -> CommandExecutor:
    return CommandExecutor()


@fixture
def test_dir(command_executor: CommandExecutor) -> Iterable[str]:
    test_dir = "/home/appuser/test"
    command_executor.run("mkdir", test_dir)

    yield test_dir

    try:
        command_executor.run("rm", "-r", test_dir)
    except CommandException:
        logger.debug(traceback.format_exc())


@fixture
def test_dir_object(command_executor: CommandExecutor, test_dir: str) -> Iterable[tuple[str, str]]:
    test_object = "{0}/test_object".format(test_dir)
    command_executor.run("touch", test_object)

    yield test_dir, test_object
