from time import perf_counter
from contextlib import contextmanager

@contextmanager
def catchtime() -> float:
    t1 = t2 = perf_counter() 
    yield lambda: t2 - t1
    t2 = perf_counter()