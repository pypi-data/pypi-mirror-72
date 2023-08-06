from concurrent.futures import as_completed, ThreadPoolExecutor
from src.clients.db import DB
from src.errors.error_handling import catch_error
from typing import Dict, List

import logging
import requests
import src.config as config


class API:

    """
    API Interface.
    Communicates with remote webserver using http requests.
    """

    db = DB()
    api_url = config.api_url

    def __init__(self):
        self.access_token = API.db.access_token
        self.refresh_token = API.db.refresh_token

    @staticmethod
    def login(username, password) -> bool:
        payload = {"username": username, "password": password}
        resp = requests.post(f"{API.api_url}/auth/token", json=payload)
        token = catch_error(resp, service="auth")
        API.db.access_token = token["access_token"]
        API.db.refresh_token = resp.cookies["refresh_token"]
        return True

    def _request(self, method, service, endpoint, payload=None) -> Dict:
        endpoint = endpoint.rstrip("/")
        headers = {"Authorization": f"Bearer {self.access_token}"}
        resp = requests.request(
            method, f"{API.api_url}/{service}/{endpoint}", json=payload, headers=headers
        )
        if resp.status_code == 402:
            logging.info("refreshing tokens", self.access_token)
            self._refresh()
            self._request(method, service, endpoint, payload)
        logging.info(f" - REQUEST, {service}, {endpoint}, {resp.status_code}")
        return catch_error(resp)

    def logout(self) -> bool:
        resp = self._request("PUT", "auth", "logout")
        if resp.get("status") == "success":
            API.db.reset()
            return True

    @staticmethod
    def refresh():
        s = requests.Session()
        s.cookies["refresh_token"] = API.db.refresh_token
        resp = s.get(f"{API.api_url}/auth/refresh")
        resp.raise_for_status()
        token = resp.json()
        API.db.access_token = token["access_token"]
        API.db.refresh_token = resp.cookies["refresh_token"]
        return True

    def _refresh(self):
        API.refresh()
        self.access_token = self.db.access_token
        self.refresh_token = self.db.refresh_token

    def get_temp_creds(self, project) -> Dict:
        return self._request("GET", "prism", f"aws_token/{project}")

    def projects(self) -> Dict:
        return self._request("GET", "prism", "projects")

    def completed_projects(self) -> Dict:
        return self._request("GET", "prism", "completed_projects")

    def uploads(self, project) -> Dict:
        return self._request("GET", "prism", f"uploads/{project}")

    def results(self, project) -> Dict:
        return self._request("GET", "prism", f"results/{project}")

    def info(self, project) -> Dict:
        return self._request("GET", "prism", f"info/{project}")

    def diseases(self) -> Dict:
        return self._request("GET", "prism", "diseases")

    def groupings(self, project, groupings) -> Dict:
        return self._request(
            "POST", "prism", f"groupings/{project}", payload={"groupings": groupings}
        )

    def execute_pipeline(self, project, groupings, disease) -> Dict:
        return self._request(
            "POST",
            "prism",
            f"execute_pipeline/{project}",
            payload={"groupings": groupings, "disease": disease},
        )

    def execution_status(self, project) -> Dict:
        return self._request("GET", "prism", f"execution_status/{project}")

    def results(self, project) -> Dict:
        return self._request("GET", "prism", f"results/{project}")

    def execute_async(self, async_requests: List[str]) -> Dict:
        """
        Execute multiple api calls asynchronously
        with multithreading.
        """

        with ThreadPoolExecutor(max_workers=len(async_requests)) as executor:
            futures = {
                executor.submit(self._request, "GET", "prism", endpoint): endpoint
                for endpoint in async_requests
            }
            data = {}
            for future in as_completed(futures):
                endpoint = futures[future]
                try:
                    data.update({endpoint: future.result()})
                except Exception as e:
                    logging.info("Async execution error:", e)
        return data
