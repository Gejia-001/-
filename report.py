def print_report(processes, algorithm_name):
    if not processes:
        print("没有可输出的作业。")
        return

    print(f"\n=== {algorithm_name} 调度结果 ===")
    print("作业\t到达\t开始\t结束\t周转\t带权周转")

    total_turnaround = 0
    total_weighted_turnaround = 0

    for process in processes:
        turnaround = process.finish_time - process.arrival_time
        weighted_turnaround = turnaround / process.burst_time

        total_turnaround += turnaround
        total_weighted_turnaround += weighted_turnaround

        print(
            f"{process.name}\t{process.arrival_time}\t"
            f"{process.start_time}\t{process.finish_time}\t"
            f"{turnaround}\t{weighted_turnaround:.2f}"
        )

    count = len(processes)

    print(f"\n平均周转时间：{total_turnaround / count:.2f}")
    print(f"平均带权周转时间：{total_weighted_turnaround / count:.2f}")