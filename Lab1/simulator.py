from event_queue import EventQueue
from event import ArrivalEvent, FinishEvent, TimerEvent
from process import Process

class Simulator:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.current_time = 0
        self.event_queue = EventQueue()
        self.ready_queue = []
        self.running_process = None
    def load_processes(self, processes):
        self.processes = [
            Process(p.name, p.arrival_time, p.burst_time, p.priority)
            for p in processes
        ]

        for process in self.processes:
            self.event_queue.add(ArrivalEvent(process))
    
    def handle_arrival(self, event):
        self.ready_queue.append(event.process)

    def handle_finish(self, event):
        process = event.process
        process.finish_time = self.current_time
        process.remaining_time = 0
        self.running_process = None

    def start_next_process(self):
        if self.running_process is not None:
            return

        if not self.ready_queue:
            return

        process = self.scheduler.select(self.ready_queue, self.current_time)
        self.running_process = process
        self.run_start_time = self.current_time

        if process.start_time is None:
            process.start_time = self.current_time

        allowed_time = self.scheduler.run_duration(process)
        duration = min(allowed_time, process.remaining_time)
        event_time = self.current_time + duration

        if duration == process.remaining_time:
            event = FinishEvent(event_time, process)
        else:
            event = TimerEvent(event_time, process)

        self.event_queue.add(event)
    def handle_timer(self, event):
        process = event.process
        elapsed = self.current_time - self.run_start_time
        process.remaining_time -= elapsed
        self.ready_queue.append(process)
        self.running_process = None
    def run(self):
        while not self.event_queue.is_empty():
            event = self.event_queue.pop()
            self.current_time = event.time

            if event.event_type == "arrival":
                self.handle_arrival(event)
            elif event.event_type == "finish":
                self.handle_finish(event)
            elif event.event_type == "timer":
                self.handle_timer(event)

            if (
                not self.event_queue.is_empty()
                and self.event_queue.peek_time() == self.current_time
            ):
                continue

            self.start_next_process()

        return self.processes