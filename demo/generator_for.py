"""Dimostrativo: un generator letto con for. Ogni valore esce appena è pronto, prima del successivo."""
from collections.abc import Iterator


def report_lines() -> Iterator[str]:
    for number in range(1, 4):
        print(f"  produco la riga {number}")
        yield f"riga {number}\n"


for line in report_lines():
    print(f"ricevo {line!r}")
