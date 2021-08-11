import multiprocessing
import random
import math
import time
import numpy as np
import copy

# ランダムなリストの生成
def generate_num(n):
    num_list = []
    for i in range(n):
        num = random.randint(1,100)
        num_list.append(num)
    return num_list

# 通常のバブルソート
def BubbleSort(num):
    for i in range(len(num)):
        for j in range(len(num)-1, i, -1):
            if num[j] < num[j-1]:
                num[j], num[j-1] = num[j-1], num[j]
    return num

# 小分けバブルソート
def a_Bubble(num):
    for i in range(len(num)):
        if num[i] < num[i-1]:
                num[i], num[i-1] = num[i-1], num[i]
    return num

"""
# n個のプロセッサモジュールを使う
def useProcessor(n, num):
    for i in range(num):
        yield num[i * len(num) // n:(i + 1) * len(num) // n]
"""

if __name__ == '__main__':
    ini_list = generate_num(100) # 初期値生成
    print("初期リスト：{}".format(ini_list))
    
    # 通常処理
    num = copy.copy(ini_list)
    t1 = time.time()
    res1 = BubbleSort(num)
    t2 = time.time()
    print("通常処理結果：{}".format(res1))
    print("通常処理計測時間：{}".format(t2-t1))
    print("--------------------------------------------------------")
    #useProcessor(num,4)
    #print(num)


    # 並列アルゴリズム
    num = copy.copy(ini_list)
    res2 = []
    roop_num = 3
    t3 = time.time()
    # queue = multiprocessing.Queue()
    for i in range(len(num)):
        divide_num = list(np.array_split(num, 4)) # リストを4分割

        # プロセス生成
        p0 = multiprocessing.Process(target=a_Bubble, args=(divide_num[0],))
        p1 = multiprocessing.Process(target=a_Bubble, args=(divide_num[1],))
        p2 = multiprocessing.Process(target=a_Bubble, args=(divide_num[2],))
        p3 = multiprocessing.Process(target=a_Bubble, args=(divide_num[3],))
        
        # プロセス開始
        p0.start()
        p1.start()
        p2.start()
        p3.start()
        
        # プロセス終了待ち合わせ
        p0.join()
        p1.join()
        p2.join()
        p3.join()

        for i in range(roop_num):
            if divide_num[i][-1] > divide_num[i+1][-1]:
                divide_num[i][-1], divide_num[i+1][-1] = divide_num[i+1][-1], divide_num[i][-1]
        res2.insert(0, divide_num[roop_num][-1])
        divide_num[roop_num] = divide_num[roop_num][:-1]

        num = []
        num.extend(divide_num[0])
        num.extend(divide_num[1])
        num.extend(divide_num[2])
        num.extend(divide_num[3])

        if len(num) == 3:
            roop_num = 2
        elif len(num) == 2:
            roop_num = 1
        elif len(num) == 1:
            t4 = time.time()
            print("並列処理結果：{}".format(res2))
            print("並列処理計測時間：{}".format(t4-t3))
            break