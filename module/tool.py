import socket
from module import printc

def test():
    printc.printf("124","red")

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
    return socket.gethostbyname(host)