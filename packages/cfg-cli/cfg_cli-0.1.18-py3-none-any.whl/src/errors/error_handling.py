from .exceptions import InvalidCredentials, NotLoggedIn

import requests


def catch_error(resp: requests.Response, service="prism") -> Exception:
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if service == "auth":
            if resp.status_code in (400,):
                raise NotLoggedIn
            elif resp.status_code in (502, 403):
                raise InvalidCredentials
            else:
                raise e
        elif service == "prism":
            if resp.status_code in (400,):
                raise NotLoggedIn
            else:
                raise e
        else:
            raise e
    return resp.json()
