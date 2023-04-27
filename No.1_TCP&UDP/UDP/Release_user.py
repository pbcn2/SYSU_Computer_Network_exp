from socket import *
from datetime import datetime
import threading 
import time

HOST = '172.28.53.135'  # 服务器连接地址
PORT = 8080  # 服务器启用端口
BUFSIZ = 1024  # 缓冲区大小
ADDR = (HOST, PORT)

udpCliendSocket = socket(AF_INET, SOCK_DGRAM)

# 一个计数变量
count = 0
time_start = '' # 第一个包的送达时间
time_end = 0  # 最后一个包的送达时间
ADDA = 0  # 目的地信息

def recv_timeout():
    pass  #为了配合函数调用变量需要设置的无用函数

def delta(time_start, time_end):
    # 将时间戳bytes字符串转换为字符串，并使用切片操作获取时间戳部分
    time_start = time_start.decode('utf-8')[1:14]
    time_end = time_end.decode('utf-8')[1:14]

    # 将时间戳字符串转换为datetime对象
    dt1 = datetime.fromtimestamp(int(time_start) / 1000)
    dt2 = datetime.fromtimestamp(int(time_end) / 1000)
    print(dt1, dt2)

    # 计算两个datetime对象之间的时间差
    delta = dt2 - dt1
    return delta

print("正在ping", HOST, "端口号", PORT)

for i in range(10):
    data = '1'
    send_time = int(time.time() * 1000 + time.time_ns() % 1000000 // 1000)
    # 构造新的时间戳字符串
    send_time_str = bytes('[%d] %s' % (send_time, data), encoding='utf-8')
    # data = bytes(send_time_str, encoding="UTF-8")  # 发送时间戳信息

    ADDR = (HOST, PORT)  # 在每次循环中更新ADDR的值
    udpCliendSocket.sendto(send_time_str, ADDR)  # 调用发送接口
    udpCliendSocket.settimeout(1)  # 设置超时时间为1秒
    timer = threading.Timer(1.1, recv_timeout)  # 创建定时器线程，超时时间为1秒
    timer.start()  # 启动定时器线程
    data, ADDR = None, None
    try:  # 捕捉错误
        data, ADDR = udpCliendSocket.recvfrom(BUFSIZ)  # 等待接受服务器回应
        if not time_start:  # 如果当前的是第一个包
            time_start = data
        time_end = data
        count += 1  # 计数器加一
        print(send_time_str,time_end)
        print("连接成功...", delta(send_time_str, time_end))
        continue
    except timeout:
        print("请求超时。")  # 超时输出
        continue  # 超时后使用continue跳过本轮循环
    finally:
        udpCliendSocket.settimeout(None)  # 恢复默认的超时时间
        timer.cancel()  # 取消定时器线程


# 将时间戳bytes字符串转换为字符串，并使用切片操作获取时间戳部分
if time_start:
    # 将时间戳bytes字符串转换为字符串，并使用切片操作获取时间戳部分
    time_start = time_start.decode('utf-8')[1:14]
    time_end = time_end.decode('utf-8')[1:14]

    # 将时间戳字符串转换为datetime对象
    dt1 = datetime.fromtimestamp(int(time_start) / 1000)
    dt2 = datetime.fromtimestamp(int(time_end) / 1000)

    # 计算两个datetime对象之间的时间差
    delta = dt2 - dt1

    # 总共发送了十个数据包，count用于计数已经收到了的个数，输出丢失率
    print("==================================")
    print(ADDR, "的统计信息：")
    print("\t 数据包：已发送 = 10, 已接收 =", count, ", 丢失 =", 10 - count, "(", 100 * (10 - count) / 10, "% 丢失)")
    print("往返行程的总时间：")
    print("\t",delta)
else:
    print("未收到任何时间戳数据包")
    print("请检查连接（IP or  Port）是否正确")
    
udpCliendSocket.close()
