from cfg_cli.utils import parse_jwt_access_token
from pathlib import Path

import shelve


class DB:
    """
    DB is an interface for local persistant storage of JSON
    web tokens.
    """

    def __init__(self, db="creds", store="jwt"):
        self.parent = f"{Path.home()}/.cfg"
        Path(self.parent).mkdir(mode=0o774, parents=True, exist_ok=True)
        self.db = f"{self.parent}/{db}"
        self.store = store

    def _get_value(self, val) -> str:
        with shelve.open(self.db) as db:
            store = db.get(self.store)
            if store is not None:
                return store.get(val)

    def _put_value(self, key, value):
        with shelve.open(self.db) as db:
            store = db.get(self.store)
            if store is not None:
                store.update(
                    {key: value,}
                )
            else:
                store = {key: value}
            db[self.store] = store
            return True

    @property
    def access_token(self) -> str:
        return self._get_value("access_token")

    @property
    def refresh_token(self) -> str:
        return self._get_value("refresh_token")

    @property
    def company_name(self) -> str:
        return self._get_value("company_name")

    @access_token.setter
    def access_token(self, access_token):
        if len(access_token.split(".")) == 3:
            self._put_value("company_name", parse_jwt_access_token(access_token))
        self._put_value("access_token", access_token)

    @refresh_token.setter
    def refresh_token(self, refresh_token):
        self._put_value("refresh_token", refresh_token)

    def token_exists(self) -> bool:
        with shelve.open(self.db) as db:
            return db.get(self.store) is not None

    def reset(self) -> bool:
        with shelve.open(self.db) as db:
            db[self.store] = None
            return True
