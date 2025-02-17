from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class APIHandlerBase(ABC):
    token: str

    @abstractmethod
    def retrieve_data(self, url: str, params: dict, headers: dict) -> dict | None:
        pass

    @property
    @abstractmethod
    def headers(self) -> dict:
        pass

    @property
    @abstractmethod
    def base_url(self) -> str:
        pass
