#!/usr/bin/env python3
"""
Title: __main__.py
Description: LCMAP App Deploy (Backup/Deploy).
             Backup app definitions from a Marathon endpoint to a json file.
             Deploy app definitions from a json file to a Marathon endpoint.
               Create if it doesn't exist, modify if it does.
"""
import argparse
import configparser
import json
import os
import sys

import requests


def load_config(file_path=None):
    """
    Load external ini style configuration if it exists.
    Args:
      file_path: String path to the name of the ini config file to load. [Optional]
    Returns: Config file parser object or None if file doesn't exist.
    """
    if not file_path:
        file_path = os.environ.get("HOME") + "/.marathon-api.conf"

    if os.path.exists(file_path):
        config = configparser.ConfigParser()
        config.read(file_path)
        return config

    return None


def get_config(file_path=None):
    """
    Load configuration from env vars or an external file.
    Args:
      file_path: String path to the name of the ini config file to load. [Optional]
    Returns: A dictionary of the loaded config from env vars or external file.
    """
    main_config = load_config(file_path)

    if main_config:
        config = {
            "user": os.environ.get(
                "marathon_username", main_config.get("marathon", "username")
            ),
            "password": os.environ.get(
                "marathon_password", main_config.get("marathon", "password")
            ),
            "marathon_site_dev": os.environ.get(
                "marathon_site_dev", main_config.get("marathon", "site_dev")
            ),
            "marathon_site_prod": os.environ.get(
                "marathon_site_prod", main_config.get("marathon", "site_prod")
            ),
        }
    else:
        config = {
            "user": os.environ.get("marathon_username"),
            "password": os.environ.get("marathon_password"),
            "marathon_site_dev": os.environ.get("marathon_site_dev"),
            "marathon_site_prod": os.environ.get("marathon_site_prod"),
        }

    return config


def get_args():
    """
    Build argument parser information.
    Args: None.
    Returns: The built parser object.
    """
    parser = argparse.ArgumentParser(
        description="Backup/Deploy Marathon Apps in JSON format via the API."
    )
    parser.add_argument(
        "-b",
        "--backup",
        help="Perform a job backup operation.[backup or deploy Required]",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "-d",
        "--deploy",
        help="Perform a job deploy operation.[deploy or backup Required]",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "-e",
        "--env",
        help="Marathon Environment Name(dev|prod)[Required]",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--project",
        help="Project name filter. Initial query filter when getting jobs from Marathon. Applied BEFORE job name filter.[Required]",
        required=True,
    )
    parser.add_argument(
        "-j",
        "--job",
        help="Job name filter. (Ex: 'all' for all jobs or 'foo' for only jobs that contain foo) Applied AFTER project filter.[Required]",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Backup to or deploy from this file.[Required]",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--test",
        help="Do NOT make any changes. Run test and output what would have happened.",
        action="store_true",
        required=False,
    )
    return parser


def valid_action(args):
    """
    Validate the action to take (backup/deploy).
    Args:
      args: A parser object's parse_args vars.
    Returns: True if arguments are valid, False otherwise.
    """
    if args["backup"] and args["deploy"]:
        print(">> ERROR! Cannot perform both backup (-b) and deploy (-d).")
        return False

    if not args["backup"] and not args["deploy"]:
        print(">> ERROR! Must perform either backup (-b) or deploy (-d).")
        return False

    return True


def valid_env(args):
    """
    Validate the environment chosen.
    Args:
      args: A parser object's parse_args vars.
    Returns: True if a valid environment, False otherwise.
    """
    if args["env"] == "dev" or args["env"] == "prod":
        return True

    print(f">> ERROR! Unknown environment ({args['env']})")
    return False


def valid_file(args):
    """
    Validate the file to use for deploy.
    Args:
      args: A parser object's parse_args vars.
    Returns: True if a valid file, False otherwise.
    """
    if args["deploy"] and os.path.exists(args["file"]):
        return True

    if args["backup"]:
        # File may not exist yet, don't check for it.
        return True

    print(f">> ERROR! File/directory provided does not exist. ({args['file']})")
    return False


def validate_args(parser):
    """
    Validate gathered arguments meet criteria.
    Adds additional config settings.
    Args:
      parser: A parser object's parse_args vars.
    Returns: None. Side effect of exiting with error if invalid args.
    """
    args = vars(parser.parse_args())

    if not valid_action(args):
        parser.print_help()
        sys.exit(1)

    if not valid_env(args):
        parser.print_help()
        sys.exit(1)

    if not valid_file(args):
        parser.print_help()
        sys.exit(1)


def get_apps_data(marathon_site, user, password, params=None):
    """
    Download Marathon application configuration.
    Args:
      marathon_site: The marathon endpoint/URL.
      user: The marathon login username.
      password: The marathon login's password.
      params: Additional parameters to pass to the marathon endpoint.
    Returns: The response object in json format.
    """
    print(f">> Backup jobs from Marathon Endpoint: {marathon_site}")

    response = requests.get(marathon_site, auth=(user, password), params=params,)
    print(f"-> HTTP Status Code was: {response.status_code}")

    if response.status_code != 200:
        print("--> ERROR! Response code was NOT 200(OK), exiting now.")
        sys.exit(1)

    return response.json()


def deploy_apps(test, marathon_site, user, password, job_list):
    """
    Change apps by modifying existing or creating new ones.
    Args:
      test: A boolean. True if testing, False otherwise.
      marathon_site: The marathon endpoint to deploy job(s) to.
      user: The marathon login username.
      password: The marathon login's password.
      job_list: A list of dictionary job definitions.
    Returns: True if all puts return OK, False otherwise.
             Side effect of putting app job(s) to Marathon endpoint.
    """
    print(f">> Deploying jobs to Marathon Endpoint: {marathon_site}")
    all_ok = True

    for job in job_list:
        if test:
            print(f"--> [TEST] I would have deployed job: {job['id']}")
        else:
            print(f"--> Deploying job: {job['id']}")
            response = requests.put(marathon_site, auth=(user, password), json=[job],)

            if response.status_code == 200 or response.status_code == 201:
                print(f"---> OK. (HTTP: {str(response.status_code)})")
            else:
                print(
                    f"---> WARNING! Job might not have deployed (HTTP: {str(response.status_code)})"
                )
                print(f"     Response: {str(response.json())})")
                all_ok = False

    return all_ok


def format_pretty_json(response_data):
    """
    Format json object into string formatted output.
    Args:
      response_data: A json object.
    Returns: A formatted dictionary indented.
    """
    return json.dumps(response_data, indent=2)


def save_output(test, file_path, pretty_output):
    """
    Save the json output to a file.
    Args:
      test: A boolean. True if testing, False otherwise.
      file_path: A string of the full path to the file to use.
      pretty_output: The formatted output to write to a file.
    Returns: None. Side effect of a file write.
    """
    if test:
        print(f">> [TEST] I would have saved output to: {file_path}")
    else:
        print(f">> Saving output to: {file_path}")

        with open(file_path, "w") as file_handle:
            for line in pretty_output:
                file_handle.write(line)


def load_job_file(file_path):
    """
    Load the json job data to variable.
    Args:
      file_path: A string of the full path to the file to load jobs from.
    Returns: The loaded jobs in json format.
    """
    print(f"-> Loading jobs from: {file_path}")

    with open(file_path, "r") as file_handle:
        job_data = json.load(file_handle)

    return job_data


def filter_jobs(job_filter, job_list):
    """
    Filter out only matching job names (or don't change if all specified).
    Args:
      job_filter: A string of the job name to filter.
      job_list: List of jobs to filter.
    Returns: A list of jobs matching the filter.
    """
    if job_filter == "all":
        print(f">> Select all jobs.")
        try:
            # top level data type is a dict (original marathon backup)
            filtered_output = job_list["apps"]
        except TypeError:
            # top level data type is a list (from a json job file)
            filtered_output = job_list

    else:
        print(f">> Select only jobs that contain {job_filter}")
        try:
            # top level data type is a dict (original marathon backup)
            filtered_output = list(
                filter(
                    (
                        lambda job_entry, job_name=job_filter: job_name
                        in job_entry["id"]
                    ),
                    job_list["apps"],
                )
            )
        except TypeError:
            # top level data type is a list (from a json job file)
            filtered_output = list(
                filter(
                    (
                        lambda job_entry, job_name=job_filter: job_name
                        in job_entry["id"]
                    ),
                    job_list,
                )
            )

    for job_entry in filtered_output:
        print(f"--> Selecting job: {job_entry['id']}")

    return filtered_output


def backup_jobs(
    project, job_filter, test, marathon_site, user, password, file_path=None
):
    """
    Backup Marathon jobs.
    Args:
      project: A string of the project name to filter on the initial job query.
      job_filter: A string of the job filter name.
      test: A boolean. True if testing, False otherwise.
      marathon_site: The marathon endpoint to deploy job(s) to.
      user: The marathon login username.
      password: The marathon login's password.
      file_path: String path to the name of the ini config file to load. [Optional]
    Returns: None. Side effect of a file write.
    """
    apps_data = get_apps_data(
        marathon_site, user, password, params={"id": "/" + project},
    )
    filtered_jobs = filter_jobs(job_filter, apps_data)
    pretty_output = format_pretty_json(filtered_jobs)
    save_output(test, file_path, pretty_output)


def deploy_jobs(
    project, job_filter, test, marathon_site, user, password, file_path=None
):
    """
    Deploy jobs to a Marathon endpoint.
    Modifies existing jobs, creates non-existing jobs.
    Args:
      project: A string of the project name to filter on the initial job query.
      job_filter: A string of the job filter name.
      test: A boolean. True if testing, False otherwise.
      marathon_site: The marathon endpoint to deploy job(s) to.
      user: The marathon login username.
      password: The marathon login's password.
      file_path: String path to the name of the ini config file to load. [Optional]
    Returns: True if all puts return OK, False otherwise.
             Side effect of putting app job(s) to Marathon endpoint.
    """
    loaded_jobs = load_job_file(file_path)
    project_jobs = filter_jobs("/" + project, loaded_jobs)
    filtered_jobs = filter_jobs(job_filter, project_jobs)
    all_ok = deploy_apps(test, marathon_site, user, password, filtered_jobs,)
    return all_ok


def main():
    """
    Backup or Deploy Marathon job definitions.
    Args: None.
    Returns: None.
    """
    cfg = get_config()
    parser = get_args()
    validate_args(parser)

    # grab arguments from the parser object
    args = vars(parser.parse_args())

    if args["backup"]:
        backup_jobs(
            args["project"],
            args["job"],
            args["test"],
            cfg["marathon_site_" + args["env"]],
            cfg["user"],
            cfg["password"],
            args["file"],
        )

    elif args["deploy"]:
        all_ok = deploy_jobs(
            args["project"],
            args["job"],
            args["test"],
            cfg["marathon_site_" + args["env"]],
            cfg["user"],
            cfg["password"],
            args["file"],
        )
        if all_ok:
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
