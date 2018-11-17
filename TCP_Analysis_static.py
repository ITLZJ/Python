import scapy.all as scapy
import matplotlib.image as mpimg
import matplotlib
#------------------------------------数据报解析三次握手过程-------------------------------
def Extraction_From_Pcap(packets):
    a,b,c=[],[],[]#存储数据
    m,x=1,1#判定界限
    try:
        for f in packets:
            if str(f.payload.payload.name) == "TCP":#判断数据流是否为TCP
                src = f.payload.src
                dst = f.payload.dst
                sport = f.payload.payload.sport
                dport = f.payload.payload.dport
                seq = f.payload.payload.seq
                ack = f.payload.payload.ack

                #添加第一个IP报文，用于鉴别
                if m:
                    Array_Update(a,src,dst,sport,dport,seq,ack)
                    m=m-1#报文初始添加进列表
                elif x:
                    if all((src==a[1],dst==a[0],sport==a[3],dport==a[2])): #------检查这次的源端口是不是来自上次的目的地端口
                        Array_Update(b, src, dst, sport, dport, seq, ack)#-----添加进第二列表中，准备下一个检查
                        x = x-1
                    else:
                        del a[:]                                        #替换第一列表中的值为当数值
                        Array_Update(a, src, dst, sport, dport, seq, ack)
                else:
                    if all((src == b[1],dst ==b[0],sport == b[3],dport == b[2])):
                        Array_Update(c, src, dst, sport, dport, seq, ack)
                        TCP_Connect_show(a,b,c)
                        print('解析成功')
                        break
                    else:
                        del a[:]                                        #第三次检查不对，清空前两存储，修改第一列表为当数值
                        Array_Update(a, src, dst, sport, dport, seq, ack)
                        del b[:]
                        x+=1#用于重新判断
            else:
                pass
    except Exception as e:
        print("该数据报不存在TCP三次建立")

#-----------------------------------------更新数值---------------------------------------
def Array_Update(A,src,dst,sport,dport,seq,ack):
    A.append(src)
    A.append(dst)
    A.append(sport)
    A.append(dport)
    A.append(seq)
    A.append(ack)

#----------------------------------------返回总数据---------------------------------------
def Data_print(a,b,c):
    temp=[]
    temp.append('SRC:{}  ,DST:{}  ,{}----->{}'.format(a[0],a[1],a[2],a[3]))
    temp.append('SRC:{}  ,DST:{}  ,{}----->{}'.format(b[0], b[1], b[2], b[3]))
    temp.append('SRC:{}  ,DST:{}  ,{}----->{}'.format(c[0], c[1], c[2], c[3]))
    return temp

#-----------------------------------------添加箭头-----------------------------------------
def Mat_Arrow(plt):
    # 添加方向
    """
    ax.arrow(A[0], A[1], B[0] - A[0], B[1] - A[1], length_includes_head=True, head_width=10, head_length=10, fc=fc,
             ec=ec)
    A,B表示列表，代表箭头尾部和头部坐标，head_width代表箭头宽度，head_length代表箭头长度，fc为内部颜色,ec表示边框颜色
    ax.arrow(75, 50, 10, 0, length_includes_head=True, head_width=10, head_length=10, fc='r', ec='w')
    """
    plt.arrow(75, 50, 225, 0, length_includes_head=True, head_width=10, head_length=10, shape='left', linewidth=3,
              fc='b', ec='b')
    plt.arrow(300, 100, -225, 0, length_includes_head=True, head_width=10, head_length=10, shape='right', linewidth=3,
              fc='y', ec='y')
    plt.arrow(75, 150, 225, 0, length_includes_head=True, head_width=10, head_length=10, shape='left', linewidth=3,
              fc='g', ec='g')

#----------------------------------------文本添加-------------------------------------------
def Mat_Text(plt,a,b,c):
    """
     plt.text(x,y,text,fontsize,color),x,y,分别为坐标，text为字符串即文本内容，fontsize为字体大小，color为字体颜色
     """
    plt.text(75, 45, 'Seq:'+str(a[4]), fontsize=15, color='g')
    plt.text(75, 65,'Ack:'+str(a[5]), fontsize=15, color='g')
    plt.text(125, 95,'Seq:'+str(b[4]), fontsize=15, color='y')
    plt.text(125, 115,'Ack:'+str( b[5]), fontsize=15, color='y')
    plt.text(75, 145, 'Seq:'+str(c[4]), fontsize=15, color='g')
    plt.text(75, 165, 'Ack:'+str(c[5]), fontsize=15, color='g')
    plt.text(0, 20, 'SRC:'+a[0], fontsize=15, color='g')
    plt.text(300, 20, 'DST:'+a[1], fontsize=15, color='g')
    plt.text(-20, 100, 'PORT:'+str(a[2]), fontsize=13, color='r')
    plt.text(300, 100, 'PORT:'+str(a[3]), fontsize=13, color='r')
    plt.text(25,225,Data_print(a,b,c)[0]+'\n'+Data_print(a,b,c)[1]+'\n'+Data_print(a,b,c)[2],fontsize=13, color='b')

#---------------------------------------图片展示调用-----------------------------------------
def TCP_Connect_show(a,b,c):
    # 加载图片
    img = mpimg.imread('D:/pythonEdit/documentONe/Data/Experiment_2.png')
    plt = matplotlib.pyplot
    imgplot = plt.imshow(img)                                             #-----------------------展示图片，即画板建立
    Mat_Arrow(plt)                                                        #-----------------------增加箭头
    Mat_Text(plt,a,b,c)                                                   #-----------------------增加文本
    #plt.grid()                                                           #-----------------------网格显示,调试图片时使用
    plt.axis('off')  # 关闭坐标轴
    plt.show()  # 展示

#------------------------------------------程序启动--------------------------------------------
if __name__=="__main__":
    packets = scapy.rdpcap('./getData.pcap')                              #-----------------------可以当作列表来处理
    Extraction_From_Pcap(packets)