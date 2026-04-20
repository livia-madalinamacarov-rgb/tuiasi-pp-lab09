"""
Tema 2 — Automat de sucuri: State Machine (STM) + Observer

Componente:
  TakeMoneySTM    — automat pentru introducerea banilor; notifică observerii
  SelectProductSTM — automat pentru selectarea produsului; notifică VendingMachineSTM
  VendingMachineSTM — entitate centrală; validează tranzacția
"""

from abc import ABC, abstractmethod
from typing import Optional


# ---------------------------------------------------------------------------
# Pattern Observer
# ---------------------------------------------------------------------------


class Observer(ABC):
    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        raise NotImplementedError("De implementat")


class Observable(ABC):
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def adauga_observer(self, observer: Observer) -> None:
        # TODO: Adaugă observer la lista internă self._observers
        raise NotImplementedError("De implementat")

    def elimina_observer(self, observer: Observer) -> None:
        # TODO: Elimină observer din self._observers (dacă există)
        raise NotImplementedError("De implementat")

    def notifica_observeri(self, *args, **kwargs) -> None:
        # TODO: Iterează self._observers și apelează update(*args, **kwargs) pe fiecare
        raise NotImplementedError("De implementat")


# ---------------------------------------------------------------------------
# TakeMoneySTM
# ---------------------------------------------------------------------------


class TakeMoneyState:
    ASTEPTARE = "ASTEPTARE"
    INTRODUCERE = "INTRODUCERE"


class TakeMoneySTM(Observable):
    """
    Stări: ASTEPTARE (inițial) → INTRODUCERE (după primul depozit de bani).
    La fiecare introdu_bani() notifică observerii cu suma curentă totală.
    Observerul implicit afișează la consolă suma introdusă.
    """

    def __init__(self) -> None:
        super().__init__()
        # TODO: Inițializează starea (TakeMoneyState.ASTEPTARE) și suma (0.0)
        raise NotImplementedError("De implementat")

    def introdu_bani(self, suma: float) -> None:
        # TODO: Adaugă suma la totalul curent, trece în starea INTRODUCERE,
        # notifică observerii cu suma curentă totală.
        raise NotImplementedError("De implementat")

    def returneaza_bani(self) -> float:
        # TODO: Returnează suma acumulată, resetează la 0.0, revine în ASTEPTARE.
        raise NotImplementedError("De implementat")

    def get_suma(self) -> float:
        # TODO: Returnează suma curentă fără modificare
        raise NotImplementedError("De implementat")

    def get_stare(self) -> str:
        # TODO: Returnează starea curentă
        raise NotImplementedError("De implementat")

    def reseteaza(self) -> None:
        # TODO: Suma ← 0.0, stare ← ASTEPTARE
        raise NotImplementedError("De implementat")


# ---------------------------------------------------------------------------
# SelectProductSTM
# ---------------------------------------------------------------------------


class SelectProductState:
    ASTEPTARE = "ASTEPTARE"
    SELECTARE = "SELECTARE"


class SelectProductSTM(Observable):
    """
    Stări: ASTEPTARE (inițial) → SELECTARE (produs ales).
    La selecteaza_produs() notifică observerii cu (nume_produs, pret).
    VendingMachineSTM se înregistrează ca observer aici.
    """

    def __init__(self) -> None:
        super().__init__()
        # TODO: Inițializează starea (SelectProductState.ASTEPTARE)
        # și produsul selectat (None)
        raise NotImplementedError("De implementat")

    def selecteaza_produs(self, produs: str, pret: float) -> None:
        # TODO: Salvează (produs, pret), trece în SELECTARE,
        # notifică observerii cu (produs, pret).
        raise NotImplementedError("De implementat")

    def get_produs_selectat(self) -> Optional[tuple[str, float]]:
        # TODO: Returnează (produs, pret) sau None dacă nimic nu e selectat
        raise NotImplementedError("De implementat")

    def get_stare(self) -> str:
        # TODO: Returnează starea curentă
        raise NotImplementedError("De implementat")

    def reseteaza(self) -> None:
        # TODO: Produs ← None, stare ← ASTEPTARE
        raise NotImplementedError("De implementat")


# ---------------------------------------------------------------------------
# VendingMachineSTM — entitate centrală + Observer pentru SelectProductSTM
# ---------------------------------------------------------------------------


class VendingMachineSTM(Observer):
    """
    Coordonează TakeMoneySTM și SelectProductSTM.
    Se înregistrează ca observer la SelectProductSTM pentru a valida tranzacția
    când un produs este selectat.
    """

    PRODUSE: dict[str, float] = {
        "Cola": 2.5,
        "Fanta": 2.5,
        "Apa": 1.5,
        "Suc de mere": 3.0,
    }

    def __init__(self) -> None:
        # TODO: Creează self.take_money_stm și self.select_product_stm.
        # Înregistrează self ca observer la self.select_product_stm.
        raise NotImplementedError("De implementat")

    def update(self, produs: str, pret: float) -> None:
        # TODO: Apelat de SelectProductSTM când un produs e selectat.
        # Verifică dacă tranzacția e validă (suma >= pret).
        # Comportament la validare/invalidare: la alegerea ta (ex. print mesaj).
        raise NotImplementedError("De implementat")

    def valideaza_tranzactie(self, produs: str, pret: float) -> bool:
        # TODO: Returnează True dacă suma curentă din take_money_stm >= pret
        raise NotImplementedError("De implementat")

    def calculeaza_rest(self, pret: float) -> float:
        # TODO: Returnează suma curentă minus pret
        raise NotImplementedError("De implementat")

    def finalizeaza_cumparare(self) -> float:
        # TODO: Calculează restul pe baza produsului selectat,
        # resetează ambele STM-uri, returnează restul.
        # Ridică ValueError dacă nu e selectat niciun produs.
        raise NotImplementedError("De implementat")
