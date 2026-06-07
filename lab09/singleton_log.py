"""
Singleton Logger — înregistrează mesaje într-un fișier text.

Clasa Log urmează pattern-ul Singleton: poate exista o singură instanță per aplicație.
"""
import os
from typing import Optional


class Log:
    """
    Logger Singleton.
    """

    _instance: Optional["Log"] = None

    def __init__(self, fname: str) -> None:
        """
        Creează instanța Singleton cu fișierul [fname].
        """
        if Log._instance is not None:
            raise Exception("Clasa este un singleton")

        self.fname = fname

        # La creare, dacă fișierul [fname] există deja, îl șterge (log nou la fiecare rulare)
        if os.path.exists(self.fname):
            os.remove(self.fname)

        Log._instance = self

    def write(self, line: str) -> None:
        """
        Adaugă [line] + newline la fișierul log.
        """
        with open(self.fname, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    @staticmethod
    def get_instance() -> "Log":
        """
        Returnează instanța existentă.
        """
        if Log._instance is None:
            raise Exception("Nu există instanță Log")
        return Log._instance

    @staticmethod
    def reset() -> None:
        """
        Resetează instanța Singleton (util pentru teste).
        Setează Log._instance la None.
        """
        Log._instance = None