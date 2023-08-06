import requests
from typing import Union

from .exceptions import InvalidCredentials, NotLoggedIn


def catch_error(resp: requests.Response, service="prism") -> requests.Response:
    """Handle errors from backend api

    Args:
        resp (requests.Response): Response from backend api
        service (str, optional): what service is returning this response

    Raises:
        NotLoggedIn: Not logged in error
        InvalidCredentials: Invalid crednetilas error
        e: return original error if response status code is not 200

    Returns:
        requests.resp: if status code is 200 reutrn original response
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
