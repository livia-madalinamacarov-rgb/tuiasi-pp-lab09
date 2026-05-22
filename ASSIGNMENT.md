# Lab 9 — Design Patterns în Python

## Descriere

Două teme independente:

| Temă | Pattern | Fișier |
|------|---------|--------|
| 1 | Singleton | `singleton_log.py` |
| 2 | AST + Visitor | `ast_expr.py` |

---

## Structura proiectului

```
lab09/
  lab09/
    __init__.py
    singleton_log.py   ← Tema 1: Logger Singleton (stub)
    ast_expr.py        ← Tema 2: AST cu vizitatori (stub)
  tests/
    __init__.py
    test_lab9.py       ← teste complete (nu se modifică)
  .github/workflows/classroom.yml
  pyproject.toml
  ASSIGNMENT.md
  README.md
```

---

## Tema 1 — Singleton Logger

Se implementează un serializator simplu (logger) bazat pe pattern-ul Singleton: poate exista
o singură instanță de `Log` per aplicație.

### Clasa `Log`

**Câmpuri de clasă:**
- `_instance: Optional[Log]` — instanța unică (inițializată cu `None`)

**Metode de implementat:**

| Metodă | Semnătură | Comportament |
|--------|-----------|-------------|
| `__init__` | `(self, fname: str)` | Dacă `_instance` există deja → aruncă `Exception("Clasa este un singleton")`. Altfel: salvează calea fișierului, dacă fișierul există îl șterge (log nou la fiecare rulare), setează `Log._instance = self` |
| `write` | `(self, line: str)` | Deschide fișierul în modul `append`, scrie `line + "\n"`, închide |
| `get_instance` | `@staticmethod` → `Log` | Returnează `_instance`. Dacă nu există → aruncă `Exception("Nu există instanță Log")` |
| `reset` | `@staticmethod` | Setează `Log._instance = None` (util pentru teste) |

**Exemplu:**
```python
log = Log("output.log")   # prima și singura creare permisă
log.write("prima linie")
log2 = Log.get_instance() # aceeași instanță ca log
log2.write("a doua linie")

Log(...)  # → Exception("Clasa este un singleton")
```

---

## Tema 2 — AST cu Vizitatori

Se implementează un arbore sintactic abstract (AST) pentru expresii aritmetice cu operatorii
`+`, `-`, `*`, `/` și operanzi întregi (inclusiv multi-cifră). Vizitatorii parcurg arborele în
diferite ordini sau evaluează expresia.

### Arborele pentru `"31+42-5"`

Algoritmul de inserare este dreapta-recursiv: operatorul nou se plasează în subarborele drept.

```
     +
    / \
  31   -
      / \
    42    5
```

Traversări:
- **Pre-ordine**: `+`, `31`, `-`, `42`, `5`
- **În-ordine**: `31`, `+`, `42`, `-`, `5`
- **Post-ordine**: `31`, `42`, `5`, `-`, `+`
- **Valoare**: `31 + (42 - 5) = 68`

### `ASTNode` (abstract — gata)

Metodele `is_operator() -> bool`, `get_value() -> str`, `accept(visitor)` sunt abstracte.

### `Operand(value: int)` (stub)

| Metodă | Returnează |
|--------|-----------|
| `is_operator()` | `False` |
| `get_value()` | `str(self._value)` |
| `accept(visitor)` | `visitor.visit_operand(self)` |

### `Operator(symbol: str)` (stub)

| Metodă | Returnează |
|--------|-----------|
| `is_operator()` | `True` |
| `get_value()` | `self._symbol` |
| `accept(visitor)` | `visitor.visit_operator(self)` |

### `AST` (stub)

**Câmpuri:** `data: Optional[ASTNode]`, `left: Optional[AST]`, `right: Optional[AST]`

**`add_node(token: ASTNode)`** — inserează token-ul urmând algoritmul:

```
dacă data este None:
    data = token
dacă token este Operator:
    dacă left = right = None:    mută data la stânga, data = token
    dacă left ≠ None, right = None: SyntaxError (2 operatori consecutivi)
    dacă left ≠ None, right ≠ None: inserează recursiv în right
dacă token este Operand:
    dacă left = right = None:    SyntaxError (2 operanzi consecutivi)
    dacă left ≠ None, right = None: right = AST nou cu token
    dacă left ≠ None, right ≠ None: inserează recursiv în right
```

**`accept(visitor)`** → apelează `visitor.visit(self)`

### `ASTBuilder(expression: str, ast: AST)` (stub)

**`_parse()`** — parcurge `expression` caracter cu caracter, construiește lista `_symbols`:
- cifre consecutive formează un `Operand` (suport multi-cifră)
- `+`, `-`, `*`, `/` formează câte un `Operator`

### Vizitatori (stub)

Fiecare vizitator implementează `visit(node: AST)` și colectează rezultatele în `self.result`.

| Clasă | Parcurgere | Algoritm |
|-------|-----------|----------|
| `PreOrderVisitor` | rădăcină → stânga → dreapta | adaugă `node.data.get_value()`, recurse stânga, recurse dreapta |
| `InOrderVisitor` | stânga → rădăcină → dreapta | recurse stânga, adaugă `node.data.get_value()`, recurse dreapta |
| `PostOrderVisitor` | stânga → dreapta → rădăcină | recurse stânga, recurse dreapta, adaugă `node.data.get_value()` |
| `CalculatorVisitor` | post-ordine + stivă | dacă Operand: push valoare; dacă Operator: pop dreapta, pop stânga, push rezultat; rezultatul final → `self.result` |

**Exemplu complet:**
```python
ast = AST()
ASTBuilder("31+42-5", ast)

pre = PreOrderVisitor()
ast.accept(pre)
# pre.result == ["+", "31", "-", "42", "5"]

calc = CalculatorVisitor()
ast.accept(calc)
# calc.result == 68
```

---

## Cum se rulează testele

```bash
uv run pytest
```

---

## Tabel de evaluare

| Cerință | Punctaj |
|---------|---------|
| `Log.__init__` (Singleton + ștergere fișier existent) | 1p |
| `Log.write` + `Log.get_instance` + `Log.reset` | 1p |
| `Operand` + `Operator` (is_operator, get_value) | 1p |
| `AST.add_node` (toate cazurile) | 2p |
| `ASTBuilder._parse` (multi-cifră, toți operatorii) | 1p |
| `PreOrderVisitor` | 1p |
| `InOrderVisitor` | 1p |
| `PostOrderVisitor` | 1p |
| `CalculatorVisitor` | 1p |
| **Total** | **10p** |
