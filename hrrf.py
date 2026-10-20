# 组员B负责：高响应比优先，非抢占式。
class HRRFScheduler:
    def select(self, ready_queue, current_time):
        index = max(
            range(len(ready_queue)),
            key=lambda i: (
                current_time - ready_queue[i].arrival_time
                + ready_queue[i].burst_time
            ) / ready_queue[i].burst_time,
        )
        return ready_queue.pop(index)

    def run_duration(self, process):
        return process.remaining_time
