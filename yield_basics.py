"""yield in una funzione normale: la funzione si ferma a metà e riprende."""


def count_to_two():
    print("parto")
    yield 1
    print("riprendo")
    yield 2
    print("ho finito")


steps = count_to_two()  # niente viene eseguito: la chiamata crea solo un oggetto
print("creato:", type(steps).__name__)

print("primo next():", next(steps))
print("secondo next():", next(steps))

try:
    next(steps)
except StopIteration:
    print("terzo next(): StopIteration, la funzione è finita")
