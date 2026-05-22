"""
Singleton Logger — înregistrează mesaje într-un fișier text.

Clasa Log urmează pattern-ul Singleton: poate exista o singură instanță per aplicație.
"""
import os
from typing import Optional


class Log:
    """
    Logger Singleton.

    Utilizare:
        log = Log("output.log")          # prima instanță
        log2 = Log.get_instance()        # aceeași instanță
        log.write("mesaj")
    """

    _instance: Optional["Log"] = None

    def __init__(self, fname: str) -> None:
        """
        Creează instanța Singleton cu fișierul [fname].

        Pre-condiții: nu există deja o instanță (Log._instance is None).
        Aruncă Exception("Clasa este un singleton") dacă o instanță există deja.

        La creare, dacă fișierul [fname] există deja, îl șterge (log nou la fiecare rulare).
        """
        # TODO: De implementat
        raise NotImplementedError("De implementat")

    def write(self, line: str) -> None:
        """
        Adaugă [line] + newline la fișierul log.
        """
        # TODO: De implementat
        raise NotImplementedError("De implementat")

    @staticmethod
    def get_instance() -> "Log":
        """
        Returnează instanța existentă.
        Aruncă Exception("Nu există instanță Log") dacă nu a fost creată nicio instanță.
        """
        # TODO: De implementat
        raise NotImplementedError("De implementat")

    @staticmethod
    def reset() -> None:
        """
        Resetează instanța Singleton (util pentru teste).
        Setează Log._instance la None.
        """
        # TODO: De implementat
        raise NotImplementedError("De implementat")
