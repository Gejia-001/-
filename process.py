class Process:
    def __init__(self, name, arrival_time, burst_time, priority):#作业名，到达时间，执行时间，优先级
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.start_time = None
        self.finish_time = None
#__init__方法是类的构造函数，用于初始化对象的属性。会在创建一个进程时自动执行，self 表示当前这个进程。
#remaining_time 保存剩余运行时间，初始值等于运行时间，后面的 RR 算法会用到它
#始和结束时间暂时填 None，表示尚未发生，之后由模拟程序填写。