from process import Process


def read_int(prompt, minimum=None):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("请输入一个整数。")
            continue

        if minimum is not None and value < minimum:
            print(f"请输入不小于 {minimum} 的整数。")
            continue

        return value

def read_processes():
    count = read_int("请输入作业数量：", 1)
    processes = []
    names = set()

    for index in range(count):
        print(f"\n请输入第 {index + 1} 个作业的信息")

        while True:
            name = input("作业名：").strip()
            if name and name not in names:
                names.add(name)
                break
            print("作业名不能为空，也不能重复。")

        arrival_time = read_int("到达时间：", 0)
        burst_time = read_int("所需运行时间：", 1)
        priority = read_int("优先级：")

        process = Process(name, arrival_time, burst_time, priority)
        processes.append(process)

    return processes