"""Shortcut Service"""

from subprocess import run  # noqa: S404
from typing import Any

from app.exceptions.command_exception import CommandException


class CommandExecutor:
    def run(self, *args: Any) -> str:
        command_result = run(tuple(arg.split()[0] for arg in args), capture_output=True, text=True)  # noqa: S603

        if command_result.stderr:
            raise CommandException(command_result.stderr)

        return command_result.stdout
