#!/usr/bin/env python3

from getpass import getpass
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.validation import ValidationError, Validator
from requests.exceptions import HTTPError
from src.clients.api import API
from src.clients.db import DB
from src.clients.s3 import S3
from src.utils import (download_file, recuse_object, validate_project_name,
                       verify_file_type)
from tabulate import tabulate

import fire
import functools
import json
import logging
import os


def catch_errors(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if os.getenv("APP_ENV") == "LOCAL":
                logging.exception(e)
            if isinstance(e, HTTPError) and e.response.json().get("message"):
                raise fire.core.FireError(Exception(e.response.json().get("message")))
            raise fire.core.FireError(e)

    return inner


class CFG_CLI(object):
    def login(self):
        """
        Login and create session. 

        Ex. `cfg login`
        Login in with your email and password.
        """

        @catch_errors
        def inner():
            username = input("username: ")
            password = getpass()
            API.login(username=username, password=password)

        inner()

    def logout(self):
        """
        Logout and close session.

        Ex. `cfg logout`
        """

        @catch_errors
        def inner():
            API().logout()

        inner()

    def status(self, project: str = ""):
        """
        Display statuses and information for one or all projects.

        Ex. `cfg status`
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
            print(
                tabulate(
                    table, headers=headers, showindex="always", tablefmt="fancy_grid"
                )
            )

        inner(project)

    def fastqs(self, project: str = ""):
        """ 
        List fastqs for specified project in Cofactor Genomics' cloud storage.

        Ex. `cfg fastqs project_name`
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
            print(
                tabulate(
                    table, headers=headers, showindex="always", tablefmt="fancy_grid"
                )
            )

        inner(project)

    def upload(self, directory: str, project: str = ""):
        """ 
        Upload fastqs to Cofactor Genomics' cloud storage.

        Ex. `cfg upload /home/dir project_name`
        /home/dir dir is assummed to contain all the fastqs that will be uploaded to Cofactor Genomics' cloud storage.
        Special characters not allowed. Only [A-Z][a-z][0-9] and underscores '_' and hyphens '-' and periods '.' are allowed for project name.
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

        inner(directory, project)

    def delete(self, project: str, file_name: str):
        """
        Delete an uploaded fastq file from Cofactor Genomics' cloud storage.
        """

        @catch_errors
        def inner(project, file_name):
            api = API()
            creds = api.get_temp_creds(project)
            s3 = S3(company=api.db.company_name, project_id=project, creds=creds)
            s3.remove_file(file_name)
            return True

        inner(project, file_name)

    def submit(self, project: str, groupings: str = "", disease: str = ""):
        """ 
        Submit analysis for specified project.

        Ex. `cfg submit project_name --groupings='{"GRP1": ["fastqs1.txt.gz", "fastqs1.txt.gz"], "GRP2": ["fastqs3.txt.gz", "fastqs4.txt.gz"]}' --disease==disease_code`
        Groupings argument is a json representation of how the fastqs should be grouped for analysis.
        Ex: '{"GRP1": ["fastqs1.txt.gz", "fastqs1.txt.gz", ...], "GRP2": ["fastqs3.txt.gz", "fastqs4.txt.gz", ...]}'
        Note the single quote ' at the beginning and end of the json.
        The fastq names should correspond to the names of the fastq files upload to Cofactor Genomics' cloud storage. 
        To see the fastq files uploaded for each project, use the `cfg fastqs <PROJECT>` command.

        If no groupings argument is supplied or each group has 3 or less fastqs listed in the array, a group report will NOT be generated. 
        In that case only individual sample reports for each fastq wil be generated.

        Disease argument is the disease code. If the submit command is run without a disease argument a prompt will list all the available disease codes to pass as argument.
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
                    "Enter disease code of associated disese: ",
                    validator=NumberValidator(),
                )

            else:
                if disease not in diseases:
                    raise ValueError(
                        f"Invalid disease provided: {disease}. Choose disease code from {dict(zip(disease_code_list, disease_list))}"
                    )

            validated = api.groupings(project, groupings)
            if validated.get("status") == "success":
                api.execute_pipeline(project, groupings, disease_code)

        inner(project, groupings, disease)

    def download(self, project: str, destination: str):
        """
        Download results into specified destination folder.

        Ex. `cfg download upload_test /home/project_folder`
        """

        @catch_errors
        def inner(project, destination):
            p = Path(destination).resolve()
            if not p.exists() or not p.is_dir():
                raise Exception(
                    f"Please double check {p.as_posix()} exists and is a directory"
                )
            api = API()
            results = api.results(project)
            for result in recuse_object(results):
                path = Path(destination) / result[1]
                download_file(result[0], path.as_posix())
                print(f"Downloaded: {result[1]}")

        inner(project, destination)


def wrapper():
    if os.getenv("APP_ENV") == "LOCAL":
        logging.basicConfig(level=logging.INFO)
    fire.Fire(CFG_CLI())


if __name__ == "__main__":
    wrapper()
