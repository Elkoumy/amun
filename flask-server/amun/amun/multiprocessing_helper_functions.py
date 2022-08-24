
import itertools
def chunked_iterable(iterable, size):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk

def init(val):
    global TASKS_AT_ONCE
    TASKS_AT_ONCE=val