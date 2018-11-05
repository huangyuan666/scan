class Tool():
    global ports,PortList,response

    def GetQueue(list):
        PortQueue = queue.Queue(65535)
        for p in list:
            PortQueue.put(p)
        return PortQueue
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
    #判断向相应的结果编码是否是utf-8如果不是将其转化为utf-8
    def set2utf8cont(self,res):
        if res.encoding=="utf-8":
            content=str(res.text)
            return content
        else:
            res.encoding="utf-8"
            return str(res.text)
    #根据响应的结果判断是否可以访问
    def visible(self,res):
        content=self.set2utf8cont(res)
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
        p1="^[htps:/]+[.\w-]+\.[a-z]+" #匹配标准的https://www.baidu.com格式
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

    #将list打印出来
    def printList(self,list,color):
        for i in list:
            printc.printf(i,color)