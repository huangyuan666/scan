# -- coding: utf-8 --
import threading, socket,time,os,re,sys
from module import printc
from module import queue
from module import argparse
#扫描常用端口
PortList=[21,22,23,25,31,42,53,67,68,69,79,80,81,85,99,102,109,135,137,138,139,143,161,389,443,445,456,
513,554,593,635,636,646,873,902,903,912,913,993,1000,1001,1029,1011,1024,1043,1044,1080,1170,1234,1245,1433,1502,1536,
1537,1538,1539,1540,1542,1543,1544,1547,1548,1549,1801,1935,2066,2500,2504,2601,2602,2604,2869,3306,3389,3443,4000,4444,
4224,4444,
4900,5040,5357,
6000,6942,7680,7702,7720,7739,7777,7778,7779,7780,7807,7831,7833,8080,8085,8088,8888,8307,8443,8800,9015,9075,9081,9086,
9087,9095,9144,9156,9666,9999,12051,13223,14367,14601,14610,14611,14612,14613,14614,14615,14616,14617,14618,14619,
14620,14621,21440,21441,28317,35432,62078,63342,65000]
#判断主机是否存活的端口
ports=[80,443]
#线程个数
nThread = 80
#线程锁
lock = threading.Lock()
#超时时间
Timeout = 3
#打开的端口列表
OpenPort = []
#存活的主机列表
OpenHost= []
#存活端口的总数
openNum=0
#一个用于存放线程的数组
threads=[]
#得到一个队列
def GetQueue(list):
    PortQueue = queue.Queue(65535)
    for p in list:
        PortQueue.put(p)
    return PortQueue
#这是一个工具类,里面放着一些常见的工具函数

class Tool():
    global ports,PortList
    #判断用户输入的线程数
    def nThreads(self,num):
        global nThread
        num=int(num)
        if num>0 and num<201:
            nThread=num
    #将一个list赋值给另一个list
    def changeList(self,list1):
        list3=[]
        for i in list1:
            i=int(i.replace("=",''))
            list3.append(i)
        return list3
    #将一个字符串变为列表
    def split2List(self,string):
        list1=string.split(',')
        return list1
    #扫描从hosts.txt文件中读取出来的主机存活端口信息    
    def scan_host_ports(self,ip):
        s1 =  '[*] Scanning:{ip}'.format(ip=ip)
        printc.printf(s1, "skyblue")
        start_time = time.time()
        global nThread, PortList
        ThreadList = []
        strIP = ip
        SingleQueue = GetQueue(PortList)
        for i in range(0, nThread):
            t = ScanThreadSingle(strIP, SingleQueue)
            ThreadList.append(t)
        for t in ThreadList:
            t.start()
        for t in ThreadList:
            t.join()
        # s1 =  '[*] The scanning is finished'
        # s2 =  '[*] A total of %d ports is open' % (openNum)
        # s3=   '[*] Time cost :' + str((time.time() - start_time)) + ' s'
        # printc.printf(s1, "skyblue")
        # printc.printf(s2, "skyblue")
        # printc.printf(s3, "skyblue")
    #获取当前时间
    def getTime(self):
        presentTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        return presentTime
    #将输出的内容保存到一个txt文件中
    def output(self,add):
        #if add :
        # if ":" in add:
        #     address=add
        # else:
        #     address="D:\\"+str(add)
        # else:
        #     address="D:\\"+str(self.getTime())+".txt"
        # address = re.sub("(?<=\d)(:)","-",address)
        sys.stdout = Logger(add)

    #存放输出文件的文件名
    def address(self,add):
        if ":" in add:
            address=add
        else:
            address="D:\\"+str(add)
        return address
    #如果存在输入文件则打印,否则不打印    
    def printIfExist(self,address):
        if address:
            s="[*] The result file is at {add}".format(add=address)
            printc.printf(s, "skyblue")
    # #利用正则表达式匹配一些无用的信息并删除        
    # def deleteUselessInfoOfFiles(add):
    #     rule=["[*] The scanning is finished","[*] A total of \d+ hosts are open","[*] Time cost :\d+\.\d+ s"]
    #     f = open(add,"r+")
    #     for line in f.readlines():
    #         #print(line)
    #         for r in rule:
    #             stringList=re.findall(r,line)
    #             print(stringList)
    #             if stringList:
    #                 f.write(line.replace(stringList[0],""))
    #             else:
    #                 f.write(line)

class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "w+")
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        pass

#扫描包括扫描端口和扫描主机
class ScanThread(threading.Thread):
    def __init__(self, scanIP):
        threading.Thread.__init__(self)
        self.IP = scanIP
    #扫描存活端口
    def ping_ports(self, Port):
        global OpenPort, lock, Timeout,openNum
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(Timeout)
        address = (self.IP, Port)
        try:
            sock.connect(address)
        except:
            sock.close()
            return False
        sock.close()
        OpenPort.append(Port)
        if lock.acquire():
            s="[+]"+str(self.IP)+":"+str(Port)+" open"
            printc.printf(s,"green")
            openNum+=1
            lock.release()
        return True

    #扫描存活主机
    def ping_hosts(self, host,port):
        global OpenHost, lock, Timeout,openNum
        isAlive=False
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(Timeout)
        address = (host, port)
        try:
            sock.connect(address)
        except:
            sock.close()
            return False
        sock.close()
        OpenPort.append(host)
        if lock.acquire():
            isAlive=True
            lock.release()
        return isAlive

#扫描存活端口类
class ScanThreadSingle(ScanThread):
    def __init__(self, scanIP, SingleQueue):
        ScanThread.__init__(self, scanIP)
        self.SingleQueue = SingleQueue

    def run(self):
        while not self.SingleQueue.empty():
            p = self.SingleQueue.get()
            self.ping_ports(p)

#扫描存活主机类
class scanHosts(ScanThread):
    def __init__(self, scanIP, SingleQueue):
        ScanThread.__init__(self, scanIP)
        self.SingleQueue = SingleQueue
    def run(self):
        global openNum
        openedPort=''
        isAlive=False
        while not self.SingleQueue.empty():
            host = self.SingleQueue.get()
            for port in ports:
                if(self.ping_hosts(host,port)==True):
                    isAlive=True
                    openedPort=port
                    break
            if(isAlive==True):
                openNum+=1
                host=host.replace("\n",'')
                s="[+] "+str(host)+":"+str(openedPort)+" "+"存活"
                printc.printf(s,"green")
                isAlive=False


#扫描端口
def scan_host_ports(ip):
    start_time = time.time()
    global nThread, PortList
    ThreadList = []
    strIP = ip
    SingleQueue = GetQueue(PortList)
    for i in range(0, nThread):
        t = ScanThreadSingle(strIP, SingleQueue)
        ThreadList.append(t)
    for t in ThreadList:
        t.start()
    for t in ThreadList:
        t.join()
    s1 =  '[*] The scanning is finished'
    s2 =  '[*] A total of %d ports is open' % (openNum)
    s3=   '[*] Time cost :' + str((time.time() - start_time)) + ' s'
    printc.printf(s1, "skyblue")
    printc.printf(s2, "skyblue")
    printc.printf(s3, "skyblue")

#扫描特定主机
def scan_specific_hosts(ip_addr,port):
    isAlive=False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(Timeout)
    address = (ip_addr, port)
    try:
        sock.connect(address)
        isAlive=True
    except:
        sock.close()
        return False
    sock.close()
    return isAlive
#发现所有存活主机
def scan_all_hosts(ip_add):
    global openNum,nThread
    ip_add=ip_add.replace("-",".")
    ip_add=ip_add.split(".")
    l=ip_add[3]
    r=ip_add[4]
    ip_pre=str(ip_add[0])+'.'+str(ip_add[1])+'.'+str(ip_add[2])+'.'
    start_time = time.time()
    ThreadList = []
    hostLists=[]#存放扫描范围的主机
    strIP = ip_add
    for i in range(int(l),int(r)):
        hostLists.append(str(ip_pre)+str(i))
    SingleQueue = GetQueue(hostLists)
    for i in range(0, nThread):
        t = scanHosts(ip_pre, SingleQueue)
        ThreadList.append(t)
    for t in ThreadList:
        t.start()
    for t in ThreadList:
        t.join()
    s1 = '[*] The scanning is finished'
    s2 = '[*] A total of %d hosts are open' % (openNum)
    s3 = '[*] Time cost :' + str((time.time() - start_time)) + ' s'
    printc.printf(s1, "skyblue")
    printc.printf(s2, "skyblue")
    printc.printf(s3, "skyblue")

#扫描所有从文件中读取出的存活主机
def scan_all_hosts_from_file(hosts_file_add):
    try:
        global openNum,nThread,PortList
        tool=Tool()
        f=open(hosts_file_add,"rb")#从文件中读取主机
        #lines = f.readlines()#逐条读取主机
        content=str(f.read())
        hosts_content=re.findall("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+",content)
        start_time = time.time()
        ThreadList = []
        hostLists=[]#存放扫描范围的主机
        hostLists= hosts_content  #lines
        if len(PortList)>2:
            SingleQueue = GetQueue(hostLists)
            while not SingleQueue.empty():
                ip = SingleQueue.get()
                tool.scan_host_ports(ip)
        else:
            SingleQueue = GetQueue(hostLists)
            for i in range(0, nThread):
                t = scanHosts(0, SingleQueue)
                ThreadList.append(t)
            for t in ThreadList:
                t.start()
            for t in ThreadList:
                t.join()
        s1 = '[*] The scanning is finished'
        #s2 = '[*] A total of %d hosts are open' % (openNum)
        s3 = '[*] Time cost :' + str((time.time() - start_time)) + ' s'
        printc.printf(s1, "skyblue")
        #printc.printf(s2, "skyblue")
        printc.printf(s3, "skyblue")
    except:
        print("结束")


def menu():
    global nThread,ports,PortList
    tool=Tool()
    address=""
    usage = """ 
       -host To scan the open ports of the Host
       -sh  Specific Host Detective                                        Example: -sh 127.0.0.1 
       -ah  All alive Hosts Find all alive alive hosts                     Example: -ah 192.168.1.1-255
       -t   Threads(1-200) Default is 80
       -r   Read hosts file                                                Example: -r "hosts.txt"
       -p   Port ping special ports,It was used to detective alive hosts   Example: -p="80,8080,443" default was 80 443 
       -o   Output file address                                            Example: -o recoder.txt or -o D:\\recoder.txt
       -help To show help information
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', dest='host', help='-h To scan the open ports of the Host')
    parser.add_argument('-sh', dest='sh', help='Specific Host Detective                                        Example: -sh 127.0.0.1 ')
    parser.add_argument('-ah', dest='ah', help='All alive Hosts Find all alive alive hosts                     Example: -ah 192.168.1.1-255')
    parser.add_argument('-t', dest='t', help='Threads(1-200) Default is 30')
    parser.add_argument('-r', dest='r', help='Read hosts file                                                Example: -r "hosts.txt"')
    parser.add_argument('-p', dest='p', help='Port ping special ports,It was used to detective alive hosts   Example: -p="80,8080,443" default was 80 443')
    parser.add_argument('-o', dest='o', help='Output file address                                            Example: -o recoder.txt or -o D:\\recoder.txt')
    parser.add_argument('-help', action="store_true", help='To show help information')
    options = parser.parse_args()
    #如果用户输入了线程数,改变线程数
    #if options.t:
        #tool.nThreads(options.t)
    if options.host:
        #address=tool.address(options.o)
        if options.o:
            address=tool.address(options.o)   
            tool.output(address)
        # add=""
        # tool.output(add)
        if options.t:
            tool.nThreads(options.t)
        if options.p:
            PortList=tool.changeList(tool.split2List(options.p))
            msg1=msg2=''
            for i in PortList:
                msg1+=str(i)+' '
            msg2="[*] Scanning Ports :"+msg1
            printc.printf(msg2,"skyblue")
        s = options.host
        scan_host_ports(s)
        tool.printIfExist(address)
    elif options.ah :
        if options.o:
            address=tool.address(options.o)   
            tool.output(address)
        if options.t:
            tool.nThreads(options.t)
        if options.p:
            ports = tool.changeList(tool.split2List(options.p))
            msg1 = msg2 = ''
            for i in ports:
                msg1 += str(i) + ' '
            msg2 = "[*] Scanning Ports :" + msg1
            printc.printf(msg2, "skyblue")
        ip_addr = options.ah
        scan_all_hosts(str(ip_addr))
        tool.printIfExist(address)
    elif options.r:
        if options.o:
            address=tool.address(options.o)   
            tool.output(address)
        if options.t:
            tool.nThreads(options.t)
        if options.p:
            PortList = tool.changeList(tool.split2List(options.p))
            ports = tool.changeList(tool.split2List(options.p))
            msg1 = msg2 = ''
            for i in PortList:
                msg1 += str(i) + ' '
            msg2 = "[*] Scanning Ports :" + msg1
            printc.printf(msg2, "skyblue")
        file_add=options.r
        scan_all_hosts_from_file(file_add)
        tool.printIfExist(address)
    elif options.sh:
        if options.p:
            ports = tool.changeList(tool.split2List(options.p))
            msg1 = msg2 = ''
            for i in ports:
                msg1 += str(i) + ' '
            msg2 = "[*] Scanning Ports :" + msg1
            printc.printf(msg2, "skyblue")
        flag = False
        ip_addr = options.sh
        for port in ports:
            if (scan_specific_hosts(ip_addr, port) == True):
                flag = True
                break
        if flag == True:
            s1 = "[+] " + str(ip_addr) + "存活"
            printc.printf(s1, "green")
        else:
            s1 = "[+] " + str(ip_addr) + "关闭"
            printc.printf(s1, "darkred")
    # 如果用户没有输入线程数则按默认nThreas=80来执行
    #if not options.t:
        # if options.host:
        #     s = options.host
        #     scan_host_ports(s)
        # if options.ah:
        #     ip_addr = options.ah
        #     scan_all_hosts(str(ip_addr))
        # elif options.r:
        #     file_add=options.r
        #     scan_all_hosts_from_file(file_add)
        # if options.sh:
        #     flag = False
        #     ip_addr = options.sh
        #     for port in ports:
        #         if (scan_specific_hosts(ip_addr, port) == True):
        #             flag = True
        #             break
        #     if flag == True:
        #         s1 = "[+] " + str(ip_addr) + "存活"
        #         printc.printf(s1, "green")
        #     else:
        #         s1 = "[+] " + str(ip_addr) + "关闭"
        #         printc.printf(s1, "darkred")
    if options.help:
              helpInfo()

def helpInfo():
    helpInformaiton = """Usage:
       -host To scan the open ports of the Host
       -sh  Specific Host Detective                                        Example: -sh 127.0.0.1 
       -ah  All alive Hosts Find all alive alive hosts                     Example: -ah 192.168.1.1-255
       -t   Threads(1-200) Default is 80
       -r   Read hosts file                                                Example: -r "hosts.txt"
       -p   Port ping special ports,It was used to detective alive hosts   Example: -p="80,8080,443" default was 80 443 
       -o   Output file address                                            Example: -o recoder.txt or -o D:\\recoder.txt
       -help To show help information
        """
    printc.printf(helpInformaiton,"blue")

if __name__=='__main__':
    menu()
