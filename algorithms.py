import random

class LoadBalancer:
    def get_slot(self, i: int, id: int, slots: int) -> int:
        ...


class Randomized(LoadBalancer):
    def get_slot(self, i: int, id: int, slots: int) -> int:
        return int(random.random() * slots)


class RoundRobin(LoadBalancer):
    def get_slot(self, i: int, id: int, slots: int) -> int:
        return i % slots


class Hashed(LoadBalancer):
    def get_slot(self, i: int, id: int, slots: int) -> int:
        return id % slots


class NextSlot(LoadBalancer):
    def __init__(self):
        self.total_requests = 0
        self.used_slots = {}

    def record(self, rv):
        self.total_requests += 1
        self.used_slots.setdefault(rv, 0)
        self.used_slots[rv] += 1

    def get_slot(self, i: int, id: int, slots: int) -> int:
        rv = orig_rv = id % slots
        while (
            self.used_slots
            and self.total_requests
            and self.used_slots.get(rv, 0) > (self.total_requests / len(self.used_slots))
        ):
            rv += 1
            rv = rv % slots
            if rv == orig_rv:
                break

        self.record(rv)
        return rv


class MultiSlot(NextSlot):
    def get_slot(self, i: int, id: int, slots: int) -> int:
        SCALE = 1
        SPREAD = 5
        slots *= SCALE

        possible_slots = [(id * (2 ** d) + d) % slots for d in range(SPREAD)]
        if self.used_slots:
            rv = min(possible_slots, key=lambda x: self.used_slots.get(x, 0))
        else:
            rv = possible_slots[0]

        self.record(rv)
        return rv // SCALE


class SpreadTopN(NextSlot):
    def get_slot(self, i: int, id: int, slots: int) -> int:
        rv = id % slots

        if self.used_slots.get(rv, 0) > 1.2 * self.total_requests // (len(self.used_slots) or 1):
            rv = int(random.random() * slots)

        self.record(rv)
        return rv
