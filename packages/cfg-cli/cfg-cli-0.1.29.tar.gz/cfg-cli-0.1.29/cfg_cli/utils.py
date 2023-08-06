from jose import jwk, jwt
from jose.utils import base64url_decode
from pathlib import Path

import requests
import time


def verify_file_type(file) -> bool:
    if isinstance(file, Path):
        file = file.as_posix()
    if (
        file.endswith(".txt.gz")
        or file.endswith(".fq.gz")
        or file.endswith(".fastq.gz")
    ):
        return True
    return False


def parse_jwt_access_token(token):
    """
    Return company name from jwt access token 
    """
    try:
        claims = jwt.get_unverified_claims(token)
        for claim in claims["cognito:groups"]:
            if claim.startswith("company:"):
                return claim.split("company:")[-1]
    except:
        return "None"


def validate_project_name(project_name):
    illegals = (
        " ",
        "<",
        ">",
        "{",
        "}",
        "[",
        "]",
        "?",
        "*",
        '"',
        "#",
        "%",
        "\\",
        "^",
        "|",
        "~",
        "`",
        "$",
        "&",
        ",",
        ";",
        ":",
        "/",
    )
    for illegal in illegals:
        if illegal in project_name:
            raise ValueError(
                f"Illegal character in projects name: '{illegal}'. Please rename your project without invalid characters."
            )


def recurse_object(d: dict):
    for k, v in d.items():
        if isinstance(v, dict):
            yield from recurse_object(v)
        elif v.startswith("http"):
            yield (v, v.split("?")[0].split("/")[-1])


def download_file(url, local_filename):
    # local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return True
