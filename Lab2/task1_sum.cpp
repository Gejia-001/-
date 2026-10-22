// task1_sum.cpp —— 用子线程计算 1 + 2 + ... + n
// 编译: g++ -std=c++20 -O2 -pthread task1_sum.cpp -o task1_sum
// 运行: ./task1_sum 1000000

#include <cstdio>
#include <cstdlib>
#include <thread>

#ifdef _WIN32
#  include <windows.h>
#endif

long long sum = 0;              // 主线程和子线程都能访问的全局变量

// 子线程要执行的函数
void compute(long long n) {
    long long s = 0;
    for (long long i = 1; i <= n; ++i) s += i;
    sum = s;                    // 算完一次性写进去；主线程 join 之后才读，不会有半成品
}

int main(int argc, char* argv[]) {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);            // Windows 控制台默认不是 UTF-8，中文会乱码
#endif

    if (argc != 2) {
        printf("用法: %s 一个整数\n", argv[0]);
        return 1;
    }
    long long n = atoll(argv[1]);

    std::thread t(compute, n);              // 创建线程，参数 n 直接传给 compute
    printf("主线程：子线程已启动，我来等它\n");

    t.join();                               // 阻塞，直到子线程结束
    printf("1..%lld 的和 = %lld\n", n, sum);
    return 0;
}
