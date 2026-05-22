"""
AST (Abstract Syntax Tree) pentru expresii aritmetice.

Suportă operatori: +, -, *, /
Operanzii sunt numere întregi.

Exemplu: expresia "31+42-5" produce arborele (inserare dreapta-recursivă):
        +
       / \
      31  -
         / \
        42   5
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Iterator


# ---------------------------------------------------------------------------
# Noduri AST
# ---------------------------------------------------------------------------

class ASTNode(ABC):
    """Nod abstract din AST."""

    @abstractmethod
    def is_operator(self) -> bool:
        """Returnează True dacă nodul este un operator, False dacă este operand."""
        raise NotImplementedError("De implementat")

    @abstractmethod
    def get_value(self) -> str:
        """Returnează valoarea nodului (operator ca string sau număr ca string)."""
        raise NotImplementedError("De implementat")

    @abstractmethod
    def accept(self, visitor: "ASTVisitor") -> None:
        """Acceptă un vizitator (Visitor pattern)."""
        raise NotImplementedError("De implementat")


class Operand(ASTNode):
    """
    Frunza arborelui: un număr întreg.

    @param value Valoarea numerică
    """

    def __init__(self, value: int) -> None:
        self._value = value

    def is_operator(self) -> bool:
        # TODO: De implementat
        raise NotImplementedError("De implementat")

    def get_value(self) -> str:
        # TODO: De implementat (returnează str(self._value))
        raise NotImplementedError("De implementat")

    def accept(self, visitor: "ASTVisitor") -> None:
        # TODO: De implementat (apelează visitor.visit_operand(self))
        raise NotImplementedError("De implementat")

    @property
    def numeric_value(self) -> int:
        return self._value


class Operator(ASTNode):
    """
    Nod intern: un operator (+, -, *, /).

    @param symbol Simbolul operatorului
    """

    def __init__(self, symbol: str) -> None:
        self._symbol = symbol

    def is_operator(self) -> bool:
        # TODO: De implementat
        raise NotImplementedError("De implementat")

    def get_value(self) -> str:
        # TODO: De implementat (returnează self._symbol)
        raise NotImplementedError("De implementat")

    def accept(self, visitor: "ASTVisitor") -> None:
        # TODO: De implementat (apelează visitor.visit_operator(self))
        raise NotImplementedError("De implementat")


# ---------------------------------------------------------------------------
# Arborele AST
# ---------------------------------------------------------------------------

class AST:
    """
    Nod din arborele AST (poate fi rădăcină sau subarbore).
    Fiecare nod are: data (ASTNode), left (AST), right (AST).
    """

    def __init__(self) -> None:
        self.data: Optional[ASTNode] = None
        self.left: Optional[AST] = None
        self.right: Optional[AST] = None

    def add_node(self, token: ASTNode) -> None:
        """
        Adaugă [token] în arborele AST.

        Algoritm (conform laboratorului):
        - Dacă data este None: setează data = token și gata.
        - Dacă token este Operator:
            - dacă left și right sunt None: mută data curentă la stânga, setează data = token
            - dacă left există dar right nu: aruncă SyntaxError (2 operatori consecutivi)
            - dacă ambii există: adaugă recursiv în right
        - Dacă token este Operand:
            - dacă left și right sunt None: aruncă SyntaxError (2 operanzi consecutivi) — excepție: prima inserare
            - dacă left există dar right nu: inserează în right (nod nou cu token ca data)
            - dacă ambii există: adaugă recursiv în right
        """
        # TODO: De implementat
        raise NotImplementedError("De implementat")

    def accept(self, visitor: "ASTVisitor") -> None:
        """Aplică vizitatorii asupra nodului curent."""
        # TODO: De implementat (apelează visitor.visit(self))
        raise NotImplementedError("De implementat")


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

class ASTBuilder:
    """
    Construiește un AST dintr-un string de expresie.
    Suportă: operanzi întregi, operatori +, -, *, /

    Exemplu:
        ast = AST()
        builder = ASTBuilder("31+42-5", ast)
        # ast conține arborele complet
    """

    def __init__(self, expression: str, ast: AST) -> None:
        self._expression = expression
        self._symbols: list[ASTNode] = []
        self._ast = ast
        self._parse()
        self._build()

    def _parse(self) -> None:
        """
        Parsează [expression] în lista de token-uri (Operand și Operator).
        Gestionează numere multi-cifră (ex: "31+42" → [Operand(31), Operator('+'), Operand(42)]).
        """
        # TODO: De implementat
        raise NotImplementedError("De implementat")

    def _build(self) -> None:
        """Inserează fiecare token în AST."""
        for token in self._symbols:
            self._ast.add_node(token)


# ---------------------------------------------------------------------------
# Vizitatori
# ---------------------------------------------------------------------------

class ASTVisitor(ABC):
    """Interfața Visitor pentru parcurgerea AST."""

    @abstractmethod
    def visit(self, node: AST) -> None:
        """Vizitează nodul [node]."""
        raise NotImplementedError("De implementat")


class PreOrderVisitor(ASTVisitor):
    """
    Parcurgere pre-ordine: rădăcină → stânga → dreapta.
    Colectează valorile în lista [result].
    """

    def __init__(self) -> None:
        self.result: list[str] = []

    def visit(self, node: AST) -> None:
        # TODO: De implementat
        raise NotImplementedError("De implementat")


class InOrderVisitor(ASTVisitor):
    """
    Parcurgere in-ordine: stânga → rădăcină → dreapta.
    Colectează valorile în lista [result].
    """

    def __init__(self) -> None:
        self.result: list[str] = []

    def visit(self, node: AST) -> None:
        # TODO: De implementat
        raise NotImplementedError("De implementat")


class PostOrderVisitor(ASTVisitor):
    """
    Parcurgere post-ordine: stânga → dreapta → rădăcină.
    Colectează valorile în lista [result].
    """

    def __init__(self) -> None:
        self.result: list[str] = []

    def visit(self, node: AST) -> None:
        # TODO: De implementat
        raise NotImplementedError("De implementat")


class CalculatorVisitor(ASTVisitor):
    """
    Evaluează expresia din AST și stochează rezultatul în [result].

    Algoritm post-ordine:
    - Dacă nodul e Operand: push valoarea pe stivă
    - Dacă nodul e Operator: pop 2 valori, aplică operatorul, push rezultatul

    Accesează rezultatul prin [result] (int).
    """

    def __init__(self) -> None:
        self._stack: list[int] = []
        self.result: Optional[int] = None

    def visit(self, node: AST) -> None:
        # TODO: De implementat
        raise NotImplementedError("De implementat")
