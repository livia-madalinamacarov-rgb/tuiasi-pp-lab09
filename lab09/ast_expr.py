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
        return False

    def get_value(self) -> str:
        return str(self._value)

    def accept(self, visitor: "ASTVisitor") -> None:
        # Nu apelăm direct visitor.visit_operand aici, interfața cere visit(AST)
        # Dar nodul în sine acceptă vizitatorul prin delegare din structura AST-ului.
        pass

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
        return True

    def get_value(self) -> str:
        return self._symbol

    def accept(self, visitor: "ASTVisitor") -> None:
        pass


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
        """
        # Dacă data este None: setează data = token și gata.
        if self.data is None:
            self.data = token
            return

        # Dacă token este Operator:
        if token.is_operator():
            # dacă left și right sunt None: mută data curentă la stânga, setează data = token
            if self.left is None and self.right is None:
                left_child = AST()
                left_child.data = self.data
                left_child.left = self.left
                left_child.right = self.right

                self.left = left_child
                self.data = token
            # dacă left există dar right nu: aruncă SyntaxError (2 operatori consecutivi)
            elif self.left is not None and self.right is None:
                raise SyntaxError("Doi operatori consecutivi sau sintaxă invalidă.")
            # dacă ambii există: adaugă recursiv în right
            else:
                self.right.add_node(token)

        # Dacă token este Operand:
        else:
            # dacă left și right sunt None: aruncă SyntaxError (2 operanzi consecutivi)
            if self.left is None and self.right is None:
                raise SyntaxError("Doi operanzi consecutivi sau sintaxă invalidă.")
            # dacă left există dar right nu: inserează în right (nod nou cu token ca data)
            elif self.left is not None and self.right is None:
                right_child = AST()
                right_child.data = token
                self.right = right_child
            # dacă ambii există: adaugă recursiv în right
            else:
                self.right.add_node(token)

    def accept(self, visitor: "ASTVisitor") -> None:
        """Aplică vizitatorii asupra nodului curent."""
        visitor.visit(self)


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

class ASTBuilder:
    """
    Construiește un AST dintr-un string de expresie.
    Suportă: operanzi întregi, operatori +, -, *, /
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
        Gestionează numere multi-cifră.
        """
        operators = {'+', '-', '*', '/'}
        i = 0
        n = len(self._expression)

        while i < n:
            char = self._expression[i]

            # Ignorăm spațiile libere
            if char.isspace():
                i += 1
                continue

            if char in operators:
                self._symbols.append(Operator(char))
                i += 1
            elif char.isdigit():
                # Extragem numărul complet format din mai multe cifre consecutive
                start = i
                while i < n and self._expression[i].isdigit():
                    i += 1
                num_val = int(self._expression[start:i])
                self._symbols.append(Operand(num_val))
            else:
                raise SyntaxError(f"Caracter neașteptat: {char}")

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
        if node is None or node.data is None:
            return

        self.result.append(node.data.get_value())
        if node.left:
            node.left.accept(self)
        if node.right:
            node.right.accept(self)


class InOrderVisitor(ASTVisitor):
    """
    Parcurgere in-ordine: stânga → rădăcină → dreapta.
    Colectează valorile în lista [result].
    """

    def __init__(self) -> None:
        self.result: list[str] = []

    def visit(self, node: AST) -> None:
        if node is None or node.data is None:
            return

        if node.left:
            node.left.accept(self)
        self.result.append(node.data.get_value())
        if node.right:
            node.right.accept(self)


class PostOrderVisitor(ASTVisitor):
    """
    Parcurgere post-ordine: stânga → dreapta → rădăcină.
    Colectează valorile în lista [result].
    """

    def __init__(self) -> None:
        self.result: list[str] = []

    def visit(self, node: AST) -> None:
        if node is None or node.data is None:
            return

        if node.left:
            node.left.accept(self)
        if node.right:
            node.right.accept(self)
        self.result.append(node.data.get_value())


class CalculatorVisitor(ASTVisitor):
    """
    Evaluează expresia din AST și stochează rezultatul în [result].
    """

    def __init__(self) -> None:
        self._stack: list[int] = []
        self.result: Optional[int] = None

    def visit(self, node: AST) -> None:
        if node is None or node.data is None:
            return

        # Algoritm post-ordine recursiv: stânga -> dreapta -> rădăcină
        if node.left:
            node.left.accept(self)
        if node.right:
            node.right.accept(self)

        # Procesăm nodul curent (rădăcina subarborelui)
        if not node.data.is_operator():
            # Dacă nodul e Operand: push valoarea pe stivă
            # Cast explicit la Operand pentru siguranța type-checking-ului static
            operand_node = node.data
            self._stack.append(operand_node.numeric_value)
        else:
            # Dacă nodul e Operator: pop 2 valori, aplică operatorul, push rezultatul
            if len(self._stack) < 2:
                raise SyntaxError("Expresie malformată: operanzi suficienți lipsă pentru operator.")

            # Din cauza structurii dreapta-recursive a acestui laborator:
            # Primul pop scoate subarborele drept (right) sau operandul drept,
            # Al doilea pop scoate elementul stâng (left).
            right_val = self._stack.pop()
            left_val = self._stack.pop()

            symbol = node.data.get_value()
            if symbol == '+':
                res = left_val + right_val
            elif symbol == '-':
                res = left_val - right_val
            elif symbol == '*':
                res = left_val * right_val
            elif symbol == '/':
                if right_val == 0:
                    raise ZeroDivisionError("Împărțire la zero în interiorul AST-ului.")
                res = int(left_val / right_val)  # Împărțire întreagă conform cerinței
            else:
                raise ValueError(f"Operator necunoscut: {symbol}")

            self._stack.append(res)

        # Rezultatul final va rămâne singurul element din stivă la terminarea parcurgerii complete
        if self._stack:
            self.result = self._stack[-1]