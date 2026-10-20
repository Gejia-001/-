class Event:
    def __init__(self, time, event_type, process):
        self.time = time
        self.event_type = event_type
        self.process = process

class ArrivalEvent(Event):
    def __init__(self, process):
        super().__init__(process.arrival_time, "arrival", process)

class FinishEvent(Event):
    def __init__(self, time, process):
        super().__init__(time, "finish", process)
class TimerEvent(Event):
    def __init__(self, time, process):
        super().__init__(time, "timer", process)
