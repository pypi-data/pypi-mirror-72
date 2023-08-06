from .exceptions import InvalidCredentials, NotLoggedIn
from typing import Union

import requests


def catch_error(resp: requests.Response, service="prism") -> requests.Response:
    """[summary]

    Args:
        resp (requests.Response): [description]
        service (str, optional): [description]. Defaults to "prism".

    Raises:
        NotLoggedIn: [description]
        InvalidCredentials: [description]
        e: [description]

    Returns:
        requests.resp: [description]
    """
    try:
        resp.raise_for_status()
        return resp
    except requests.exceptions.HTTPError as e:
        if resp.status_code in (402,):
            return resp
        elif resp.status_code in (400,):
            raise NotLoggedIn
        elif resp.status_code in (502, 403):
            raise InvalidCredentials
        elif resp.status_code != 200:
            raise e
        # if service == "auth":
        #     pass
        # elif service == "prism":
        #     pass
