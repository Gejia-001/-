# 组员C负责：时间片轮转。
class RRScheduler:
    def __init__(self, quantum):
        if type(quantum) is not int or quantum <= 0:
            raise ValueError("时间片必须是正整数。")
        self.quantum = quantum

    def select(self, ready_queue, current_time):
        return ready_queue.pop(0)

    def run_duration(self, process):
        return self.quantum
