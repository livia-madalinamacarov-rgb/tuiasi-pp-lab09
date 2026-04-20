"""
Tema 3 — Proxy cu caching pentru cereri HTTP GET

RealHTTPClient   — face cereri reale cu requests.get()
CachingHTTPProxy — proxy care verifică/actualizează un cache în fișier text

Format cache (câte o linie JSON per intrare):
  {"url": "...", "timestamp": 1713000000.0, "raspuns": "..."}

O intrare e validă dacă timestamp-ul nu a depășit DURATA_CACHE_SECUNDE față
de momentul curent.
"""

from abc import ABC, abstractmethod
import json
import time
from typing import Optional

import requests


class HTTPClient(ABC):
    @abstractmethod
    def get(self, url: str) -> str:
        raise NotImplementedError("De implementat")


class RealHTTPClient(HTTPClient):
    """
    Realizează cererea HTTP reală.
    Returnează response.text (conținutul ca string).
    """

    def get(self, url: str) -> str:
        # TODO: Apelează requests.get(url) și returnează .text
        raise NotImplementedError("De implementat")


class CachingHTTPProxy(HTTPClient):
    """
    Proxy față de un HTTPClient real.

    Logică get(url):
      1. Citește cache-ul din fișier.
      2. Dacă există o intrare pentru url și nu a expirat → returnează răspunsul din cache.
      3. Dacă există dar a expirat → apelează clientul real, actualizează intrarea, scrie cache-ul.
      4. Dacă nu există → apelează clientul real, adaugă intrarea, scrie cache-ul.
    """

    DURATA_CACHE_SECUNDE: float = 3600.0  # 1 oră

    def __init__(self, client: HTTPClient, fisier_cache: str = "cache.txt") -> None:
        # TODO: Salvează self._client și self._fisier_cache
        raise NotImplementedError("De implementat")

    def get(self, url: str) -> str:
        # TODO: De implementat conform descrierii de mai sus
        raise NotImplementedError("De implementat")

    def _citeste_cache(self) -> list[dict]:
        # TODO: Deschide self._fisier_cache (dacă există) și parsează fiecare linie ca JSON.
        # Returnează lista de dicționare; dacă fișierul nu există, returnează [].
        raise NotImplementedError("De implementat")

    def _scrie_cache(self, intrari: list[dict]) -> None:
        # TODO: Scrie fiecare intrare din listă ca o linie JSON în self._fisier_cache.
        raise NotImplementedError("De implementat")

    def _este_valida(self, intrare: dict) -> bool:
        # TODO: Returnează True dacă time.time() - intrare["timestamp"] < DURATA_CACHE_SECUNDE
        raise NotImplementedError("De implementat")
