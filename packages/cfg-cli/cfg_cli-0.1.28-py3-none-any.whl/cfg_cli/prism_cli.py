#!/usr/bin/env python3

from cfg_cli import __version__
from cfg_cli.clients.api import API
from cfg_cli.clients.db import DB
from cfg_cli.clients.s3 import S3
from cfg_cli.utils import (download_file, recurse_object,
                           validate_project_name, verify_file_type)
from getpass import getpass
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.validation import ValidationError, Validator
from requests.exceptions import HTTPError
from tabulate import tabulate

import fire
import functools
import json
import logging
import os
import sys


def catch_errors(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if os.getenv("PRISM_ENV") == "DEV":
                logging.exception(e)
            if isinstance(e, HTTPError) and e.response.json().get("message"):
                raise fire.core.FireError(Exception(e.response.json().get("message")))
            raise fire.core.FireError(e)

    return inner


class PrismCLI(object):
    """
    Command Line Tool to interact with Cofactor Genomics' ImmunoPrism product.
    This is the Python interface for CLI commands, the CLI command `prism` instantiates this class and sub commands correspond to methods of this object.
    """

    def _v(self):
        return __version__

    def login(self, username="", password=""):
        """
        Login with your cofactor credentials.

        Login in with your email and password.

        Examples:
            >>> prism login
            username: example_user@gmail.com
            password:
            Successfully logged in.

            >>> prism login --username user@example.com --password example_password
            Successfully logged in.

        Args:
            username (str): Cofactor Genomics account username
            password (str): Cofactor Genomics account password
        """

        @catch_errors
        def inner(username, password):
            if username == "":
                username = input("username: ")
            if password == "":
                password = getpass()
            if API.login(username=username, password=password):
                return "Successfully logged in."

        return inner(username, password)

    def logout(self):
        """
        Logout and close session.

        Examples:
            >>> prism logout
            logged out.
        """

        @catch_errors
        def inner():
            API().logout()
            return "logged out."

        return inner()

    def status(self, project: str = ""):
        """
        Display statuses and information for one or all projects.

        Examples:
            >>> prism status
            ╒════╤════════════════╤═══════════╤══════════════════╤═══════════════╤═══════════════════╕
            │    │ Project Name   │ Disease   │ Groups           │ Status        │   Uploaded Fastqs │
            ╞════╪════════════════╪═══════════╪══════════════════╪═══════════════╪═══════════════════╡
            │  0 │ test_project   │           │                  │ not submitted │                 6 │
            ├────┼────────────────┼───────────┼──────────────────┼───────────────┼───────────────────┤
            │  1 │ test_project2  │ DLBC      │ ['GRP1']         │ fail          │                 4 │
            ├────┼────────────────┼───────────┼──────────────────┼───────────────┼───────────────────┤
            │  2 │ test_project3  │ BRCA      │ ['GRP2', 'GRp1'] │ success       │                 6 │
            ╘════╧════════════════╧═══════════╧══════════════════╧═══════════════╧═══════════════════╛
        Args:
            project (str): Project name.
        """

        @catch_errors
        def inner(project_id):
            api = API()
            projects = api.projects().get("projects", {})
            async_requests = []
            if project_id != "" and project_id not in projects:
                raise ValueError(f"Project: {project_id} not found")
            for project in projects:
                if project_id and project != project_id:
                    continue
                async_requests.append(f"info/{project}")
                async_requests.append(f"uploads/{project}")
                async_requests.append(f"execution_status/{project}")
            results = api.execute_async(async_requests)
            table = []
            for project in projects:
                if project_id and project != project_id:
                    continue
                row = []
                row.append(project)
                row.append(results.get(f"info/{project}", {}).get("disease"))
                groupings = list(
                    results.get(f"info/{project}", {}).get("groupings", {}).keys()
                )
                row.append(groupings or None)
                row.append(
                    results.get(f"execution_status/{project}", {}).get(
                        "pipeline_status", "not_started"
                    )
                )
                row.append(
                    len(results.get(f"uploads/{project}", {}).get("uploads", []))
                )
                table.append(row)
            headers = ["Project Name", "Disease", "Groups", "Status", "Uploaded Fastqs"]
            return tabulate(
                table,
                headers=headers,
                showindex=range(1, len(table) + 1),
                tablefmt="fancy_grid",
            )

        return inner(project)

    def fastqs(self, project: str):
        """
        List fastqs for specified project in Cofactor Genomics' cloud storage.

        Examples:
            >>> prism fastqs project_name
            ╒════╤═══════════════════════════════════╤═══════════════════════════════╤═══════════╕
            │    │ Fastq                             │ Last Modified                 │   Size MB │
            ╞════╪═══════════════════════════════════╪═══════════════════════════════╪═══════════╡
            │  0 │ 5-PBCM-SM-2-11M.txt.gz            │ Mon, 08 Jun 2020 06:38:22 GMT │       436 │
            ├────┼───────────────────────────────────┼───────────────────────────────┼───────────┤
            │  1 │ 6-PBCM-SM-2-11M.txt.gz            │ Mon, 08 Jun 2020 06:46:47 GMT │       436 │
            ├────┼───────────────────────────────────┼───────────────────────────────┼───────────┤
            │  2 │ TG19DH-pos1a_10M_sequence.txt.gz  │ Mon, 08 Jun 2020 06:19:41 GMT │       446 │
            ├────┼───────────────────────────────────┼───────────────────────────────┼───────────┤
            │  3 │ TG19DH-pos1a_10M_sequence1.txt.gz │ Mon, 08 Jun 2020 06:15:21 GMT │       446 │
            ├────┼───────────────────────────────────┼───────────────────────────────┼───────────┤
            │  4 │ TG19DH-pos1a_10M_sequence2.txt.gz │ Mon, 08 Jun 2020 06:11:26 GMT │       446 │
            ├────┼───────────────────────────────────┼───────────────────────────────┼───────────┤
            │  5 │ TG19DH-pos1a_10M_sequence3.txt.gz │ Mon, 08 Jun 2020 06:04:06 GMT │       446 │
            ╘════╧═══════════════════════════════════╧═══════════════════════════════╧═══════════╛
            

        Args:
            project (str): Project name, must not include special characters.
        """

        @catch_errors
        def inner(project):
            api = API()
            uploads = api.uploads(project).get("uploads", {})
            table = []
            for upload in uploads:
                row = []
                row.append(upload.get("Key", "").split("/")[-1])
                row.append(upload.get("LastModified"))
                row.append(upload.get("Size", 0) // 1000000)
                table.append(row)
            headers = ["Fastq", "Last Modified", "Size MB"]
            return tabulate(
                table,
                headers=headers,
                showindex=range(1, len(table) + 1),
                tablefmt="fancy_grid",
            )

        return inner(project)

    def upload(self, local_directory: str, project: str):
        """ 
        Upload fastqs to Cofactor Genomics' cloud storage.

        Only files types withe the suffixes (txt.gz, fastq.gz, fq.gz) will be uploaded. local_directory is assummed to contain all the fastqs that will be uploaded to Cofactor Genomics' cloud storage.
        
        Examples:
            >>> prism upload /home/dir project_name
            Upload complete: TG19DH-pos1a_10M_sequence.txt.gz              progress: (100.00%)   |||||||||||||||||||||||||||||||||||||||||||||||||| 446/446MB

        Args:
            project (str): Project name. Special characters not allowed. Only [A-Z][a-z][0-9] and underscores '_' and hyphens '-' and periods '.' are allowed for project name.
            local_directory (str): local directory containing the fastq files
        """

        @catch_errors
        def inner(directory, project):
            validate_project_name(project)
            p = Path(directory).resolve()
            if not p.exists() or not p.is_dir():
                raise Exception(
                    f"Please double check {p.as_posix()} exists and is a directory"
                )
            files = [x for x in p.glob("**/*") if x.is_file() and verify_file_type(x)]
            api = API()
            creds = api.get_temp_creds(project)
            s3 = S3(company=api.db.company_name, project_id=project, creds=creds)
            s3.upload_files(files)
            return

        return inner(local_directory, project)

    def delete(self, project: str, file_name: str):
        """
        Delete an uploaded fastq file from Cofactor Genomics' cloud storage.

        Examples:
        >>> prism delete test_project
        """

        @catch_errors
        def inner(project, file_name):
            api = API()
            creds = api.get_temp_creds(project)
            s3 = S3(company=api.db.company_name, project_id=project, creds=creds)
            s3.remove_file(file_name)
            return

        return inner(project, file_name)

    def submit(self, project: str, groupings: str = "", disease: str = ""):
        """ 
        Submit analysis for specified project.

        A submition for a project can only be done once. If an error was made a new project will need to be created in order to run the run the analysis correctly. 
        Groupings argument is a JSON representation of how the fastqs should be grouped for analysis.
        Ex: '{"GRP1": ["fastqs1.txt.gz", "fastqs1.txt.gz", ...], "GRP2": ["fastqs3.txt.gz", "fastqs4.txt.gz", ...]}'
        Note the single quote at the beginning and end of the json.
        The fastq names should correspond to the names of the fastq files upload to Cofactor Genomics' cloud storage. 
        To see the fastq files uploaded for each project, use the `prism fastqs <PROJECT>` command.

        If no groupings argument is supplied, or each group has three or less fastqs listed in the array, a group report will NOT be generated. 
        In that case only individual sample reports for each fastq wil be generated.

        Disease argument is the disease code. If the submit command is run without a disease argument, a prompt will list all the available disease codes to pass as argument.

        Examples:
            >>> prism submit project_name --groupings='{"GRP1": ["fastqs1.txt.gz", "fastqs1.txt.gz"], "GRP2": ["fastqs3.txt.gz", "fastqs4.txt.gz"]}' --disease==disease_code
            Submitted project project_name. Use `status project_name` command to view status.

        Args:
            project (str): Project name, must not include special characters.
            groupings (str): JSON string that represents how the fastqs should be groupped for the biomarker report
            disease (str): disease code associated with fastq samples.

        """

        @catch_errors
        def inner(project, groupings, disease):
            disease = disease.upper()
            api = API()
            diseases = api.diseases()
            disease_list = []
            disease_code_list = []
            for code, name in diseases.items():
                disease_list.append(name)
                disease_code_list.append(code)
            if disease == "":
                headers = ["Disease Code", "Diseases"]
                row = zip(disease_code_list, disease_list)
                print(tabulate(row, headers=headers, tablefmt="fancy_grid"))

                class NumberValidator(Validator):
                    def validate(self, document):
                        text = document.text.upper()
                        if text and text not in disease_code_list:
                            i = 0
                            for i, c in enumerate(text):
                                if not c.isdigit():
                                    break
                            raise ValidationError(
                                message="Invalid input value, choose from Disease Codes. Ex: OTHR",
                                cursor_position=i,
                            )

                disease_code = prompt(
                    "Please choose disease code: ", validator=NumberValidator(),
                )

            else:
                if disease not in diseases:
                    raise ValueError(
                        f"Invalid disease provided: {disease}. Choose disease code from {dict(zip(disease_code_list, disease_list))}"
                    )
                disease_code = disease

            if groupings == "":
                fastqs = [
                    upload.get("Key", "").split("/")[-1]
                    for upload in api.uploads(project).get("uploads", {})
                ]
                groupings = {"GRP1": fastqs}
            validated = api.groupings(project, groupings)
            if validated.get("status") == "success":
                resp = api.execute_pipeline(project, groupings, disease_code)
                return f"Submitted project: {project}. Use `status {project}` command to view status."

        return inner(project, groupings, disease)

    def download(self, project: str, local_directory: str):
        """
        Download results into local_directory.

        Examples:
            >>> prism download upload_test /home/project_folder
            Downloaded: project_test_raw_all_values.csv
            Downloaded: TG19DH-pos1a_10M_sequence1_sample_report.pdf
        """

        @catch_errors
        def inner(project, local_directory):
            p = Path(local_directory).resolve()
            if not p.exists() or not p.is_dir():
                raise Exception(
                    f"Please double check {p.as_posix()} exists and is a directory"
                )
            api = API()
            results = api.results(project)
            if (
                not results.get("group_reports")
                and not results.get("sample_reports")
                and not results.get("data")
            ):
                print("No files to download.")
            else:
                for result in recurse_object(results):
                    path = Path(local_directory) / result[1]
                    download_file(result[0], path.as_posix())
                    print(f"Downloaded: {result[1]}")
            return

        return inner(project, local_directory)


def wrapper():
    if os.getenv("PRISM_ENV") == "DEV":
        logging.basicConfig(level=logging.INFO)
    fire.Fire(PrismCLI())


if __name__ == "__main__":
    wrapper()
