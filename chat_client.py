"""
chat room 客户端
发送请求,展示结果
"""

from socket import *
import os,sys

# 服务器地址
ADDR = ("127.0.0.1",1605)

# 发送消息
def send_msg(s,name):
    while True:
        try:
            text = input(">>")
        # 键盘退出或者其他异常直接视为退出
        except(KeyboardInterrupt,SyntaxError):
            text = "quit"
        if text.strip() == "quit":  # strip去除两边空格
            msg = "Q " + name
            s.sendto(msg.encode(),ADDR)
            sys.exit("退出群聊")
        msg = "C %s %s" % (name,text)
        s.sendto(msg.encode(),ADDR)

# 接收消息
def recv_msg(s):
    while True:
        data,addr = s.recvfrom(4096)
        # 接收到EXIT,父进程也退出,该用户即可推出
        if data.decode() == "EXIT":
            sys.exit()
        print(data.decode() + "\n>>",end = "")

# 搭建网络
def main():
    s = socket(AF_INET,SOCK_DGRAM)

    #进入聊天室
    while True:
        name = input("请输入用户名:")
        msg = "L " + name
        s.sendto(msg.encode(),ADDR)
        # 接收反馈
        data,addr = s.recvfrom(128)
        if data.decode() == "OK":
            print("欢迎您加入群聊")
            break
        else:
            print(data.decode())

    # 已经进入聊天室
    pid = os.fork()
    if pid < 0:
        sys.exit("进程错误!")
    elif pid == 0:
        send_msg(s,name)
    else:
        recv_msg(s)



if __name__ == '__main__':
    main()
