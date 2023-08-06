"""
Unit tests for app_deploy.__main__.py
"""
from contextlib import ExitStack as does_not_raise
import json
import os

from pathlib import Path
import pytest
from app_deploy import __main__

cfg = __main__.get_config()


def test_load_config():
    """Validate config can load."""
    config = __main__.load_config()

    if os.path.exists(os.environ.get("HOME") + "/.marathon-api.conf"):
        assert config is not None
    else:
        assert config is None


@pytest.mark.parametrize(
    "keyword", [("user"), ("password"), ("marathon_site_dev"), ("marathon_site_prod"),],
)
def test_get_config(keyword):
    """Validate config gathering from env vars."""
    config = __main__.get_config()
    assert config[keyword]


@pytest.mark.parametrize(
    "arguments, exception, result",
    [
        (["--help"], pytest.raises(SystemExit), None),
        (["--backup"], pytest.raises(SystemExit), None),
        (
            [
                "--backup",
                "--deploy",
                "--env",
                "dev",
                "--project",
                "foo",
                "--job",
                "myjob",
                "--file",
                "myfile",
            ],
            does_not_raise(),
            {
                "backup": True,
                "deploy": True,
                "env": "dev",
                "project": "foo",
                "job": "myjob",
                "file": "myfile",
                "test": False,
            },
        ),
        (
            [
                "--backup",
                "--env",
                "dev",
                "--project",
                "foo",
                "--job",
                "myjob",
                "--file",
                "myfile",
            ],
            does_not_raise(),
            {
                "backup": True,
                "deploy": False,
                "env": "dev",
                "project": "foo",
                "job": "myjob",
                "file": "myfile",
                "test": False,
            },
        ),
    ],
)
def test_get_args(arguments, exception, result):
    """Validate argument parser object building."""
    parser = __main__.get_args()
    with exception:
        args = vars(parser.parse_args(arguments))
        print(f"> parser args are: {args}")
        assert args == result


@pytest.mark.parametrize(
    "args, result",
    [
        ({"backup": True, "deploy": False,}, True),
        ({"backup": False, "deploy": True,}, True),
        ({"backup": True, "deploy": True,}, False),
        ({"backup": False, "deploy": False,}, False),
    ],
)
def test_valid_action(args, result):
    """Validate backup/deploy argument flags."""
    assert __main__.valid_action(args) is result


@pytest.mark.parametrize(
    "args, result",
    [({"env": "dev"}, True), ({"env": "prod"}, True), ({"env": "foo"}, False),],
)
def test_valid_env(args, result):
    """Validate environment argument flags."""
    assert __main__.valid_env(args) is result


@pytest.mark.parametrize(
    "args, result",
    [
        ({"backup": True, "deploy": False, "file": "mytmptestfile.json"}, True),
        ({"backup": False, "deploy": True, "file": "mytmptestfile.json"}, True),
        ({"backup": False, "deploy": True, "file": "filedoesntexist.json"}, False,),
    ],
)
def test_valid_file(args, result):
    """Validate json file checking."""
    Path("mytmptestfile.json").touch()
    assert __main__.valid_file(args) is result
    Path("mytmptestfile.json").unlink()


# TODO
# def test_validate_args(parser):


@pytest.mark.parametrize(
    "marathon_site, user, password, params, exception",
    [
        (
            cfg["marathon_site_dev"],
            cfg["user"],
            cfg["password"],
            {"id": "/lcmap"},
            does_not_raise(),
        ),
        (
            cfg["marathon_site_dev"],
            cfg["user"],
            cfg["password"],
            {"id": "/doesnotexist"},
            pytest.raises(IndexError),
        ),
    ],
)
def test_get_apps_data(marathon_site, user, password, params, exception):
    """Validate getting job app definitions."""
    response = __main__.get_apps_data(marathon_site, user, password, params)
    print(f"> response is: {response}")
    with exception:
        assert response["apps"][0]["id"] is not None


# TODO
# def deploy_apps(test, marathon_site, user, password, job_list):


@pytest.mark.parametrize(
    "json_data", [([{"id": "/myproject/myapp", "cmd": "null", "args": "null"}]),],
)
def test_format_pretty_json(json_data):
    """Validate formatting doesn't change data structure."""
    pretty_json = __main__.format_pretty_json(json_data)
    print(f"> pretty_json is: {pretty_json}")
    assert json_data[0]["id"] in json.loads(pretty_json)[0]["id"]
    assert json_data[0]["cmd"] in json.loads(pretty_json)[0]["cmd"]
    assert json_data[0]["args"] in json.loads(pretty_json)[0]["args"]


@pytest.mark.parametrize(
    "test, file_path, pretty_output, result",
    [
        (
            False,
            "./mytmptestfile.json",
            '[{"id": "/myproject/myapp", "cmd": "null", "args": "null"}]',
            True,
        ),
    ],
)
def test_save_output(test, file_path, pretty_output, result):
    """Validate output is saved to disk."""
    __main__.save_output(test, file_path, pretty_output)
    assert os.path.exists(file_path) is result


@pytest.mark.parametrize(
    "file_path, job_key, job_value",
    [("mytmptestfile.json", "id", "/myproject/myapp"),],
)
def test_load_job_file(file_path, job_key, job_value):
    """Validate loading of a json job file."""
    job_data = __main__.load_job_file(file_path)
    assert job_data[0][job_key] == job_value
    Path("mytmptestfile.json").unlink()


@pytest.mark.parametrize(
    "job_filter, job_list, jobs_length",
    [
        (
            "myproject",
            [
                {"id": "/myproject/myapp01", "cmd": "null", "args": "null"},
                {"id": "/myproject/myapp02", "cmd": "null", "args": "null"},
                {"id": "/anotherproject/myapp01", "cmd": "null", "args": "null"},
            ],
            2,
        ),
        (
            "anotherproject",
            {
                "apps": [
                    {"id": "/myproject/myapp01", "cmd": "null", "args": "null"},
                    {"id": "/myproject/myapp02", "cmd": "null", "args": "null"},
                    {"id": "/anotherproject/myapp01", "cmd": "null", "args": "null"},
                ]
            },
            1,
        ),
        (
            "myapp01",
            [
                {"id": "/myproject/myapp01", "cmd": "null", "args": "null"},
                {"id": "/myproject/myapp02", "cmd": "null", "args": "null"},
                {"id": "/anotherproject/myapp01", "cmd": "null", "args": "null"},
            ],
            2,
        ),
        (
            "all",
            [
                {"id": "/myproject/myapp01", "cmd": "null", "args": "null"},
                {"id": "/myproject/myapp02", "cmd": "null", "args": "null"},
                {"id": "/anotherproject/myapp01", "cmd": "null", "args": "null"},
            ],
            3,
        ),
        (
            "all",
            {
                "apps": [
                    {"id": "/myproject/myapp01", "cmd": "null", "args": "null"},
                    {"id": "/myproject/myapp02", "cmd": "null", "args": "null"},
                    {"id": "/anotherproject/myapp01", "cmd": "null", "args": "null",},
                ]
            },
            3,
        ),
    ],
)
def test_filter_jobs(job_filter, job_list, jobs_length):
    """Validate jobs are filtered out correctly."""
    filtered_jobs = __main__.filter_jobs(job_filter, job_list)
    print(f"> filtered_jobs are: {filtered_jobs}")
    assert len(filtered_jobs) == jobs_length


# TODO
# def test_backup_jobs(
# project, job_filter, test, marathon_site, user, password, file_path=None
# ):

# TODO
# def test_deploy_jobs(
# project, job_filter, test, marathon_site, user, password, file_path=None
# ):
