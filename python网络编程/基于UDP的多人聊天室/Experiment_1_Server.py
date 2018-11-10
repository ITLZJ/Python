#------------------Bird Code----------------------------

import socket
MAX_BYTES = 65535#定义最大长度
import time
import os
Default_path = 'D:/Data/'#初始存储文件路径
#服务器端数据加载
def Import_DB():
    username = []
    password = []
    with open('D:/Data/Secret.txt','r') as f:
        init_data = f.read().split('\n')
    for i in range(len(init_data)-1):#采用txt存储的方式在读取过程中最后会有一个空格字符，导致程序运行失败
        username.append(init_data[i].split('    ')[0])
        password.append(init_data[i].split('    ')[1])
    Temp_data = dict(zip(username,password))
    return  Temp_data
#注册端
def Regist_Server(txt):
    if txt.split('    ')[0] in Import_DB().keys():#只限制用户名不能相同
        return 'R-Fail'
    else:
        try:
            with open('D:/Data/Secret.txt','a+') as f:
                f.write(txt+'\n')
        except Exception:
            pass
        return 'R-Success'
#登录检查端
#       检查用户名以及密码是否正确
def Check_Server(data):
    if data.split('    ')[0] in Import_DB().keys():#检查用户名
        if ChenkUser_online(data.split('    ')[0]):  # 检查是否在线
            if data.split('    ')[1] == Import_DB()[data.split('    ')[0]]:#检查密码
                with open('D:/Data/online.txt', 'a+') as f:
                    f.write(data.split('    ')[0]+'\n')
                return 'L-yes'
            else:
                return 'L-psw'
        else:
            return 'L-online'
    else:
        return 'L-fail'

#       检查用户是否已经登录--Way:创建txt保存在线用户，用户退出时从txt中去掉该用户，后继可以实现在线用户的直观界面
def ChenkUser_online(user):
    with open('D:/Data/online.txt', 'r+') as f:
        m = f.read()
        online_user = m.split('\n')
    if user not in online_user:
        return 1
    else:
        return 0
#用户退出
def User_Exit(user):
    with open('D:/Data/online.txt', 'r+') as f:
        m=f.read().split('\n')
    with open('D:/Data/online.txt', 'w') as f:
        f.write('')
    try:
        m.remove(user)
        with open('D:/Data/online.txt', 'a+') as f:
            for i in range(len(m)):
                f.write(m[i]+'\n')
        return 1
    except Exception:
        return 0

#服务器中转
def Brocast_Server_Public():
    ANY = '0.0.0.0'
    SENDERPORT=1501
    MCAST_ADDR = '224.168.2.9'
    MCAST_PORT = 1600

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind((ANY,SENDERPORT)) #绑定发送端口到SENDERPORT，即此例的发送端口为1501
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255) #设置使用多播发送
    while 1:
        data,addr = sock.recvfrom(1024)
        temp_data=data.decode('utf-8')
        if 'zhuyi_这是检查' in temp_data:
            check_data = temp_data.split('---')[0]
            sock.sendto(Check_Server(check_data).encode('gbk'),(MCAST_ADDR,MCAST_PORT))
        elif 'zhuyi_这是Register' in temp_data:
            Regist_data = temp_data.split('---')[0]
            sock.sendto(Regist_Server(Regist_data).encode('gbk'), (MCAST_ADDR, MCAST_PORT))
        else:
            sock.sendto(data, (MCAST_ADDR,MCAST_PORT) )#将数据发送到多播地址的指定端口，属于这个多播组的成员都可以收到这个信息
#w文件创建
def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(path)
    try:
        if not isExists:
            os.mkdir(path)
            password_txt = Default_path+'Secret.txt'
            online_txt = Default_path+'online.txt'
            with open(password_txt, 'w') as f:
                f.write('')
            with open(online_txt, 'w') as f:
                f.write('')
            return 1
        else:
            return 'Exist'

    except Exception:
        return 0

def Server_init():#服务器端初始化，用于把程序转移到他人电脑上使用
    if mkdir(Default_path):
        print("初始化成功")
        return 1
    else:
        print('初始化失败服务器退出')
        return 0

if __name__ == "__main__":
    if Server_init():
        Brocast_Server_Public()
    else:
        os.popen('taskkill.exe /f /pid:' + str(os.getpid()))  # 服务器端程序退出


