"""App Tests"""

from flask.testing import FlaskClient

from app.services.command_executor import CommandExecutor


def test_common(test_client: FlaskClient, v1_prefix: str) -> None:
    app_response = test_client.get(v1_prefix.format("/"))
    assert app_response.status_code == 200


def test_ls(test_client: FlaskClient, test_dir_object: tuple[str, str], v1_prefix: str) -> None:
    test_dir, test_object = test_dir_object

    app_response = test_client.get(v1_prefix.format("/ls?path={0}".format(test_dir)))
    assert app_response.status_code == 200
    assert app_response.json == {"dir_items": ["test_object"]}

    app_response = test_client.get(v1_prefix.format("/ls?path=/test"))
    assert app_response.status_code == 400


def test_rm(
    test_client: FlaskClient, command_executor: CommandExecutor, v1_prefix: str, test_dir_object: tuple[str, str]
) -> None:
    test_dir, test_object = test_dir_object

    new_test_dir = "{0}/test_rm_dir".format(test_dir)
    command_executor.run("mkdir", new_test_dir)
    command_executor.run("touch", "{0}/test_rm_dir/test_object".format(test_dir))

    app_response = test_client.delete(v1_prefix.format("/rm"), json={"object_name": new_test_dir})
    assert app_response.status_code == 200
    assert command_executor.run("ls", test_dir).split() == ["test_object"]

    app_response = test_client.delete(v1_prefix.format("/rm"), json={"object_name": "/home"})
    assert app_response.status_code == 400


def test_touch(test_client: FlaskClient, command_executor: CommandExecutor, v1_prefix: str, test_dir: str) -> None:
    app_response = test_client.post(v1_prefix.format("/touch"), json={"file_name": "test_object", "path": test_dir})
    assert app_response.status_code == 200
    assert command_executor.run("ls", test_dir).split() == ["test_object"]

    app_response = test_client.post(v1_prefix.format("/touch"), json={"file_name": "test", "path": "/"})
    assert app_response.status_code == 400


def test_chmod(
    test_client: FlaskClient, command_executor: CommandExecutor, v1_prefix: str, test_dir_object: tuple[str, str]
) -> None:
    test_dir, test_object = test_dir_object
    app_response = test_client.post(v1_prefix.format("/chmod"), json={"object_name": test_object, "mask": 1})
    assert app_response.status_code == 200
    assert command_executor.run("ls", "-l", test_dir).split()[2] == "---------x"

    app_response = test_client.post(
        v1_prefix.format("/chmod"),
        json={"object_name": "{0}/test_object_invalid".format(test_dir), "mask": 1},
    )
    assert app_response.status_code == 400


def test_chown(
    test_client: FlaskClient, command_executor: CommandExecutor, v1_prefix: str, test_dir_object: tuple[str, str]
) -> None:
    test_dir, test_object = test_dir_object
    app_response = test_client.post(
        v1_prefix.format("/chown"),
        json={"object_name": test_object, "owner": "appuser"},
    )
    assert app_response.status_code == 200
    assert command_executor.run("ls", "-l", test_dir).split()[4] == "appuser"

    app_response = test_client.post(
        v1_prefix.format("/chown"),
        json={"object_name": test_object, "owner": "docker"},
    )
    assert app_response.status_code == 400
