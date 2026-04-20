"""
Teste pentru Lab 9 — Design Patterns în Python.

Acoperă:
  - Tema 1: Chain of Responsibility + Command (chain_command.py)
  - Tema 2: State Machine + Observer (vending_machine.py)
  - Tema 3: Proxy cu caching HTTP (http_proxy.py)
"""

import json
import os
from unittest.mock import MagicMock

import pytest

from lab09.chain_command import (
    BashHandler,
    FileExecutor,
    JavaHandler,
    KotlinHandler,
    PythonCommand,
    PythonHandler,
)
from lab09.http_proxy import CachingHTTPProxy, RealHTTPClient
from lab09.vending_machine import (
    Observer,
    SelectProductSTM,
    SelectProductState,
    TakeMoneySTM,
    TakeMoneyState,
    VendingMachineSTM,
)

# ===========================================================================
# Tema 1 — Chain of Responsibility + Command
# ===========================================================================

KOTLIN_CODE = "fun main() {\n    println(\"Hello\")\n}\n"
PYTHON_CODE = "def main():\n    print('Hello')\n\nif __name__ == '__main__':\n    main()\n"
BASH_CODE = "#!/bin/bash\necho 'Hello World'\n"
JAVA_CODE = (
    "public class Main {\n"
    "    public static void main(String[] args) {\n"
    "        System.out.println(\"Hello\");\n"
    "    }\n"
    "}\n"
)
NECUNOSCUT = "xxxxxxxxxxx\nyyyyyyy\nzzzzzzz\n"


class TestChainOfResponsibility:
    def test_kotlin_handler_recunoaste_kotlin(self) -> None:
        assert KotlinHandler().handle(KOTLIN_CODE) == "kotlin"

    def test_python_handler_recunoaste_python(self) -> None:
        assert PythonHandler().handle(PYTHON_CODE) == "python"

    def test_bash_handler_recunoaste_bash(self) -> None:
        assert BashHandler().handle(BASH_CODE) == "bash"

    def test_java_handler_recunoaste_java(self) -> None:
        assert JavaHandler().handle(JAVA_CODE) == "java"

    def test_kotlin_handler_nu_recunoaste_python(self) -> None:
        """KotlinHandler singur nu trebuie să returneze 'kotlin' pentru cod Python."""
        assert KotlinHandler().handle(PYTHON_CODE) != "kotlin"

    def test_lant_kotlin_python_identifica_python(self) -> None:
        kotlin = KotlinHandler()
        python = PythonHandler()
        kotlin.set_next(python)
        assert kotlin.handle(PYTHON_CODE) == "python"

    def test_lant_complet_identifica_java(self) -> None:
        kotlin = KotlinHandler()
        python = PythonHandler()
        bash = BashHandler()
        java = JavaHandler()
        kotlin.set_next(python).set_next(bash).set_next(java)
        assert kotlin.handle(JAVA_CODE) == "java"

    def test_lant_returneaza_none_pentru_necunoscut(self) -> None:
        kotlin = KotlinHandler()
        python = PythonHandler()
        bash = BashHandler()
        java = JavaHandler()
        kotlin.set_next(python).set_next(bash).set_next(java)
        assert kotlin.handle(NECUNOSCUT) is None

    def test_set_next_returneaza_handler_urmator(self) -> None:
        """set_next() trebuie să returneze handler-ul primit (pentru înlănțuire)."""
        kotlin = KotlinHandler()
        python = PythonHandler()
        assert kotlin.set_next(python) is python


class TestCommand:
    def test_python_command_executa_si_returneaza_output(self) -> None:
        cmd = PythonCommand("print('Hello from Python')")
        result = cmd.executa()
        assert "Hello from Python" in result


class TestFileExecutor:
    def test_executor_detecteaza_si_executa_python(self) -> None:
        executor = FileExecutor()
        result = executor.detecteaza_si_executa("print('Hello from executor')")
        assert "Hello from executor" in result

    def test_executor_ridica_eroare_pentru_necunoscut(self) -> None:
        executor = FileExecutor()
        with pytest.raises(ValueError):
            executor.detecteaza_si_executa(NECUNOSCUT)


# ===========================================================================
# Tema 2 — State Machine + Observer
# ===========================================================================


class _CollectObserver(Observer):
    """Observer ajutător care colectează argumentele notificărilor."""

    def __init__(self) -> None:
        self.calls: list = []

    def update(self, *args, **kwargs) -> None:
        self.calls.append(args)


class TestObservable:
    def test_notifica_observer_la_introducere_bani(self) -> None:
        obs = _CollectObserver()
        stm = TakeMoneySTM()
        stm.adauga_observer(obs)
        stm.introdu_bani(2.5)
        assert len(obs.calls) == 1
        assert obs.calls[0][0] == pytest.approx(2.5)

    def test_observer_eliminat_nu_primeste_notificari(self) -> None:
        obs = _CollectObserver()
        stm = TakeMoneySTM()
        stm.adauga_observer(obs)
        stm.elimina_observer(obs)
        stm.introdu_bani(1.0)
        assert len(obs.calls) == 0

    def test_select_notifica_cu_produs_si_pret(self) -> None:
        obs = _CollectObserver()
        stm = SelectProductSTM()
        stm.adauga_observer(obs)
        stm.selecteaza_produs("Cola", 2.5)
        assert len(obs.calls) == 1
        assert obs.calls[0] == ("Cola", 2.5)


class TestTakeMoneySTM:
    def test_stare_initiala(self) -> None:
        stm = TakeMoneySTM()
        assert stm.get_stare() == TakeMoneyState.ASTEPTARE
        assert stm.get_suma() == pytest.approx(0.0)

    def test_introdu_bani_schimba_starea(self) -> None:
        stm = TakeMoneySTM()
        stm.introdu_bani(2.0)
        assert stm.get_stare() == TakeMoneyState.INTRODUCERE

    def test_introdu_bani_acumuleaza(self) -> None:
        stm = TakeMoneySTM()
        stm.introdu_bani(1.0)
        stm.introdu_bani(2.5)
        assert stm.get_suma() == pytest.approx(3.5)

    def test_returneaza_bani_reseteaza(self) -> None:
        stm = TakeMoneySTM()
        stm.introdu_bani(5.0)
        returned = stm.returneaza_bani()
        assert returned == pytest.approx(5.0)
        assert stm.get_suma() == pytest.approx(0.0)
        assert stm.get_stare() == TakeMoneyState.ASTEPTARE

    def test_reseteaza(self) -> None:
        stm = TakeMoneySTM()
        stm.introdu_bani(3.0)
        stm.reseteaza()
        assert stm.get_suma() == pytest.approx(0.0)
        assert stm.get_stare() == TakeMoneyState.ASTEPTARE


class TestSelectProductSTM:
    def test_stare_initiala(self) -> None:
        stm = SelectProductSTM()
        assert stm.get_stare() == SelectProductState.ASTEPTARE
        assert stm.get_produs_selectat() is None

    def test_selecteaza_produs_schimba_starea(self) -> None:
        stm = SelectProductSTM()
        stm.selecteaza_produs("Cola", 2.5)
        assert stm.get_stare() == SelectProductState.SELECTARE

    def test_get_produs_selectat(self) -> None:
        stm = SelectProductSTM()
        stm.selecteaza_produs("Cola", 2.5)
        produs, pret = stm.get_produs_selectat()
        assert produs == "Cola"
        assert pret == pytest.approx(2.5)

    def test_reseteaza(self) -> None:
        stm = SelectProductSTM()
        stm.selecteaza_produs("Apa", 1.5)
        stm.reseteaza()
        assert stm.get_stare() == SelectProductState.ASTEPTARE
        assert stm.get_produs_selectat() is None


class TestVendingMachineSTM:
    def test_valideaza_tranzactie_suma_suficienta(self) -> None:
        vm = VendingMachineSTM()
        vm.take_money_stm.introdu_bani(5.0)
        assert vm.valideaza_tranzactie("Cola", 2.5) is True

    def test_valideaza_tranzactie_suma_insuficienta(self) -> None:
        vm = VendingMachineSTM()
        vm.take_money_stm.introdu_bani(1.0)
        assert vm.valideaza_tranzactie("Cola", 2.5) is False

    def test_calculeaza_rest(self) -> None:
        vm = VendingMachineSTM()
        vm.take_money_stm.introdu_bani(5.0)
        assert vm.calculeaza_rest(2.5) == pytest.approx(2.5)

    def test_finalizeaza_cumparare_returneaza_rest(self) -> None:
        vm = VendingMachineSTM()
        vm.take_money_stm.introdu_bani(5.0)
        vm.select_product_stm.selecteaza_produs("Cola", 2.5)
        rest = vm.finalizeaza_cumparare()
        assert rest == pytest.approx(2.5)

    def test_finalizeaza_cumparare_reseteaza_stm(self) -> None:
        vm = VendingMachineSTM()
        vm.take_money_stm.introdu_bani(5.0)
        vm.select_product_stm.selecteaza_produs("Cola", 2.5)
        vm.finalizeaza_cumparare()
        assert vm.take_money_stm.get_suma() == pytest.approx(0.0)
        assert vm.select_product_stm.get_produs_selectat() is None

    def test_select_product_notifica_vending_machine(self) -> None:
        """VendingMachineSTM este observer la SelectProductSTM."""
        vm = VendingMachineSTM()
        vm.take_money_stm.introdu_bani(5.0)
        # Selectarea produsului trebuie să ajungă la vm.update() fără eroare
        vm.select_product_stm.selecteaza_produs("Apa", 1.5)


# ===========================================================================
# Tema 3 — Proxy cu caching HTTP
# ===========================================================================

CACHE_TEST = "test_cache_lab9.txt"


def _make_proxy(text: str = "Mock response") -> tuple[CachingHTTPProxy, MagicMock]:
    mock_client: MagicMock = MagicMock()
    mock_client.get.return_value = text
    return CachingHTTPProxy(mock_client, CACHE_TEST), mock_client


class TestRealHTTPClient:
    def test_get_apeleaza_requests_si_returneaza_text(self) -> None:
        mock_resp = MagicMock()
        mock_resp.text = "Hello World"

        import unittest.mock as um

        with um.patch("lab09.http_proxy.requests.get", return_value=mock_resp):
            client = RealHTTPClient()
            assert client.get("http://example.com") == "Hello World"


class TestCachingHTTPProxy:
    def setup_method(self) -> None:
        if os.path.exists(CACHE_TEST):
            os.remove(CACHE_TEST)

    def teardown_method(self) -> None:
        if os.path.exists(CACHE_TEST):
            os.remove(CACHE_TEST)

    def test_prima_cerere_apeleaza_clientul_real(self) -> None:
        proxy, mock_client = _make_proxy("First")
        proxy.get("http://example.com")
        mock_client.get.assert_called_once_with("http://example.com")

    def test_a_doua_cerere_foloseste_cache(self) -> None:
        proxy, mock_client = _make_proxy("Cached")
        proxy.get("http://example.com")
        result = proxy.get("http://example.com")
        assert mock_client.get.call_count == 1
        assert result == "Cached"

    def test_url_diferit_face_request_separat(self) -> None:
        proxy, mock_client = _make_proxy()
        proxy.get("http://example.com/1")
        proxy.get("http://example.com/2")
        assert mock_client.get.call_count == 2

    def test_cache_expirat_face_request_nou(self) -> None:
        proxy, mock_client = _make_proxy("Fresh")
        intrare_expirata = {
            "url": "http://example.com",
            "timestamp": 0.0,
            "raspuns": "Old",
        }
        with open(CACHE_TEST, "w") as f:
            f.write(json.dumps(intrare_expirata) + "\n")

        result = proxy.get("http://example.com")
        mock_client.get.assert_called_once()
        assert result == "Fresh"

    def test_fisier_cache_creat_dupa_prima_cerere(self) -> None:
        proxy, _ = _make_proxy()
        proxy.get("http://example.com")
        assert os.path.exists(CACHE_TEST)

    def test_cache_contine_url_timestamp_raspuns(self) -> None:
        proxy, _ = _make_proxy("Test response")
        proxy.get("http://example.com")
        with open(CACHE_TEST) as f:
            intrare = json.loads(f.readline())
        assert intrare["url"] == "http://example.com"
        assert intrare["raspuns"] == "Test response"
        assert "timestamp" in intrare
