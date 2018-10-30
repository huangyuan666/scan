﻿﻿中文说明:
========
## 更新说明:
   1. 新增全局 -o 参数,您可以保存存任意输出的结果
   2. 改变 -r 参数功能使其既可以采用默认方式扫描全部开放端口,也可以扫描特定的端口开放情况
   3. 新增正则表达式,意味着您在让程序读取文件时不用对文件做任何处理(即便里面有中文或者其他无用信息),程序会自动筛选有效信息
   4. 新增全局 -p 参数,用户可以自己设定扫描端口
   5. 改变之前的线程设置策略,线程设置由原来的1-100(默认30)改变为1-200(默认80)扫描速度更快
   6. 改善规则,改变之前只能输入标准主机的限定如: -host www.target.com 现在您只需要输入 -host target.com 亦或是 http://www.target.cn/xxgkw/xxfbh/201205/t20120517_155695.htm  亦或是其他格式程序都能识别

这是一款基于python3的小巧的扫描工具

我已经将需要的模块封装好了,只需要下载即可使用

您只需要输入python scan.py就可以并且得到如下结果:	
Usage:

       -host To scan the open ports of the Host
       -sh  Specific Host Detective                                        Example: -sh 127.0.0.1
       -ah  All alive Hosts Find all alive alive hosts                     Example: -ah 192.168.1.1-255
       -t   Threads(1-200) Default is 80
       -r   Read hosts file                                                Example: -r "hosts.txt"
       -p   Port ping special ports,It was used to detective alive hosts   Example: -p="80,8080,443" default was 80 443
       -o   Output file address                                            Example: -o recoder.txt or -o D:\recoder.txt
       -help To show help information



优     点:小巧,方便,强大

 1. 扫描特定账主机的端口信息 python scan.py -host 127.0.0.1
    ![](https://raw.githubusercontent.com/spacesec/images/master/scan/scanHost.png) 
    
 2. 扫描一定范围内的存活主机  python scan.py -ah 10.86.65.1-255
    ![](https://raw.githubusercontent.com/spacesec/images/master/scan/scanAlive.png)
	
 3. 扫描特定主机存活状态 scan.py -sh 127.0.0.1
    ![](https://raw.githubusercontent.com/spacesec/images/master/scan/scanSpecificHost.png)
 
 4. 从文件中读取主机并扫描特定端口存活状态 python scan.py -r C:\Users\Ma\Desktop\Desk\info.txt -p 80 -t 200
    ![扫描特定端口存活状态](https://raw.githubusercontent.com/spacesec/images/master/scan/5.png)

 5. 从文件中读取主机并扫描全部端口存活状态 python scan.py -r "C:\Users\Ma\Desktop\1.txt" -t 200
    ![扫描全部端口存活状态](https://raw.githubusercontent.com/spacesec/images/master/scan/6.png)

 6. 扫描一定范围内的存活主机并且保存至特定的输入出文件中  python scan.py -ah 10.86.65.1-255 -t 200 -p 80 -o result.txt
    ![扫描结果并保存](https://raw.githubusercontent.com/spacesec/images/master/scan/1.png)
    ![生成的txt文件](https://raw.githubusercontent.com/spacesec/images/master/scan/2.png)
 
 7. 您可以输入任意有效的url程序会自动识别主机
    python scan.py -host "https://tieba.baidu.com/index.html"
    python scan.py -host "www.baidu.com"
    python scan.py -host "baidu.com"
    python scan.py -host "127.0.0.1"
![自动识别主机](https://raw.githubusercontent.com/spacesec/images/master/scan/7.png)

 

******************************************************************************
分割线 分割线	分割线	分割线	分割线	分割线	分割线
******************************************************************************
English introduction:
=========
This is an powerful scanner based on python

What you need to do is just download it and use it because have packaged all third-part modules

What you need to do is just type python scan.py and then you can get the result as follows
 Usage:
       
       -host To scan the open ports of the Host
       -sh  Specific Host Detective                                        Example: -sh 127.0.0.1
       -ah  All alive Hosts Find all alive alive hosts                     Example: -ah 192.168.1.1-255
       -t   Threads(1-200) Default is 80
       -r   Read hosts file                                                Example: -r "hosts.txt"
       -p   Port ping special ports,It was used to detective alive hosts   Example: -p="80,8080,443" default was 80 443
       -o   Output file address                                            Example: -o recoder.txt or -o D:\recoder.txt
       -help To show help information


Advantage:small but powerful 

1. Scan a specific Host's opened ports information '''python   python scan.py -host 127.0.0.1 '''
![](https://raw.githubusercontent.com/spacesec/images/master/scan/scanHost.png) 

2. Scan to get all alive hosts in a range  python scan.py -ah 10.86.65.1-255
![](https://raw.githubusercontent.com/spacesec/images/master/scan/scanAlive.png)

3. Scan a specific host python scan.py 127.0.0.1 
![](https://raw.githubusercontent.com/spacesec/images/master/scan/scanSpecificHost.png)

4. Scan the special port of hosts from a txt file python scan.py -r C:\Users\Ma\Desktop\Desk\info.txt -p 80 -t 200
  ![扫描特定端口存活状态](https://raw.githubusercontent.com/spacesec/images/master/scan/5.png)

5. Scan all ports info of the hosts in a txt file python scan.py -r "C:\Users\Ma\Desktop\1.txt" -t 200
  ![扫描全部端口存活状态](https://raw.githubusercontent.com/spacesec/images/master/scan/6.png)

6. Scan a range  of surviving hosts and save the result  python scan.py -ah 10.86.65.1-255 -t 200 -p 80 -o result.txt
  ![扫描结果并保存](https://raw.githubusercontent.com/spacesec/images/master/scan/1.png)
  ![生成的txt文件](https://raw.githubusercontent.com/spacesec/images/master/scan/2.png)

 7. Type any urls or ip
    python scan.py -host "https://tieba.baidu.com/index.html"
    python scan.py -host "www.baidu.com"
    python scan.py -host "baidu.com"
    python scan.py -host "127.0.0.1"
![自动识别主机](https://raw.githubusercontent.com/spacesec/images/master/scan/7.png)