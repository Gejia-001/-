import heapq


class EventQueue:
    def __init__(self):
        self.events = []
        self.counter = 0

    def add(self, event):
        heapq.heappush(self.events, (event.time, self.counter, event))
        self.counter += 1

    def pop(self):
        item = heapq.heappop(self.events)
        return item[2]

    def is_empty(self):
        return len(self.events) == 0
    def peek_time(self):
        return self.events[0][0]