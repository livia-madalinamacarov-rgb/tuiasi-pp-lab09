# Lab 9 — Design Patterns în Python

Template GitHub Classroom pentru laboratorul 9 — Paradigme de Programare (TUIASI).

## Conținut

Două teme independente de design patterns:

| Temă | Pattern | Fișier |
|------|---------|--------|
| 1 | Singleton Logger | `lab09/singleton_log.py` |
| 2 | AST + Visitor | `lab09/ast_expr.py` |

Fișierele sursă conțin **schelete** (`raise NotImplementedError("De implementat")`).
Testele din `tests/test_lab9.py` sunt complete și definesc comportamentul așteptat.

## Rulare teste

```bash
uv run pytest
uv run pytest -v
```

## CI

La fiecare `git push`, GitHub Actions rulează automat `uv run pytest`.
