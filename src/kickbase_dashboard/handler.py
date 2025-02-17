import os
import json
import base64
import requests
import time
from dataclasses import dataclass
from wyscout_api.spinner.Spinner import Spinner
from wyscout_api.hudl.base import APIHandlerBase


@dataclass(frozen=True)
class APIHandler(APIHandlerBase):
    username: str
    password: str
    max_trials: int = 3
    retry_seconds: float = 0.1

    def retrieve_data(
        self, url: str, params: dict, headers: dict, n_trial=0
    ) -> dict | None:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            if n_trial > 0:
                print("✅")
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}", end=" ")
            if n_trial < self.max_trials:
                print(f"Retrying in {self.retry_seconds} seconds...")
                time.sleep(self.retry_seconds)
                return self.retrieve_data(url, params, headers, n_trial + 1)
            print(f"Max number of trials reached ({n_trial}).")
            return None

    def retrieve_areas(self):
        return self.retrieve_data(
            os.path.join(self.base_url, "areas"),
            {},
            self.headers,
        )

    @property
    def headers(self):
        auth = base64.b64encode(f"{self.username}:{self.password}".encode())
        return {"Authorization": f"Basic {auth.decode()}"}

    @property
    def base_url(self):
        return "https://apirest.wyscout.com/v4"
