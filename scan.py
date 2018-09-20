# -- coding: utf-8 --
import threading, socket,time,os,queue
from module import printc
from module import queue
from module import argparse

#扫描常用端口
PortList=[21,22,23,25,31,42,53,67,68,69,79,80,99,102,109,135,137,138,139,143,161,389,443,445,456,513,554,635,636,902,903,912,913,993,1001,1029,1011,1024,1043,1080,1170,1234,1245,1433,1502,1536,1537,1538,1539,1540,1542,1543,1544,1547,1548,1549,1801,2500,2504,2869,3306,3389,3443,4444,5040,5357,6000,6942,7680,7702,7720,7739,7777,7778,7779,7780,7807,7831,7833,8080,8888,8307,8800,9015,9075,9081,9086,9087,9095,9144,9156,12051,13223,14367,14601,14610,14611,14612,14613,14614,14615,14616,14617,14618,14619,14620,14621,21440,21441,28317,35432,62078,63342,65000]
#判断主机是否存活的端口
ports=[135,80,139,443,445,62078]
#单IP扫描线程个数
nThread = 30
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
        isAlive=False
        while not self.SingleQueue.empty():
            host = self.SingleQueue.get()
            for port in ports:
                if(self.ping_hosts(host,port)==True):
                    isAlive=True
                    break
            if(isAlive==True):
                openNum+=1
                s="[+] "+str(host)+":"+"存活"
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
    global openNum
    ip_add=ip_add.replace("-",".")
    ip_add=ip_add.split(".")
    l=ip_add[3]
    r=ip_add[4]
    ip_pre=str(ip_add[0])+'.'+str(ip_add[1])+'.'+str(ip_add[2])+'.'
    start_time = time.time()
    global nThread
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
    s2 = '[*] A total of %d hosts is open' % (openNum)
    s3 = '[*] Time cost :' + str((time.time() - start_time)) + ' s'
    printc.printf(s1, "skyblue")
    printc.printf(s2, "skyblue")
    printc.printf(s3, "skyblue")

def menu():
    usage = """ 
       -host To scan the open ports of the Host
       -sh  Specific Host Detective                                        Example: -sh 127.0.0.1 
       -ah  All alive Hosts Find all alive alive hosts                     Example: -ah 192.168.1.1-255
       --h To show help information
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', dest='host', help='-h To scan the open ports of the Host')
    parser.add_argument('-ah', dest='ah', help='Specific Host Detective                                        Example: -sh 127.0.0.1 ')
    parser.add_argument('-sh', dest='sh', help='All alive Hosts Find all alive alive hosts                     Example: -ah 192.168.1.1-255')
    parser.add_argument('--h', action="store_true", help='To show help information')
    options = parser.parse_args()

    if options.host:
        s = options.host
        scan_host_ports(s)

    elif options.sh:
        global ports
        flag=False
        ip_addr = options.sh
        for port in ports:
            if(scan_specific_hosts(ip_addr,port)==True):
                flag=True
                break
        if flag==True:
            s1="[+] "+str(ip_addr)+"存活"
            printc.printf(s1,"green")
        else:    
            s1 = "[+] " + str(ip_addr) + "关闭"
            printc.printf(s1, "darkred")


    elif options.ah:
        ip_addr = options.ah
        scan_all_hosts(str(ip_addr))
    else:
        helpInfo()

def helpInfo():
    helpInformaiton = """Usage:
       -host To scan the open ports of the Host
       -sh  Specific Host Detective                                        Example: -sh 127.0.0.1 
       -ah  All alive Hosts Find all alive alive hosts                     Example: -ah 192.168.1.1-255
       --h To show help information
        """
    print(helpInformaiton)

if __name__=='__main__':
    # scan_all_hosts("10.1.89.1-255")
    # scan_host_ports("127.0.0.1")
    # s=scan_specific_hosts("192.168.31.206",135)
    # print(s)
    menu()
