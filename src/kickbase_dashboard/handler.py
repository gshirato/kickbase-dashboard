import os
import json
import base64
import requests
import time
from dataclasses import dataclass
from kickbase_dashboard.base import APIHandlerBase


@dataclass(frozen=True)
class APIHandler(APIHandlerBase):
    token: str
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

    def retrieve_user_settings(self):
        return self.retrieve_data(
            os.path.join(self.base_url, "user", "settings"), {}, self.headers
        )

    def retrieve_leagues(self):
        return self.retrieve_data(
            os.path.join(self.base_url, "leagues", "selection"),
            {},
            self.headers,
        )

    def retrieve_league_overview(self, league_id: str):
        return self.retrieve_data(
            os.path.join(self.base_url, "leagues", league_id, "overview"),
            {},
            self.headers,
        )

    def retrieve_league_market(self, league_id: str):
        return self.retrieve_data(
            os.path.join(self.base_url, "leagues", league_id, "market"),
            {},
            self.headers,
        )

    def retrieve_league_ranking(self, league_id: str, day_number: str):
        return self.retrieve_data(
            os.path.join(self.base_url, "leagues", league_id, "ranking"),
            {"dayNumber": day_number},
            self.headers,
        )

    def retrieve_user_teamcenter(self, league_id: str, user_id: str, day_number: str):
        return self.retrieve_data(
            os.path.join(
                self.base_url, "leagues", league_id, "users", user_id, "teamcenter"
            ),
            {"dayNumber": day_number},
            self.headers,
        )

    def retrieve_user_profile(self, league_id: str, user_id: str):
        return self.retrieve_data(
            os.path.join(
                self.base_url, "leagues", league_id, "managers", user_id, "profile"
            ),
            {},
            self.headers,
        )

    def retrieve_user_squad(self, league_id: str, user_id: str):
        return self.retrieve_data(
            os.path.join(
                self.base_url, "leagues", league_id, "managers", user_id, "squad"
            ),
            {},
            self.headers,
        )

    def retrieve_user_performance(self, league_id: str, user_id: str):
        return self.retrieve_data(
            os.path.join(
                self.base_url, "leagues", league_id, "managers", user_id, "performance"
            ),
            {},
            self.headers,
        )

    def retrieve_user_transfers(self, league_id: str, user_id: str):
        return self.retrieve_data(
            os.path.join(
                self.base_url, "leagues", league_id, "managers", user_id, "transfer"
            ),
            {},
            self.headers,
        )

    def retrieve_league_player(self, league_id: str, player_id: str):
        return self.retrieve_data(
            os.path.join(self.base_url, "leagues", league_id, "players", player_id),
            {},
            self.headers,
        )

    def retrieve_league_player_marketvalue(
        self, league_id: str, player_id: str, timeframe: str
    ):
        """
        valid value for timeframe is 92 or 365
        -> 92 a quarter year in days
        -> 365 a full year in days
        depending which value is chosen it returns the history of the market value for the last 92 days or respectivly 365 days
        """
        return self.retrieve_data(
            os.path.join(
                self.base_url,
                "leagues",
                league_id,
                "players",
                player_id,
                "marketvalue",
                timeframe,
            ),
            {},
            self.headers,
        )

    def retrieve_league_player_performance(self, league_id: str, player_id: str):
        return self.retrieve_data(
            os.path.join(
                self.base_url, "leagues", league_id, "players", player_id, "performance"
            ),
            {},
            self.headers,
        )

    def retrieve_league_player_transfers(self, league_id: str, player_id: str):
        return self.retrieve_data(
            os.path.join(
                self.base_url, "leagues", league_id, "players", player_id, "transfers"
            ),
            {},
            self.headers,
        )

    def retrieve_league_player_transfer_history(
        self, league_id: str, player_id: str, start: str
    ):
        return self.retrieve_data(
            os.path.join(
                self.base_url,
                "leagues",
                league_id,
                "players",
                player_id,
                "transferHistory",
            ),
            {"start": start},
            self.headers,
        )

    def retrieve_scouted_players(self, league_id: str):
        return self.retrieve_data(
            os.path.join(self.base_url, "leagues", league_id, "scoutedplayers"),
            {},
            self.headers,
        )

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.token}", "accept": "application/json"}

    @property
    def base_url(self):
        return "https://api.kickbase.com/v4"
