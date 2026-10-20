# 组员A负责：主入口，统一接入四种算法。
from process import Process
from simulator import Simulator
from fcfs import FCFSScheduler
from sjf import SJFScheduler
from hrrf import HRRFScheduler
from rr import RRScheduler
from report import print_report
from input_data import read_processes, read_int

processes = [
    Process("A", 0, 3, 1),
    Process("B", 2, 6, 1),
    Process("C", 4, 4, 1),
    Process("D", 6, 5, 1),
    Process("E", 8, 2, 1),
]
print("1. 使用老师测试案例")
print("2. 手动输入作业")

while True:
    choice = input("请选择 1 或 2：").strip()
    if choice in ("1", "2"):
        break
    print("请选择 1 或 2。")

if choice == "2":
    processes = read_processes()
print("1. FCFS  2. SJF  3. HRRF  4. RR")
algorithm = read_int("请选择算法 1 至 4：", 1)
while algorithm not in (1, 2, 3, 4):
    algorithm = read_int("请选择算法 1 至 4：", 1)

if algorithm == 1:
    scheduler, algorithm_name = FCFSScheduler(), "FCFS"
elif algorithm == 2:
    scheduler, algorithm_name = SJFScheduler(), "SJF"
elif algorithm == 3:
    scheduler, algorithm_name = HRRFScheduler(), "HRRF"
else:
    quantum = read_int("请输入正整数时间片：", 1)
    scheduler, algorithm_name = RRScheduler(quantum), f"RR 时间片 {quantum}"

simulator = Simulator(scheduler)

simulator.load_processes(processes)
results = simulator.run()

print_report(results, algorithm_name)
