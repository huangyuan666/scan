import socket,os,threading,queue,time,re
from module import printc
try:
    import requests
except:
    msg1="\n[-] 检测到您还没有安装Python3的requests依赖包,请使用 pip install requests 安装\n"
    printc.printf(msg1,'red')
#线程锁        
lock = threading.Lock()
count  = 0  #计数

def test():
    printc.printf("124","red")

#得到一个队列
def GetQueue(list):
    PortQueue = queue.Queue(65535)
    for p in list:
        PortQueue.put(p)
    return PortQueue

#导入需要的依赖包,如果用户没有安装则提示用户安装
def importModules():
    try:
        import json
    except:
        msg1="\n[-] 检测到您还没有安装Python3的json依赖包,请使用 pip install json 安装\n"
        printc.printf(msg1,'red')
    try:
        import requests
    except:
        msg1="\n[-] 检测到您还没有安装Python3的requests依赖包,请使用 pip install requests 安装\n"
        printc.printf(msg1,'red')

#通过域名获取ip
def getIPByName(host):
    try:
        return socket.gethostbyname(host)
    except:
        return 0
        pass

#读取文件每一行并将文件内容存放在列表中
def content2List(add):
    # cwd=os.getcwd()
    dirList=[]
    # add=cwd+"\\dict\\directory.txt"
    f=open(add,"rb")
    for line in f.readlines():
        dirList.append(str(line)[2:-5])
    return dirList

#判断是否访问的页面是否存在
def ifExist(res):
    symbol=["404","NOT FOUND","对不起"]
    p="<title>([\W\w]*?)</title>"
    for i in symbol:
        if i in re.findall(p,res)[0]:
            return False
            break
        else:
            return True
#bytes 转化为str
def bytes2str(input):
    if type(input)=="bytes":
        input=bytes.decode(input)
    return input
#删除文件中无用且重复的信息            
def delUseless(add):
    try:
        s=[]
        f=open(add,"r+")
        for i in f.readlines():
            i=i.replace("\n","") 
            s.append(i)
        f.close()
        s=list(set(s))
        with open(add,"w+") as f:
            for i in s:
                f.write(i+"\n")
            f.close()
    except:
        msg1="[-] 是不是路径输错了呢?"
        printc.printf(msg1,"red")
#将爬取的res转化为标准res.text的格式
def change2standard(res):
    try:
        if res.encoding=="ISO-8859-1":
            # res.encoding="utf-8
            result=res.text.encode(res.encoding).decode('GBK')
            #result=res.text.decode(res.encoding).encode("utf8")
        else:
            result=res.text
        return bytes2str(result)
    except:
        if res.encoding=="ISO-8859-1":
            # res.encoding="utf-8
            #result=res.text.decode(res.encoding).encode("gbk")
            result=res.text.encode(res.encoding).decode('utf8')
        else:
            result=res.text
        return bytes2str(result)


#获取子域名类
class getSubdomainNames(threading.Thread):
    def __init__(self,subdomains,domain,protocol):
        threading.Thread.__init__(self)
        self.subdomains=subdomains
        self.domain=domain
        self.protocol=protocol
        self.p="<title>([\W\w]*?)</title>"
        self.p1="<TITLE>([\W\w]*?)</TITLE>"
    def run(self):
        global lock,count
        domain=self.domain
        while not self.subdomains.empty():
            subdomain=self.subdomains.get()
            # domain=httpOrHttps(domain)+"://" +subdomain+"."+domain
            domain=httpOrHttps(self.protocol)+"://" +subdomain+"."+domain
            # print(domain)
            #lock.acquire()
            try: 
                res=requests.get(domain,timeout=2)
                result=change2standard(res)
                # print(result)
                # if ifExist(res)==True:
                if (re.findall(self.p,result)):
                    title=(re.findall(self.p,result)[0])
                elif re.findall(self.p1,result):
                    title=(re.findall(self.p1,result)[0])
                else:
                    title=' '
                title=title.replace("\n","")
                title=title.replace("\r","")
                title=title.replace("\t","")
                title=title.replace(" ",'')
                count=count+1
                msg1="[+] "+domain+"   "+title
                printc.printf(msg1,'green')
            except:
                # msg2=domain+"不可访问"
                # printc.printf(msg2,'red')
                pass
            #lock.release()
#根据不同的类型选择不同的字典 1 subnames_school 2 subnames_gov 3 subnames_company 0 default subnames ,当然也支持用户自定义字典
def dicJudgeByInput(Input):
    if Input==0:
        return os.getcwd().replace("module","dict\subnames.txt")
    elif Input==1:
        return os.getcwd()+"\dict\subnames_school.txt"
    elif Input==2:
        return os.getcwd().replace("module","dict\subnames_gov.txt")
    elif Input==3:
        return os.getcwd().replace("module","dict\subnames_company.txt")
    else:
        return Input 
#判断网站使用的是http或者https
def httpOrHttps(protocol):
    if protocol=="https":
        protocol="https"
    else:
        protocol="http"
        return protocol

#将字符串设定为统一长度
def setStr2SameLen(length,string):
    if length>len(string):
        length=length-len(string)
        for i in range(length):
            string=string+' '
        return string
    else:
        return string
#获取子域名
def getSubdomainName(nThreads,Num,domain,protocol):
    global count
    start_time=time.time()
    add=dicJudgeByInput(Num)
    subdomains=GetQueue(content2List(add))
    ThreadList=[]
    for i in range(0, nThreads):
        t = getSubdomainNames(subdomains,domain,protocol)
        ThreadList.append(t)
    for t in ThreadList:
        t.start()
    for t in ThreadList:
        t.join()
    msg1="[+] Time cost:"+str(time.time()-start_time)+" s"
    msg2="[+] {count} Subdomains have been found".format(count=count)
    printc.printf(msg1,"green")
    printc.printf(msg2,"green")
if __name__=='__main__':
    getSubdomainName(300,1,"ncu.edu.cn","http")
    #bingRequests("site:ncu.edu.cn")
    #delUseless("D:\\Github\\scan\\dict\\subnames_school.txt")

