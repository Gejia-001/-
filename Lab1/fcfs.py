class FCFSScheduler:
    def select(self, ready_queue, current_time):
        return ready_queue.pop(0)

    def run_duration(self, process):
        return process.remaining_time
    