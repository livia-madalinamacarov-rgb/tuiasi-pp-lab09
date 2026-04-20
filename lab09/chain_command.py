"""
Tema 1 — Lanț de responsabilități (CoR) + Comandă (Command)

Aplicația primește conținutul unui fișier fără extensie și determină tipul
(Kotlin / Python / Bash / Java) pe baza conținutului, apoi îl execută.
"""

from abc import ABC, abstractmethod
from typing import Optional


class FileTypeHandler(ABC):
    """
    Baza lanțului de responsabilități.
    Fiecare handler concret determină un singur tip de fișier.
    Dacă nu recunoaște conținutul, pasează mai departe în lanț.
    """

    def __init__(self) -> None:
        self._next: Optional["FileTypeHandler"] = None

    def set_next(self, handler: "FileTypeHandler") -> "FileTypeHandler":
        # TODO: Salvează referința la următorul handler și returnează-l
        # (permite înlănțuirea: h1.set_next(h2).set_next(h3))
        raise NotImplementedError("De implementat")

    @abstractmethod
    def handle(self, continut: str) -> Optional[str]:
        # TODO: Încearcă să determine tipul fișierului din conținut.
        # Dacă reușește → returnează tipul ('kotlin', 'python', 'bash', 'java').
        # Dacă nu → apelează self._next.handle(continut) dacă există next,
        # altfel returnează None.
        raise NotImplementedError("De implementat")


class KotlinHandler(FileTypeHandler):
    """
    Recunoaște cod Kotlin.
    Hint: caută cuvinte cheie specifice: fun, val, var, when, println
    sau tipuri Kotlin (Int, String, List, etc.).
    """

    def handle(self, continut: str) -> Optional[str]:
        # TODO: De implementat
        raise NotImplementedError("De implementat")


class PythonHandler(FileTypeHandler):
    """
    Recunoaște cod Python.
    Hint: shebang #!/usr/bin/env python, cuvinte cheie def, import,
    indentare, print(...).
    """

    def handle(self, continut: str) -> Optional[str]:
        # TODO: De implementat
        raise NotImplementedError("De implementat")


class BashHandler(FileTypeHandler):
    """
    Recunoaște cod Bash.
    Hint: shebang #!/bin/bash sau #!/usr/bin/env bash, echo, $variabile.
    """

    def handle(self, continut: str) -> Optional[str]:
        # TODO: De implementat
        raise NotImplementedError("De implementat")


class JavaHandler(FileTypeHandler):
    """
    Recunoaște cod Java.
    Hint: public class, System.out.println, import java., void main.
    """

    def handle(self, continut: str) -> Optional[str]:
        # TODO: De implementat
        raise NotImplementedError("De implementat")


# ---------------------------------------------------------------------------
# Pattern Comandă
# ---------------------------------------------------------------------------


class FileCommand(ABC):
    """
    Baza comenzilor de execuție.
    Fiecare comandă concretă știe cum să ruleze un anumit tip de fișier.
    """

    def __init__(self, continut: str) -> None:
        self.continut = continut

    @abstractmethod
    def executa(self) -> str:
        # TODO: Salvează conținutul într-un fișier temporar (tempfile),
        # execută-l cu subprocess.run() și returnează stdout-ul ca string.
        raise NotImplementedError("De implementat")


class KotlinCommand(FileCommand):
    """Execută conținut Kotlin cu `kotlinc-jvm` + `kotlin`."""

    def executa(self) -> str:
        # TODO: De implementat
        raise NotImplementedError("De implementat")


class PythonCommand(FileCommand):
    """Execută conținut Python cu `python3`."""

    def executa(self) -> str:
        # TODO: De implementat
        raise NotImplementedError("De implementat")


class BashCommand(FileCommand):
    """Execută conținut Bash cu `bash`."""

    def executa(self) -> str:
        # TODO: De implementat
        raise NotImplementedError("De implementat")


class JavaCommand(FileCommand):
    """Compilează cu `javac` și execută cu `java`."""

    def executa(self) -> str:
        # TODO: De implementat
        raise NotImplementedError("De implementat")


# ---------------------------------------------------------------------------
# Executor — combină CoR cu Command
# ---------------------------------------------------------------------------

_TIP_LA_COMANDA: dict[str, type[FileCommand]] = {
    "kotlin": KotlinCommand,
    "python": PythonCommand,
    "bash":   BashCommand,
    "java":   JavaCommand,
}


class FileExecutor:
    """
    Construiește lanțul CoR (Kotlin → Python → Bash → Java),
    detectează tipul fișierului și lansează comanda corespunzătoare.
    """

    def __init__(self) -> None:
        # TODO: Instanțiază handlere și înlănțuiește-le;
        # salvează primul handler ca self._lant.
        raise NotImplementedError("De implementat")

    def detecteaza_si_executa(self, continut: str) -> str:
        # TODO: Apelează self._lant.handle(continut) pentru a obține tipul.
        # Dacă tipul e None → ridică ValueError("Tip de fișier nerecunoscut").
        # Altfel → instanțiază comanda corespunzătoare și apelează executa().
        raise NotImplementedError("De implementat")
