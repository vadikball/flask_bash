"""Command Service"""

from app.services.command_executor import CommandExecutor


class CommandService:
    def __init__(self, executor: CommandExecutor):
        self._executor = executor

    def ls(self, path: str) -> list[str]:
        return self._executor.run("ls", path).split()

    def rm(self, object_name: str) -> None:
        self._executor.run("rm", "-rf", object_name)

    def touch(self, file_name: str, path: str) -> None:
        self._executor.run("touch", self._make_path(file_name, path))

    def mkdir(self, dir_name: str, path: str) -> None:
        self._executor.run("mkdir", "-p", self._make_path(dir_name, path))

    def chmod(self, object_name: str, mask: int) -> None:
        self._executor.run("chmod", self._eval_mask(mask), object_name)

    def chown(self, object_name: str, owner: str) -> None:
        self._executor.run("chown", owner, object_name)

    def _eval_mask(self, mask: int) -> str:
        if mask < 10:
            return "00{0}".format(mask)

        if mask < 100:
            return "0{0}".format(mask)

        return str(mask)

    def _make_path(self, dir_name: str, path: str) -> str:
        return (
            "/".join(
                (
                    path,
                    dir_name,
                )
            )
            if path
            else dir_name
        )


command_service = CommandService(CommandExecutor())
