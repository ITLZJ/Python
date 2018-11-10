#------------------Bird Code----------------------------

#对话框实现首页的三个选项----聊天，退出，私聊，并且每个按钮弹出不同的对话框进行操作
#实现单独聊天在滚动聊天记录中能够显示其唯一的端口，也就是建立公共聊天服务器的时候开启多线程，同一个IP地址对每个客户端采用不同的端口号
#暂时不考虑从公共聊天室中转到私聊的功能选项
#---------代表后继优化
from tkinter import messagebox
from tkinter import *
from tkinter import scrolledtext#滚动显示文本内容
import tkinter as tk
from Experiment_1_Server import *
from Experiment1_killChildProcess import stop_thread#子进程的关闭
import threading
import random
import time
class Talk_Room:
#登录界面
    def Load_tk(self):
        self.load_root = Tk()
        self.load_root.title("欢迎使用UDP聊天程序")
        self.load_root.geometry('390x130+754+378')
        self.Load_Lable()
        self.Load_Entry_text()
        self.Load_Button()
        self.load_root.mainloop()
    #控件实现（下同）
    def Load_Lable(self):
        self.L_lable_1 = Label(self.load_root,text = '用户名：',font = ('微软雅黑',10))
        self.L_lable_1.grid(row = 0,column = 0)
        self.L_lable_1.bind('<Key-Return>',self.Load_client)
        self.L_lable_2 = Label(self.load_root,text = '密码：',font=('微软雅黑',10))
        self.L_lable_2.grid(row = 1,column=0)
    #输入框
    def Load_Entry_text(self):
        self.res = StringVar()
        self.L_entrytext_1 = Entry(self.load_root,width = 20,font=('微软雅黑',10))
        self.L_entrytext_1.grid(row = 0,column=1)
        self.L_entrytext_2 = Entry(self.load_root,width = 20,font = ('微软雅黑',10))
        self.L_entrytext_2.grid(row = 1,column=1)
        self.L_entrytext_2['show'] = '*'#密码不显示
    #按钮
    def Load_Button(self):
        self.L_button_1 = Button(self.load_root,text = '登录',width = 10,font = ('华文行楷',16),command=self.Load_client)
        self.L_button_1.grid(row = 2,column = 0,sticky=W)
        self.L_button_2 = Button(self.load_root,text = '注册',width = 10,font=('华文行楷',16),command = self.Regist_tk)
        self.L_button_2.grid(row = 2,column = 1)
        self.L_button_3 = Button(self.load_root,text = '退出',width = 10,font=('华文行楷',16),command =self.CloseWindow_load)
        self.L_button_3.grid(row = 2,column = 2)


#注册界面
    def Regist_tk(self):
        self.regist_root = Toplevel(self.load_root)
        self.regist_root.title('欢迎注册')
        self.regist_root.geometry('280x116+764+410')
        self.Regist_Lable()
        self.Regist_Entry_text()
        self.Regist_Button()
        self.regist_root.mainloop()
    def Regist_Lable(self):
        self.R_lable_1 = Label(self.regist_root,text = '用户名：',font = ('微软雅黑',10))
        self.R_lable_1.grid(row = 0,column = 0)
        self.R_lable_2 = Label(self.regist_root,text = '密码：',font=('微软雅黑',10))
        self.R_lable_2.grid(row = 1,column=0)
    def Regist_Entry_text(self):
        self.R_entrytext_1 = Entry(self.regist_root,width = 20,font=('微软雅黑',10))
        self.R_entrytext_1.grid(row = 0,column=1)
        self.R_entrytext_2 = Entry(self.regist_root,width = 20,font = ('微软雅黑',10))
        self.R_entrytext_2.grid(row = 1,column=1)
    def Regist_Button(self):
        self.R_button_1 = Button(self.regist_root,text = '注册',width = 10,font = ('华文行楷',16),command=self.Regist_client)
        self.R_button_1.grid(row = 2,column = 0,sticky=W)
        self.R_button_2 = Button(self.regist_root,text = '取消',width = 10,font=('华文行楷',16),command = self.CloseWindow_Regist)
        self.R_button_2.grid(row = 2,column = 1)


#选择界面
    def init_tk(self):
        self.CloseWindow_load()#关闭登录界面，防止程序冲突
        self.root1 =Tk()
        self.root1.title('选择聊天界面')
        self.root1.geometry('334x282+754+378')
        self.init_Button()
        self.root1.mainloop()
    def init_Button(self):
        i_Button_1  = Button(self.root1,text ='聊天',width = 10,font = ("华文行楷",20),command = self.Public_Talkroom_tk)
        i_Button_1.pack(expand = "yes")
        i_Button_2 = Button(self.root1,text = '私聊',width = 10,font = ('华文行楷',20),command = self.Private_Talk)
        #Button_2.grid(row=1,column = 2)
        i_Button_2.pack(expand="yes")
        i_Button_3 = Button(self.root1,text = '退出',width = 10,font = ('华文行楷',20),command = self.CloseWindow_choice)
        #Button_3.grid(row=1,column = 4)
        i_Button_3.pack(expand="yes")


#聊天对话框模版
    def Public_Talkroom_Lable(self,TK):
        self.P_lable_1 = Label(TK,text = '聊天记录',font = ('微软雅黑',25))
        self.P_lable_1.grid(row = 0,column = 0,sticky = W)
        self.P_lable_2 = Label(TK,text = '消息输入框：',font=('微软雅黑',25))
        self.P_lable_2.grid(row =200,column=0,sticky=W)

    """
    向滚动框加入文本显示的网址：https://blog.csdn.net/weixin_42249184/article/details/81319403
    批量与优化：https://blog.csdn.net/up1012/article/details/79933628
    """
    def Public_Talkroom_Button(self,TK,Scmd,Ecmd):
        self.P_button_1 = Button(TK,text = '发送',width = 10,font = ('华文行楷',16),command = Scmd)
        self.P_button_1.grid(row = 202,column = 0,sticky=W)
        self.P_button_2 = Button(TK,text = '退出',width = 10,font=('华文行楷',16),command = Ecmd)#--------------如果消息框内还有消息则提醒用户
        self.P_button_2.grid(row = 202,column = 1,sticky=E)

#公共聊天室界面-------建立一个客户端，当用户退出时，关闭客户端程序
    def Public_Talkroom_tk(self):
        self.root = Toplevel(self.root1)
        self.root.title('多人实时聊天软件')
        self.root.geometry('518x521+552+204')
        self.Public_Talkroom_Lable(self.root)
        self.Public_Talkroom_Entry_text()
        self.Public_Talkroom_Button(self.root,self.Public_send_data,self.ClosWindow_TalkRoom)
        self.t = threading.Thread(target=self.P_input_data)
        self.t.start()
        self.DHCP_IP = str(random.randint(0,128))+'.'+str(random.randint(0,255))+'.'+str(random.randint(0,255))+'.'+str(random.randint(0,255))
        self.root.mainloop()

    def Public_Talkroom_Entry_text(self):
        self.P_entrytext_1 = scrolledtext.ScrolledText(self.root,width =70,height =25,wrap = tk.WORD)
        """  wrap=tk.WORD
         这个值表示在行的末尾如果有一个单词跨行，会将该单词放到下一行显示,比如输入hello，
         he在第一行的行尾,llo在第二行的行首, 这时如果wrap=tk.WORD，则表示会将 hello 这个单词挪到下一行行首显示, wrap默认的值为tk.CHAR
        """
        self.P_entrytext_1.grid(row = 1,columnspan=3)
        self.P_entrytext_2 = Entry(self.root,width = 20,font = ('华文行楷',20))
        self.P_entrytext_2.grid(row =201,columnspan=20)
#私聊界面
    def Private_TalkWindow(self):
        self.p_root = Toplevel(self.root1)
        self.p_root.title('单人聊天室')
        self.p_root.geometry('518x521+552+204')
        self.Public_Talkroom_Lable(self.p_root)
        self.Private_Talkroom_Entry_text()
        self.Public_Talkroom_Button(self.p_root,self.Private_sendData,self.sc_WindowClose)
        self.m = threading.Thread(target=self.S_input_data)
        self.m.start()
        self.p_root.mainloop()



    def Private_Talkroom_Entry_text(self):
        self.S_entrytext_1 = scrolledtext.ScrolledText(self.p_root,width =70,height =25,wrap = tk.WORD)
        self.S_entrytext_1.grid(row = 1,columnspan=3)
        self.S_entrytext_2 = Entry(self.p_root,width = 20,font = ('华文行楷',20))
        self.S_entrytext_2.grid(row =201,columnspan=20)
    def Private_Talk(self):
        self.sc_root = Toplevel(self.root1)
        self.sc_root.title('地址输入')
        self.sc_root.geometry('352x126+761+452')
        self.sc_Lable()
        self.sc_Entry()
        self.sc_Button()
        self.sc_root.mainloop()
    def sc_Lable(self):
        self.sc_lale = Label(self.sc_root,text = '请输入指定IP',font = ('微软雅黑',10))
        self.sc_lale.grid(row = 0,column=0,sticky = W)
    def sc_Entry(self):
        self.sc_entry = Entry(self.sc_root,width=10,font = ('微软雅黑',20))
        self.sc_entry.grid(row = 1,column=1,sticky=E)
    def sc_Button(self):
        self.sc_button_1= Button(self.sc_root,text = '确定',width = 10,font = ('华文行楷',15),command = self.sc_yes)
        self.sc_button_1.grid(row = 2,column=0,sticky=E)
        self.sc_button_2 = Button(self.sc_root, text='退出', width=10, font=('华文行楷', 15), command=self.sc_exit)
        self.sc_button_2.grid(row=2, column=4, sticky=W)


#按钮动作事件
    def Load_client(self):#登录
        user = str(self.L_entrytext_1.get())
        pwd  = str(self.L_entrytext_2.get())
        global Gname
        Gname = user
        if user == '':
            messagebox.showinfo('警告','用户名不能为空')
        elif pwd=='':
            messagebox.showinfo('警告', '密码不能为空')
        else:
            check_data = user+'    '+pwd+'---zhuyi_这是检查'
            self.RC_Send_Connect(check_data)
            ANY = '0.0.0.0'
            MCAST_ADDR = '224.168.2.9'
            MCAST_PORT = 1600
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # 创建UDP socket
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许端口复用
            sock.bind((ANY, MCAST_PORT))  # 绑定监听多播数据包的端口
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)  # 告诉内核这是一个多播类型的socket
            status = sock.setsockopt(socket.IPPROTO_IP,  # 告诉内核把自己加入指定的多播组，组地址由第三个参数指定
                                     socket.IP_ADD_MEMBERSHIP,
                                     socket.inet_aton(MCAST_ADDR) + socket.inet_aton(ANY))
            sock.setblocking(0)
            while 1:
                try:
                    data, addr = sock.recvfrom(1024)
                except socket.error as e:
                    pass
                else:
                    if 'L' in data.decode('gbk'):
                        final = data.decode('gbk').split('-')[1]
                        if final == 'yes':
                            self.user_online = user
                            self.init_tk()
                            break
                        elif final == 'psw':
                            messagebox.showinfo('警告', '请输入正确的密码')
                            self.L_entrytext_2.delete('0', 'end')
                            break
                        elif final == 'online':
                            messagebox.showinfo('提示', '用户已经登录')
                            break
                        elif final == 'fail':
                            messagebox.showinfo('警告', '请输入正确的用户名')
                            self.L_entrytext_1.delete('0', 'end')
                            break
                        else:
                            break
                    else:
                        break
    def Regist_client(self):#注册
        user = self.R_entrytext_1.get()
        pwd = self.R_entrytext_2.get()
        if user == '':
            messagebox.showinfo('警告','用户名不能为空')
        elif pwd=='':
            messagebox.showinfo('警告', '密码不能为空')
        else:
            Regist_data = user+'    '+pwd+'---zhuyi_这是Register'
            self.RC_Send_Connect(Regist_data)
            ANY = '0.0.0.0'
            MCAST_ADDR = '224.168.2.9'
            MCAST_PORT = 1600
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # 创建UDP socket
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许端口复用
            sock.bind((ANY, MCAST_PORT))  # 绑定监听多播数据包的端口
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)  # 告诉内核这是一个多播类型的socket
            status = sock.setsockopt(socket.IPPROTO_IP,  # 告诉内核把自己加入指定的多播组，组地址由第三个参数指定
                                     socket.IP_ADD_MEMBERSHIP,
                                     socket.inet_aton(MCAST_ADDR) + socket.inet_aton(ANY))
            sock.setblocking(0)
            while 1:
                try:
                    data, addr = sock.recvfrom(1024)
                except socket.error as e:
                    pass
                else:
                    if 'R' in data.decode('gbk'):
                        final = data.decode('gbk').split('-')[1]
                        if final == 'Success':
                            messagebox.showinfo('恭喜', '注册成功！')
                            self.CloseWindow_Regist()
                            break
                        elif final == 'Fail':
                            messagebox.showinfo('提示', '注册失败，用户名已经存在请重新注册')
                            self.R_entrytext_1.delete('0', 'end')  # 清空用户名中的内容
                            break
                        else:
                            break
                    else:
                        break


    def sc_yes(self):#输入地址后确定按钮发送事件
        self.tempdata = self.sc_entry.get()#记下私聊对象地址
        self.sc_exit()
        self.Private_TalkWindow()

#关闭事件
    def ClosWindow_TalkRoom(self):#聊天室界面
        stop_thread(self.t)
        self.root.destroy()

    def CloseWindow_load(self):#强制关闭登录界面
        try:
            self.load_root.destroy()
        except Exception:
            self.CloseWindow_load()
    def CloseWindow_Regist(self):#关闭注册界面
        self.regist_root.destroy()
    def CloseWindow_choice(self):#选择界面
        if User_Exit(self.user_online):#同时活跃中用户退出
            self.root1.destroy()
        else:
            self.CloseWindow_choice()
    def sc_exit(self):#地址输入界面
        self.sc_root.destroy()
    def sc_WindowClose(self):#单独聊天室界面
        stop_thread(self.m)
        self.p_root.destroy()


#                   功能实现
#输入公共聊天室，不断接收消息送入对话框
    def P_input_data(self):
        ANY = '0.0.0.0'
        MCAST_ADDR = '224.168.2.9'
        MCAST_PORT = 1600
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # 创建UDP socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许端口复用
        sock.bind((ANY, MCAST_PORT))  # 绑定监听多播数据包的端口
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)  # 告诉内核这是一个多播类型的socket
        status = sock.setsockopt(socket.IPPROTO_IP,  # 告诉内核把自己加入指定的多播组，组地址由第三个参数指定
                                 socket.IP_ADD_MEMBERSHIP,
                                 socket.inet_aton(MCAST_ADDR) + socket.inet_aton(ANY))
        sock.setblocking(0)
        ts = time.time()
        while 1:
            try:
                data, addr = sock.recvfrom(1024)
            except socket.error as e:
                pass
            else:
                if '@' in data.decode('utf-8'): #@作为向公共聊天室发送的判断字符
                    F_data = data.decode('utf-8').split(':')
                    self.P_entrytext_1.insert(END, F_data[0]+':'+'\n')
                    self.P_entrytext_1.insert(END, F_data[1] + '\n')
                else:
                    pass
# 私聊模式接收端
    def S_input_data(self):
        ANY = '0.0.0.0'
        MCAST_ADDR = '224.168.2.9'
        MCAST_PORT = 1600
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # 创建UDP socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许端口复用
        sock.bind((ANY, MCAST_PORT))  # 绑定监听多播数据包的端口
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)  # 告诉内核这是一个多播类型的socket
        status = sock.setsockopt(socket.IPPROTO_IP,  # 告诉内核把自己加入指定的多播组，组地址由第三个参数指定
                                 socket.IP_ADD_MEMBERSHIP,
                                 socket.inet_aton(MCAST_ADDR) + socket.inet_aton(ANY))
        sock.setblocking(0)
        ts = time.time()
        while 1:
            try:
                Data_0, addr = sock.recvfrom(1024)
                F_data = Data_0.decode('utf-8')
                if 'ox_cde' in F_data:
                    P_data = F_data.split('ox_cde')
                    if P_data[0] == self.DHCP_IP or P_data[0] ==self.tempdata:  # 接收属于自己的消息
                        self.S_entrytext_1.insert(END, P_data[0] + ':' + '\n')
                        self.S_entrytext_1.insert(END, P_data[1] + '\n')
                    else:
                        pass
                else:
                    pass
            except socket.error as e:
                pass

#公共聊天发送口
    def Public_send_data(self):
        MCAST_PORT = 1501
        text =self.DHCP_IP+'@'+Gname+':'+self.P_entrytext_2.get()
        self.P_entrytext_2.delete('0','end')#清空输入栏
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.sendto(text.encode('utf-8'),('127.0.0.1',MCAST_PORT))

#私聊发送
    def Private_sendData(self):
        MCAST_PORT = 1501
        text = self.tempdata+'ox_cde'+self.S_entrytext_2.get()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.S_entrytext_2.delete('0', 'end')  # 清空输入栏
        sock.sendto(text.encode('utf-8'), ('127.0.0.1', MCAST_PORT))

#检查z注册链接
    def RC_Send_Connect(self,text):
        MCAST_PORT = 1501
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(text.encode('utf-8'), ('127.0.0.1', MCAST_PORT))


#私聊连接
    def Private_connect(self):
        text = self.tempdata+'$'
        c = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        c.sendto(text.encode('utf-8'),('127.0.0.1',1501))


if __name__ == "__main__":
    t = Talk_Room()
    t.Load_tk()