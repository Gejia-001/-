// task1_race.cpp —— 两个线程各把 counter 加 1 一千万次，看最后少了多少
// 编译: g++ -std=c++20 -O2 -pthread task1_race.cpp -o task1_race
// 运行: ./task1_race           不加锁，结果会少
//       ./task1_race --fix     加锁，结果正好

#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <mutex>
#include <string>
#include <thread>

#ifdef _WIN32
#  include <windows.h>
#endif

volatile int counter = 0;       // 两个线程共享的计数器
std::mutex   m;                 // 互斥锁，保护 counter
bool         useLock = false;   // 是否走加锁分支
long long    rounds  = 10000000; // 每个线程加多少次

// 线程函数：循环累加
void work() {
    for (long long i = 0; i < rounds; ++i) {
        if (useLock) {
            std::lock_guard<std::mutex> lock(m);   // 进临界区，离开作用域自动解锁
            counter = counter + 1;                 // C++20 起对 volatile 变量用 ++ 会告警，写成加法
        } else {
            counter = counter + 1;   // 读-加-写三步，中途可能被另一个线程插进来
        }
    }
}

// 画一条横向的对比条
void bar(const char* name, long long value, long long max) {
    int filled = (int)(value * 20 / max);
    if (filled > 20) filled = 20;

    std::string s;
    for (int i = 0; i < 20; ++i) s += (i < filled ? "█" : "░");
    printf("  %s  %s %lld\n", name, s.c_str(), value);
}

int main(int argc, char* argv[]) {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    for (int i = 1; i < argc; ++i) {        // 解析参数：--fix 开关 + 可选的次数
        if (strcmp(argv[i], "--fix") == 0) useLock = true;
        else rounds = atoll(argv[i]);
    }

    long long expect = rounds * 2;
    printf("模式: %s   每个线程加 %lld 次   期望结果 %lld\n",
           useLock ? "加锁(正确)" : "不加锁(有竞态)", rounds, expect);

    auto start = std::chrono::steady_clock::now();

    std::thread a(work);            // 两个线程同时跑同一个函数
    std::thread b(work);
    a.join();                       // 两个都等完再读结果
    b.join();

    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(
                  std::chrono::steady_clock::now() - start).count();

    printf("\n结果 counter = %d   耗时 %lld ms\n\n", counter, (long long)ms);
    bar("期望", expect,         expect);
    bar("实际", counter,        expect);
    bar("丢失", expect - counter, expect);

    printf("\n  %s\n", (counter == expect) ? "结果正确：一次也没丢"
                                          : "结果偏小：这就是竞态，属预期现象");
    return 0;               // 演示程序始终返回 0，免得 VS Code 把它标成"任务失败"
}
