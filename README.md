# Lab 9 — Design Patterns în Python

Template GitHub Classroom pentru laboratorul 9 — Paradigme de Programare (TUIASI).

## Conținut

Trei teme independente de design patterns:

| Tema | Pattern-uri | Fișier |
|------|-------------|--------|
| 1 | Chain of Responsibility + Command | `lab09/chain_command.py` |
| 2 | State Machine + Observer | `lab09/vending_machine.py` |
| 3 | Proxy cu caching HTTP | `lab09/http_proxy.py` |

Fișierele sursă conțin **schelete** (`raise NotImplementedError("De implementat")`).
Testele din `tests/test_lab9.py` sunt complete și definesc comportamentul așteptat.

## Rulare teste

```bash
uv run pytest
uv run pytest -v
```

## CI

La fiecare `git push`, GitHub Actions rulează automat `uv run pytest`.
