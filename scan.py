# -- coding: utf-8 --
import threading, socket,time,os,re,sys,string
from module import printc,butianInfo,queue,argparse
# from module import queue
# from module import argparse
try:
    import requests
except:
    msg1="[-] 检测到您还没有安装Python3的requests依赖包,请使用 pip install requests安装"
    printc.printf(msg1,'red')
try:
    import json
except:
    msg1="[-] 检测到您还没有安装Python3的json依赖包,请使用 pip install json安装"
    printc.printf(msg1,'red')
#扫描常用端口
PortList=[21,22,23,25,31,42,53,67,68,69,79,80,81,85,99,102,109,135,137,138,139,143,161,389,443,445,456,
513,554,593,635,636,646,873,902,903,912,913,993,1000,1001,1029,1011,1024,1043,1044,1080,1170,1234,1245,1433,1502,1536,
1537,1538,1539,1540,1542,1543,1544,1547,1548,1549,1801,1935,2066,2500,2504,2601,2602,2604,2869,3306,3389,3443,4000,4444,
4224,4444,4900,5040,5357,6000,6942,7680,7702,7720,7739,7777,7778,7779,7780,7807,7831,7833,8080,8085,8088,8888,8307,8443,8800,9015,9075,9081,9086,
9087,9095,9144,9156,9666,9999,12051,13223,14367,14601,14610,14611,14612,14613,14614,14615,14616,14617,14618,14619,14620,14621,21440,21441,28317,35432,62078,63342,65000]
#判断主机是否存活的端口
ports=[80,443]
#后台不能访问的标志'404','NOT FOUND','护卫神','WAF','管理员','Forbidden','很抱歉',
cantFlag=["WAF","页面不存在","404",'管理员','Forbidden','很抱歉',"服务器内部错误","服务器错误","您要查找的资源可能已被删除，已更改名称或者暂时不可用。","无法访问"]
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
flag = 1
#全局队列
Queue=''
#得到一个队列
response=''
def GetQueue(list):
    PortQueue = queue.Queue(65535)
    for p in list:
        PortQueue.put(p)
    return PortQueue
#这是一个工具类,里面放着一些常见的工具函数

class Tool():
    global ports,PortList,response
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
    #获取当前时间
    def getTime(self):
        presentTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        return presentTime
    #将输出的内容保存到一个txt文件中
    def output(self,add):
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
    #判断是否字符串中是否含有数字
    def hasNum(self,inputString):
        return any(char.isdigit() for char in inputString)

    #由于https://www.test.con http://baidu.com 使用程序是无法是别的,只有www.target.com这种才能被识别
    #所以需要将一些非标准的转化为标准的形如www.target.com这样的,ip地址也要转化为(/d+.)+\d类型的
    def standardUrl(self,url):
        pattern="([hwtps:/]{3,}[.\w-]+\.[a-z]+)"
        ip_pattern="[\d+\.]+\d+"
        host=url
        flag = True 
        # if self.hasNum(host) ==True:
        #     flag=False
        if re.findall(ip_pattern,url):
            return re.findall(ip_pattern,url)[0]
        else:
        # if flag == True:   
            if re.search(pattern,url):
                host=re.search(pattern,url)[1]
            for i in ["https://","http://"]:
                host=host.replace(i,"")
            if "www." not in host:
                host="www."+host
            return host
    #因为像将ip或者url输出位标准的    
    #读取文件每一行并将文件内容存放在列表中
    def content2List(self,add):
        # cwd=os.getcwd()
        dirList=[]
        # add=cwd+"\\dict\\directory.txt"
        f=open(add,"rb")
        for line in f.readlines():
            dirList.append(str(line)[2:-5])
        return dirList
    #根据响应的结果判断是否可以访问
    def visible(self,res):
        if res.encoding=="utf-8":
            content=str(res.text)
        else:
            res.encoding="utf-8"
            content=str(res.text)
        if content==response:
            return False
        else:
            flag=True
            global cantFlag
            if res.status_code ==200:
                if res.is_redirect==False:
                    for i in cantFlag:
                        if  i  in content:
                            flag=False
                    return flag
                else:
                    return False
            else:
                return False
    #判断用户输入是否是标准的http://127.0.0.1 或者https://www.baidu.com
    def isStandard(self,inputString):
        p1="([htps:/]+[.\w-]+\.[a-z]+)" #匹配标准的https://www.baidu.com格式
        p2="[htps.:/]+(\d+\.){3}\d"  #匹配形如http://127.0.0.1格式
        res1=re.findall(p1,inputString)
        res2=re.findall(p2,inputString)
        if res1 or res2:
            return True
        else:
            return False
    #由于https和http响应结果的不同,所以要对其进行分类     
    def Requests(self,url):
        try:
            requests.packages.urllib3.disable_warnings()
            if "https" in str(url):
                return requests.get(url,verify=False)
            else:
                return requests.get(url)
        except:
            pass



class Logger(object):
    def __init__(self, fileN="Default.log"):
        try:
            self.terminal = sys.stdout
            self.log = open(fileN, "w+")
        except:
            print("保存路径换到D盘试试")
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
        global openNum,lock
        openedPort=''
        isAlive=False
        try:
            #lock.acquire()
            while not self.SingleQueue.empty():
                host = self.SingleQueue.get()
                for port in ports:
                    if(self.ping_hosts(host,port)==True):
                        isAlive=True
                        openedPort=port
                        #lock.release()
                        break
                lock.acquire()
                if(isAlive==True):
                    openNum+=1
                    host=host.replace("\n",'')
                    s="[+] "+str(host)+":"+str(openedPort)+" "+"存活"
                    printc.printf(s,"green")
                    isAlive=False
                    lock.release()
                else:
                    lock.release()
        except:
            pass
            
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

#扫描web可访问的后台文件目录       
class ScanBackDirectory(threading.Thread):
    def __init__(self,host):
        threading.Thread.__init__(self)
        self.host=host
    def run(self):
        global Queue,lock
        tool=Tool()
        while not Queue.empty():
            try:
                url=self.host+"/"+str(Queue.get())
                res=tool.Requests(url)
                lock.acquire()
                try:
                    if tool.visible(res) == True:
                        s1="[+]:"+url+" 存在"
                        printc.printf(s1,"green")
                        # print(threading.get_ident())#线程ID
                        lock.release()
                    #     break
                    else:
                        s2 = "[-]:" + url + " 不存在"
                        printc.printf(s2, "red")
                        # print(threading.get_ident())#线程ID
                        lock.release()
                except:
                      pass
            except:
                msg1="[-]:连接中断正在重试中..."
                printc.printf(msg1,'red')
                pass


#扫描后台可访问的目录
def scanDir(host,add):
    #try:
    global nThread,flag,Queue
    start_time=time.time()
    tool=Tool()
    dirlists=ThreadList=[]
    #dirlists=tool.content2List("D:\Github\scan\dict\directory.txt")
    dirlists=tool.content2List(add)
    # print(str(dirlists))
    Queue = GetQueue(dirlists)  
    for i in range(0, nThread):
        t = ScanBackDirectory(host)
        ThreadList.append(t)
    for t in ThreadList:
        t.start()
    for t in ThreadList:
        t.join()
    s1 = '[*] The scanning is finished'
    s2 = '[*] Time cost :' + str((time.time() - start_time)) + ' s'
    printc.printf(s1, "skyblue")
    printc.printf(s2, "skyblue")
    # except:
    #     pass

def menu():
    global nThread,ports,PortList,response
    tool=Tool()
    address=""
    usage = """ 
       -host   To scan the open ports of the Host
       -sh     Specific Host Detective                                        Example: -sh 127.0.0.1 
       -ah     All alive Hosts .Find all alive hosts                          Example: -ah 192.168.1.1-255
       -t      Threads(1-200) Default is 80
       -r      Read hosts file                                                Example: -r "hosts.txt"
       -p      Port. Ping special ports,It was used to detective alive hosts  Example: -p="80,8080,443" default was 80 443 
       -o      Output file address                                            Example: -o recoder.txt or -o D:\\recoder.txt
       -dir    Scanning visible background directory                          Example: -dir http://127.0.0.1
       -add    Dictionary File Address                                        Example: -dir http://127.0.0.1  -add C:\dic.txt
       -url    Butian SRC list url                                            Example: -url https://butian.360.cn/Home/Active/company -page 10
       -page   Butian SRC Pages      Default is 10                            Example: -url https://butian.360.cn/Home/Active/company -page 10
       -help To show help information
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', dest='host', help='-h To scan the open ports of the Host')
    parser.add_argument('-sh', dest='sh', help='Specific Host Detective                                        Example: -sh 127.0.0.1 ')
    parser.add_argument('-ah', dest='ah', help='All alive Hosts .Find all alive hosts                          Example: -ah 192.168.1.1-255')
    parser.add_argument('-t', dest='t', help='Threads(1-200) Default is 80')
    parser.add_argument('-r', dest='r', help='Read hosts file                                                  Example: -r "hosts.txt"')
    parser.add_argument('-p', dest='p', help='Port.Ping special ports,It was used to detective alive hosts     Example: -p="80,8080,443" default was 80 443')
    parser.add_argument('-o', dest='o', help='Output file address                                              Example: -o recoder.txt or -o D:\\recoder.txt')
    parser.add_argument('-dir', dest='dir', help='Scanning visible background directory                        Example: -dir http://127.0.0.1' )
    parser.add_argument('-add', dest='add', help='Dictionary File Address                                      Example: -dir http://127.0.0.1  -add C:\dic.txt' )
    parser.add_argument('-url', dest='url', help='Butian SRC list url                                          Example: -url https://butian.360.cn/Home/Active/company' )
    parser.add_argument('-page', dest='page', help='Butian SRC Pages      Default is 10                        Example: -url https://butian.360.cn/Home/Active/company' )
    parser.add_argument('-help', action="store_true", help='To show help information')
    options = parser.parse_args()
    if options.host:
        if options.o:
            address=tool.address(options.o)   
            tool.output(address)
        if options.t:
            tool.nThreads(options.t)
        if options.p:
            PortList=tool.changeList(tool.split2List(options.p))
            msg1=msg2=''
            for i in PortList:
                msg1+=str(i)+' '
            msg2="[*] Scanning Ports :"+msg1
            printc.printf(msg2,"skyblue")
        s = tool.standardUrl(options.host)
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
    elif options.dir:
        if options.o:
            address=tool.address(options.o)   
            tool.output(address)
        if options.t:
            tool.nThreads(options.t)

        host=options.dir
        if  tool.isStandard(host) ==True:
            res=tool.Requests(host)
            res.encoding="utf-8"
            response=res.text
            #dirList=tool.content2List()
            if options.add:
                add=options.add
            else:
                add=str(os.getcwd())+"\\dict\\directory.txt"
            scanDir(host,add)
            tool.printIfExist(address)
        else:        
         printc.printf("\n[-] 请在您输入的地址前面添加http或者https。http://127.0.0.1 或者 https://www.baidu.com 格式的地址",'yellow')
    elif options.url:
        url=options.url
        if options.o:
            address=tool.address(options.o)   
            tool.output(address)
        if options.page:
            page=options.page
        else:
            # url="https://butian.360.cn/Home/Active/company"
            # page=10
            page=10
        butianInfo.get_src_name(url,page)
        tool.printIfExist(address)
    
    if options.help:
              helpInfo()

def helpInfo():
    helpInformaiton = """Usage:
       -host   To scan the open ports of the Host
       -sh     Specific Host Detective                                        Example: -sh 127.0.0.1 
       -ah     All alive Hosts .Find all alive hosts                          Example: -ah 192.168.1.1-255
       -t      Threads(1-200) Default is 80
       -r      Read hosts file                                                Example: -r "hosts.txt"
       -p      Port. Ping special ports,It was used to detective alive hosts  Example: -p="80,8080,443" default was 80 443 
       -o      Output file address                                            Example: -o recoder.txt or -o D:\\recoder.txt
       -dir    Scanning visible background directory                          Example: -dir http://127.0.0.1
       -add    Dictionary File Address                                        Example: -dir http://127.0.0.1  -add C:\dic.txt
       -url    Butian SRC list url                                            Example: -url https://butian.360.cn/Home/Active/company -page 10
       -page   Butian SRC Pages      Default is 10                            Example: -url https://butian.360.cn/Home/Active/company -page 10
       -help To show help information
        """
    printc.printf(helpInformaiton,"yellow")

if __name__=='__main__':
    menu()
