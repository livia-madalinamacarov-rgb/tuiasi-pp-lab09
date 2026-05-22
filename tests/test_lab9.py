"""
Teste pentru Lab 9: Singleton Logger + AST cu Vizitatori.
"""
import os
import pytest

from lab09.singleton_log import Log
from lab09.ast_expr import (
    Operand, Operator, AST, ASTBuilder,
    PreOrderVisitor, InOrderVisitor, PostOrderVisitor, CalculatorVisitor,
)


# ---------------------------------------------------------------------------
# Singleton Log
# ---------------------------------------------------------------------------

class TestSingletonLog:

    def setup_method(self):
        Log.reset()

    def teardown_method(self):
        Log.reset()

    def test_create_first_instance(self, tmp_path):
        log = Log(str(tmp_path / "test.log"))
        assert Log._instance is log

    def test_create_second_instance_raises(self, tmp_path):
        Log(str(tmp_path / "a.log"))
        with pytest.raises(Exception, match="singleton"):
            Log(str(tmp_path / "b.log"))

    def test_get_instance_returns_same_object(self, tmp_path):
        log = Log(str(tmp_path / "test.log"))
        assert Log.get_instance() is log

    def test_get_instance_without_create_raises(self):
        with pytest.raises(Exception):
            Log.get_instance()

    def test_write_appends_lines(self, tmp_path):
        fname = str(tmp_path / "test.log")
        log = Log(fname)
        log.write("prima linie")
        log.write("a doua linie")
        with open(fname) as f:
            lines = [l.strip() for l in f.readlines()]
        assert "prima linie" in lines
        assert "a doua linie" in lines

    def test_existing_file_deleted_on_create(self, tmp_path):
        fname = str(tmp_path / "test.log")
        with open(fname, "w") as f:
            f.write("continut vechi\n")
        log = Log(fname)
        log.write("continut nou")
        with open(fname) as f:
            content = f.read()
        assert "continut vechi" not in content
        assert "continut nou" in content

    def test_reset_allows_new_instance(self, tmp_path):
        Log(str(tmp_path / "a.log"))
        Log.reset()
        assert Log._instance is None
        log2 = Log(str(tmp_path / "b.log"))  # nu trebuie să arunce
        assert Log._instance is log2


# ---------------------------------------------------------------------------
# Noduri ASTNode
# ---------------------------------------------------------------------------

class TestASTNodes:

    def test_operand_is_not_operator(self):
        assert Operand(5).is_operator() is False

    def test_operand_get_value_returns_string(self):
        assert Operand(42).get_value() == "42"

    def test_operand_get_value_zero(self):
        assert Operand(0).get_value() == "0"

    def test_operator_is_operator(self):
        assert Operator("+").is_operator() is True

    def test_operator_get_value(self):
        assert Operator("-").get_value() == "-"
        assert Operator("*").get_value() == "*"


# ---------------------------------------------------------------------------
# ASTBuilder + vizitatori
# ---------------------------------------------------------------------------

def _build(expr: str) -> AST:
    ast = AST()
    ASTBuilder(expr, ast)
    return ast


class TestPreOrderVisitor:

    def test_single_operand(self):
        ast = _build("7")
        v = PreOrderVisitor()
        ast.accept(v)
        assert v.result == ["7"]

    def test_simple_addition(self):
        ast = _build("3+4")
        v = PreOrderVisitor()
        ast.accept(v)
        assert v.result == ["+", "3", "4"]

    def test_chain_expression(self):
        # 31+42-5 → arbore: + la rădăcină, 31 stânga, - dreapta (42, 5)
        ast = _build("31+42-5")
        v = PreOrderVisitor()
        ast.accept(v)
        assert v.result == ["+", "31", "-", "42", "5"]


class TestInOrderVisitor:

    def test_simple_addition(self):
        ast = _build("3+4")
        v = InOrderVisitor()
        ast.accept(v)
        assert v.result == ["3", "+", "4"]

    def test_chain_expression(self):
        ast = _build("31+42-5")
        v = InOrderVisitor()
        ast.accept(v)
        assert v.result == ["31", "+", "42", "-", "5"]

    def test_multidigit_numbers(self):
        ast = _build("100+200")
        v = InOrderVisitor()
        ast.accept(v)
        assert v.result == ["100", "+", "200"]


class TestPostOrderVisitor:

    def test_simple_addition(self):
        ast = _build("3+4")
        v = PostOrderVisitor()
        ast.accept(v)
        assert v.result == ["3", "4", "+"]

    def test_chain_expression(self):
        ast = _build("31+42-5")
        v = PostOrderVisitor()
        ast.accept(v)
        assert v.result == ["31", "42", "5", "-", "+"]

    def test_subtraction(self):
        ast = _build("10-3")
        v = PostOrderVisitor()
        ast.accept(v)
        assert v.result == ["10", "3", "-"]


class TestCalculatorVisitor:

    def test_addition(self):
        ast = _build("3+4")
        v = CalculatorVisitor()
        ast.accept(v)
        assert v.result == 7

    def test_subtraction(self):
        ast = _build("10-3")
        v = CalculatorVisitor()
        ast.accept(v)
        assert v.result == 7

    def test_chain_expression(self):
        # 31+(42-5) = 68  (arbore dreapta-recursiv)
        ast = _build("31+42-5")
        v = CalculatorVisitor()
        ast.accept(v)
        assert v.result == 68

    def test_multidigit_addition(self):
        ast = _build("100+200")
        v = CalculatorVisitor()
        ast.accept(v)
        assert v.result == 300

    def test_single_operand(self):
        ast = _build("42")
        v = CalculatorVisitor()
        ast.accept(v)
        assert v.result == 42
