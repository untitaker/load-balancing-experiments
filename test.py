import math
import random
import pytest
import algorithms

import matplotlib.pyplot as plt


def box_muller_transform(a, b):
    return (
        math.sqrt(-2 * math.log2(a)) * math.cos(math.tau * b),
        math.sqrt(-2 * math.log2(a)) * math.sin(math.tau * b)
    )

TESTS = list(enumerate((
    algorithms.NextSlot,
    algorithms.Randomized,
    algorithms.RoundRobin,
    algorithms.Hashed,
    algorithms.MultiSlot,
    algorithms.SpreadTopN,
)))

@pytest.fixture(scope='session', autouse=True)
def show_plot():
    yield
    plt.tight_layout()
    plt.show()

IDS = 100
SLOTS = 60

@pytest.fixture(scope='session')
def ids_seq():
    rv = []
    for _ in range(100000):
        for id_factor in box_muller_transform(random.random(), random.random()):
            id = abs(int(id_factor * id_factor * IDS))
            rv.append(id)

    return rv


@pytest.mark.parametrize("fn_i,fn", TESTS)
def test(fn_i, fn, ids_seq):
    uniq_ids_total = set()
    uniq_ids_per_slot = {}
    slot_seq = []

    lb = fn()

    for i, id in enumerate(ids_seq):
        uniq_ids_total.add(id)
        slot = lb.get_slot(i, id, SLOTS)
        slot_seq.append(slot)
        uniq_ids_per_slot.setdefault(slot, set()).add(id)

    grid = (3, len(TESTS))

    plt.subplot2grid(grid, (0, fn_i), rowspan=1, colspan=1)
    plt.title(f"total ids = {len(uniq_ids_total)}")
    plt.hist(ids_seq)

    plt.subplot2grid(grid, (1, fn_i), rowspan=1, colspan=1)
    plt.title(f"requests per slot, {fn.__name__}")
    plt.hist(slot_seq, bins=SLOTS)

    plt.subplot2grid(grid, (2, fn_i), rowspan=1, colspan=1)
    plt.title(f"ids per slot")
    uniq_ids_per_slot = list(uniq_ids_per_slot.items())
    plt.bar(
        x=[k for k, _ in uniq_ids_per_slot],
        height=[len(v) for _, v in uniq_ids_per_slot]
    )
