# Lab 9 — Design Patterns în Python

## Descriere

Implementează trei aplicații independente, fiecare folosind câte unul-două design patterns clasice:

| Tema | Pattern-uri | Fișier |
|------|-------------|--------|
| 1 | Chain of Responsibility + Command | `chain_command.py` |
| 2 | State Machine + Observer | `vending_machine.py` |
| 3 | Proxy (+ Bonus: Strategy) | `http_proxy.py` |

---

## Structura proiectului

```
lab09/
  lab09/
    __init__.py
    chain_command.py    ← Tema 1: CoR + Command (stub)
    vending_machine.py  ← Tema 2: STM + Observer (stub)
    http_proxy.py       ← Tema 3: Proxy (stub)
  tests/
    __init__.py
    test_lab9.py        ← teste complete (nu se modifică)
  .github/workflows/classroom.yml
  pyproject.toml
  ASSIGNMENT.md
  README.md
```

---

## Tema 1 — Identificare tip fișier + execuție (CoR + Command)

Aplicația primește conținutul unui fișier **fără extensie** și trebuie să:
1. Determine tipul fișierului (Kotlin / Python / Bash / Java) **exclusiv din conținut**
2. Execute conținutul cu comanda corespunzătoare și returneze output-ul

### `FileTypeHandler` (baza CoR)

Clasă abstractă cu:
- `set_next(handler)` — înlănțuiește handlerul următor; returnează `handler` (permite `h1.set_next(h2).set_next(h3)`)
- `handle(continut: str) -> Optional[str]` — încearcă să identifice tipul; dacă nu reușește, pasează la `_next`

### Handlere concrete

| Clasă | Detectează | Sugestii de detecție |
|-------|-----------|----------------------|
| `KotlinHandler` | Kotlin | `fun`, `val`, `var`, `when`, `println` |
| `PythonHandler` | Python | `def`, `import`, `print(`, shebang `python` |
| `BashHandler` | Bash | shebang `#!/bin/bash`, `echo`, `$` |
| `JavaHandler` | Java | `public class`, `System.out`, `import java.` |

Fiecare handler returnează `'kotlin'` / `'python'` / `'bash'` / `'java'` sau pasează mai departe.

### `FileCommand` (baza Command)

Clasă abstractă cu:
- `__init__(continut: str)` — memorează conținutul
- `executa() -> str` — salvează conținutul într-un fișier temporar (`tempfile`), îl execută cu `subprocess.run()`, returnează stdout-ul

### Comenzi concrete

| Clasă | Comandă de execuție |
|-------|---------------------|
| `PythonCommand` | `python3 <fișier_temp>` |
| `BashCommand` | `bash <fișier_temp>` |
| `KotlinCommand` | `kotlinc-jvm` + `kotlin` |
| `JavaCommand` | `javac <fișier_temp>` + `java <clasă>` |

### `FileExecutor`

Combină CoR cu Command:
- `__init__()` — construiește lanțul: Kotlin → Python → Bash → Java
- `detecteaza_si_executa(continut: str) -> str` — detectează tipul, instanțiază comanda corespunzătoare, execută și returnează output-ul; ridică `ValueError` dacă tipul nu e recunoscut

### Exemplu de utilizare

```python
executor = FileExecutor()
cod = "print('Hello from Python')"
print(executor.detecteaza_si_executa(cod))  # → "Hello from Python\n"
```

---

## Tema 2 — Automat de sucuri (STM + Observer)

Simulează un automat de sucuri prin trei componente interconectate.

### Pattern Observer

**`Observer`** (ABC):
- `update(*args, **kwargs)` — metodă abstractă

**`Observable`** (ABC):
- `adauga_observer(observer)` — adaugă la lista internă
- `elimina_observer(observer)` — elimină din lista internă
- `notifica_observeri(*args, **kwargs)` — apelează `update()` pe fiecare observer

### `TakeMoneySTM(Observable)`

Stări: `ASTEPTARE` → `INTRODUCERE`

| Metodă | Comportament |
|--------|-------------|
| `introdu_bani(suma)` | Adaugă la total, trece în `INTRODUCERE`, notifică observerii cu suma curentă |
| `returneaza_bani()` | Returnează suma, resetează la 0, trece în `ASTEPTARE` |
| `get_suma()` | Returnează suma curentă |
| `get_stare()` | Returnează starea curentă |
| `reseteaza()` | Suma ← 0, stare ← `ASTEPTARE` |

Observerul implicit (opțional) afișează la consolă suma introdusă.

### `SelectProductSTM(Observable)`

Stări: `ASTEPTARE` → `SELECTARE`

| Metodă | Comportament |
|--------|-------------|
| `selecteaza_produs(produs, pret)` | Salvează produsul, trece în `SELECTARE`, notifică cu `(produs, pret)` |
| `get_produs_selectat()` | Returnează `(produs, pret)` sau `None` |
| `get_stare()` | Returnează starea curentă |
| `reseteaza()` | Produs ← None, stare ← `ASTEPTARE` |

### `VendingMachineSTM(Observer)`

Entitatea centrală. Se înregistrează ca observer la `SelectProductSTM`.

| Atribut/Metodă | Detalii |
|----------------|---------|
| `take_money_stm` | instanță `TakeMoneySTM` |
| `select_product_stm` | instanță `SelectProductSTM` |
| `update(produs, pret)` | apelat de STM la selecție; verifică validitatea tranzacției |
| `valideaza_tranzactie(produs, pret)` | `True` dacă suma introdusă ≥ preț |
| `calculeaza_rest(pret)` | suma curentă − preț |
| `finalizeaza_cumparare()` | calculează restul, resetează ambele STM-uri, returnează restul |

Produse disponibile: `Cola (2.5 lei)`, `Fanta (2.5 lei)`, `Apa (1.5 lei)`, `Suc de mere (3.0 lei)`.

### Exemplu de utilizare

```python
vm = VendingMachineSTM()
vm.take_money_stm.introdu_bani(5.0)
vm.select_product_stm.selecteaza_produs("Cola", 2.5)
rest = vm.finalizeaza_cumparare()
print(f"Rest: {rest} lei")  # → Rest: 2.5 lei
```

---

## Tema 3 — Proxy cu caching HTTP

Realizează cereri HTTP GET cu un mecanism de caching în fișier text.

### `HTTPClient` (ABC)

- `get(url: str) -> str`

### `RealHTTPClient(HTTPClient)`

- `get(url)` — apelează `requests.get(url)` și returnează `.text`

### `CachingHTTPProxy(HTTPClient)`

Proxy care verifică/actualizează un cache stocat într-un fișier text (câte o linie JSON per intrare).

Format intrare cache:
```json
{"url": "https://...", "timestamp": 1713000000.0, "raspuns": "..."}
```

**`__init__(client, fisier_cache="cache.txt")`**

**`get(url) -> str`** — logică:
1. Citește cache-ul
2. Dacă există intrare pentru `url` și **nu a expirat** (< 1 oră) → returnează răspunsul din cache
3. Dacă a **expirat** → apelează clientul real, actualizează intrarea, rescrie cache-ul
4. Dacă **nu există** → apelează clientul real, adaugă intrarea, rescrie cache-ul

**`_citeste_cache() -> list[dict]`** — parsează fișierul; dacă nu există, returnează `[]`

**`_scrie_cache(intrari)`** — scrie lista ca linii JSON în fișier

**`_este_valida(intrare) -> bool`** — `True` dacă `time.time() - intrare["timestamp"] < 3600`

### Exemplu de utilizare

```python
client = RealHTTPClient()
proxy = CachingHTTPProxy(client, "cache.txt")

r1 = proxy.get("https://httpbin.org/get")  # cerere reală
r2 = proxy.get("https://httpbin.org/get")  # din cache
```

### [BONUS] Strategy + Load Balancing

Folosind pattern-ul **Strategy** combinat cu proxy-ul, monitorizează numărul de cereri într-o cuantă de timp. Dacă numărul de cereri a crescut de 10 ori față de cuanta anterioară, creează un nou proces (`multiprocessing`) care să gestioneze jumătate din cereri.

---

## Cum se rulează testele

```bash
uv run pytest
uv run pytest -v          # verbose
uv run pytest -k Tema1    # filtrare după clasă/funcție
```

---

## Tabel de evaluare

| Cerință | Punctaj |
|---------|---------|
| `FileTypeHandler.set_next()` + logică pasare | 5p |
| Handlere CoR — detectare corectă (toate 4 tipuri) | 15p |
| `FileCommand` + `PythonCommand.executa()` | 10p |
| `FileExecutor` — detectare + execuție + ValueError | 10p |
| `Observable` — adaugă/elimină/notifică | 5p |
| `TakeMoneySTM` — stări + notificări | 10p |
| `SelectProductSTM` — stări + notificări | 10p |
| `VendingMachineSTM` — validare + rest + finalizare | 15p |
| `RealHTTPClient.get()` | 5p |
| `CachingHTTPProxy` — cache miss/hit/expirat | 15p |
| **[BONUS]** Strategy + Load Balancing | +10p |
| **Total** | **100p** |
