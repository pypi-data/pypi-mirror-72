from cfg_cli.clients.db import DB
from cfg_cli.errors.error_handling import catch_error
from concurrent.futures import as_completed, ThreadPoolExecutor
from typing import Dict, List

import cfg_cli.config as config
import logging
import requests
import time


class API:

    """
    API Interface.
    Communicates with remote webserver using http requests.
    """

    db = DB()
    api_url = config.api_url

    @staticmethod
    def login(username, password) -> bool:
        payload = {"username": username, "password": password}
        resp = requests.post(f"{API.api_url}/auth/token", json=payload)
        token = catch_error(resp, service="auth").json()
        API.db.access_token = token["access_token"]
        API.db.refresh_token = resp.cookies["refresh_token"]
        return True

    @staticmethod
    def refresh():
        s = requests.Session()
        s.cookies["refresh_token"] = API.db.refresh_token
        resp = s.get(f"{API.api_url}/auth/refresh")
        logging.info(f"REFRSH RESP {resp}")
        token = catch_error(resp, service="auth").json()
        API.db.access_token = token["access_token"]
        API.db.refresh_token = resp.cookies["refresh_token"]
        return True

    def logout(self) -> bool:
        resp = self._request("PUT", "auth", "logout")
        if resp.get("status") == "success":
            API.db.reset()
            return True

    def _request(self, method, service, endpoint, payload=None) -> Dict:
        self.access_token = API.db.access_token
        self.refresh_token = API.db.refresh_token
        endpoint = endpoint.rstrip("/")
        headers = {"Authorization": f"Bearer {self.access_token}"}
        resp = requests.request(
            method, f"{API.api_url}/{service}/{endpoint}", json=payload, headers=headers
        )
        resp = catch_error(resp)
        if resp.status_code == 402:
            logging.info("refreshing tokens", self.access_token)
            API.refresh()
            time.sleep(0.1)
            return self._request(method, service, endpoint, payload)
        logging.info(f" - REQUEST, {service}, {endpoint}, {resp.status_code}")
        return resp

    def get_temp_creds(self, project) -> Dict:
        return self._request("GET", "prism", f"aws_token/{project}").json()

    def projects(self) -> Dict:
        return self._request("GET", "prism", "projects").json()

    def completed_projects(self) -> Dict:
        return self._request("GET", "prism", "completed_projects").json()

    def uploads(self, project) -> Dict:
        return self._request("GET", "prism", f"uploads/{project}").json()

    def results(self, project) -> Dict:
        return self._request("GET", "prism", f"results/{project}").json()

    def info(self, project) -> Dict:
        return self._request("GET", "prism", f"info/{project}").json()

    def diseases(self) -> Dict:
        return self._request("GET", "prism", "diseases").json()

    def groupings(self, project, groupings) -> Dict:
        return self._request(
            "POST", "prism", f"groupings/{project}", payload={"groupings": groupings}
        ).json()

    def execute_pipeline(self, project, groupings, disease) -> Dict:
        return self._request(
            "POST",
            "prism",
            f"execute_pipeline/{project}",
            payload={"groupings": groupings, "disease": disease},
        ).json()

    def execution_status(self, project) -> Dict:
        return self._request("GET", "prism", f"execution_status/{project}").json()

    def results(self, project) -> Dict:
        return self._request("GET", "prism", f"results/{project}").json()

    def execute_async(self, async_requests: List[str]) -> Dict:
        """
        Execute multiple api calls asynchronously
        with multithreading.
        """

        data = {}
        if len(async_requests) > 0:
            with ThreadPoolExecutor(max_workers=len(async_requests)) as executor:
                futures = {
                    executor.submit(self._request, "GET", "prism", endpoint): endpoint
                    for endpoint in async_requests
                }
                for future in as_completed(futures):
                    endpoint = futures[future]
                    try:
                        data.update({endpoint: future.result().json()})
                    except Exception as e:
                        logging.info("Async execution error:", e)
        return data
