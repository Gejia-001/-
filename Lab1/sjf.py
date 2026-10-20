# 组员B负责：短作业优先，非抢占式。
class SJFScheduler:
    def select(self, ready_queue, current_time):
        index = min(
            range(len(ready_queue)),
            key=lambda i: ready_queue[i].burst_time,
        )
        return ready_queue.pop(index)

    def run_duration(self, process):
        return process.remaining_time
