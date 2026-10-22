// task2_wordcount.cpp —— 两个线程各统计一个文件的单词数，累加到共享总数上
// 编译: g++ -std=c++20 -O2 -pthread task2_wordcount.cpp -o task2_wordcount
// 运行: ./task2_wordcount essay_a.txt essay_b.txt

#include <cctype>
#include <cstdio>
#include <semaphore>
#include <string>
#include <thread>

#ifdef _WIN32
#  include <windows.h>
#endif

std::binary_semaphore sem{1};   // 二值信号量，初值 1：acquire 就是 P，release 就是 V
int total = 0;                  // 共享的单词总数，必须受信号量保护
int perFile[2] = {0, 0};        // 每个线程自己的统计，只用来画图

// 判断这个字符是不是字母或数字（isalnum 只接受 0~255 或 EOF，所以先转 unsigned char）
bool letter(int c) {
    return c != EOF && isalnum((unsigned char)c) != 0;
}

// 线程函数：统计一个文件
void count(const char* file, int idx) {
    FILE* fp = fopen(file, "r");
    if (fp == nullptr) {
        printf("打不开 %s\n", file);
        return;
    }

    int c, prev = 0;
    int local = 0;                          // 本线程自己数了多少个

    while ((c = fgetc(fp)) != EOF) {
        if (!letter(c) && letter(prev)) {   // 分隔符跟在字母数字后面 = 一个单词结束
            sem.acquire();                  // P：申请进入临界区
            total++;
            sem.release();                  // V：离开临界区
            local++;
        }
        prev = c;
    }

    if (letter(prev)) {                     // 收尾：文件最后一个词后面没有分隔符
        sem.acquire();
        total++;
        sem.release();
        local++;
    }

    fclose(fp);
    perFile[idx] = local;                   // join 之后主线程才读，不用加锁
}

// 画一条横向的对比条
void bar(const std::string& name, int value, int max) {
    int filled = (max > 0) ? value * 28 / max : 0;
    if (filled > 28) filled = 28;

    std::string s;
    for (int i = 0; i < 28; ++i) s += (i < filled ? "█" : "░");
    printf("  %s %s %d\n", name.c_str(), s.c_str(), value);
}

int main(int argc, char* argv[]) {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    if (argc != 3) {
        printf("用法: %s 文件1 文件2\n", argv[0]);
        return 1;
    }

    std::thread t1(count, argv[1], 0);      // 一个线程统计第一个文件
    std::thread t2(count, argv[2], 1);      // 另一个线程统计第二个文件

    t1.join();                              // 两个都统计完
    t2.join();

    char pad1[64], pad2[64];                // 把文件名补齐到 12 列，让后面几条竖着对齐
    snprintf(pad1, sizeof pad1, "%-12s", argv[1]);
    snprintf(pad2, sizeof pad2, "%-12s", argv[2]);

    printf("\n");
    bar(pad1, perFile[0], total);
    bar(pad2, perFile[1], total);
    bar("总计        ", total, total);

    return 0;
}
