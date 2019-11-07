"""
chat room
env:python3.6
socket udp & fork exc
"""

from socket import *
import os,sys

# 全局变量:很多封装模块,或者有特定含义的变量都要用
HOST = "127.0.0.1"
PORT = 1605
ADDR = (HOST,PORT)

# 存储用户{name:address}
user = {}

# 处理用户登录
def do_login(s,name,addr):
    if name in user or "管理员" in name:
        s.sendto("\n用户名已存在".encode(),addr)
        return
    else:
        s.sendto(b"OK",addr) # 可以进入
    # 通知其他人
    msg = "\n欢迎 %s 加入群聊" % name
    for i in user:
        s.sendto(msg.encode(),user[i]) # user[i]为已在群聊(字典)里用户的地址
    user[name] = addr # 新用户加入字典

# 处理聊天
def do_chat(s,name,text):
    msg = "\n%s : %s" % (name,text)
    for i in user:
        # 不能发送给自己
        if i != name:
            s.sendto(msg.encode(),user[i])

# 处理退出
def do_quit(s,name):
    msg = "\n%s 退出群聊" % name
    for i in user:
        # 将EXIT返回给name用户,使其退出
        if i == name:
            s.sendto(b"EXIT",user[i])
        else:
            s.sendto(msg.encode(),user[i])
    del user[name]

# 循环接收客户端请求
def do_request(s):
    while True:
        data,addr = s.recvfrom(1024)
        # 只切前两项,防止用户输入的消息中有空格也被切掉
        tmp = data.decode().split(" ",2)
        # 根据不同的请求类型,执行不同的事件
        if tmp[0] == "L":
            do_login(s,tmp[1],addr)
        elif tmp[0] == "C":
            do_chat(s,tmp[1],tmp[2])
        elif tmp[0] == "Q":
            do_quit(s,tmp[1])

# 搭建网络
def main():
    # udp网络
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)
    pid = os.fork()
    if pid < 0:
        sys.exit("进程错误!")
    elif pid == 0:
        # 管理员消息处理(子进程发给父进程,父进程执行转发操作)
        while True:
            msg = input("请输入管理员消息:")
            msg = "C 管理员 " + msg
            s.sendto(msg.encode(),ADDR)
    else:
        do_request(s) # 接受客户端请求



if __name__ == '__main__':
    main()
