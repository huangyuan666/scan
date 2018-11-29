﻿﻿中文说明:
========
## 注意
   因为精力和时间有限,现在只适配了windows上Python3环境,而且我在别人的电脑上是可以正常运行的,一些必要的依赖包我已经封装好了,所以正常情况下在windwos上python3运行是不会有问题的

   如果实在解决不了:
   QQ:1058763824


## 更新说明:
   1. 新增-dir参数 扫描后台文件和目录,
   2. 新增-add参数,用户既可以使用自己的字典也可以使用默认字典
   3. 新增线程锁解决输出颜色不一致的问题
   4. 新增全局 -o 参数,您可以保存存任意输出的结果
   5. 改变 -r 参数功能使其既可以采用默认方式扫描全部开放端口,也可以扫描特定的端口开放情况
   6. 新增正则表达式,意味着您在让程序读取文件时不用对文件做任何处理(即便里面有中文或者其他无用信息),程序会自动筛选有效信息
   7. 新增全局 -p 参数,用户可以自己设定扫描端口,也可以扫描一定范围内的扫描
   8. 改变之前的线程设置策略,线程设置由原来的1-100(默认30)改变为1-200(默认80)扫描速度更快
   9. 改善规则,改变之前只能输入标准主机的限定如: -host www.target.com 现在您只需要输入 -host target.com 亦或是 http://www.target.cn/xxgkw/xxfbh/201205/t20120517_155695.htm  亦或是其他格式程序都能识别
   10. 新增扫描后台目录的功能  -dir  http://127.0.0.1 或者  -dir https://www.baidu.com/dire/
   11. 新增-url 和-page参数,自动化获取补天公益SRC厂商名单并且可保存生成txt文件
   12. 新增ip显示,例如您输入python scan.py -host http://www.baidu.com/ 程序会自动打印主机的ip地址方便您进一步操作
   13. 程序将变得模块化,例如以后的功能函数会写在modules目录下的文件里面,如tool.py里面放的全部是功能函数,功能函数的代码不会在出现在scan.py主文件里面。
   14. 新增-types子域名扫描,支持三种类型扫描 1学校 2公司 3政府类网站,如果不指定类型也可以扫描但是扫描会很慢

这是一款基于python3的小巧的扫描工具

我已经将需要的模块封装好了,只需要下载即可使用

您只需要输入python scan.py -help就可以并且得到如下结果:  

      Usage:
        -host   To scan the open ports of the Host                             Default scanning ports are most usual ports
       -sh     Specific Host Detective                                        Example: -sh 127.0.0.1
       -ah     All alive Hosts .Find all alive hosts                          Example: -ah 192.168.1.1-255 Default ports is 80 443
       -t      Threads(1-200) Default is 80
       -r      Read hosts file                                                Example: -r "hosts.txt"
       -p      Ports                                                          Example: -p="80,8080,443" or -p 1-255 default are most usual ports
       -o      Output file address                                            Example: -o recoder.txt or -o D:\recoder.txt
       -dir    Scanning visible background directory                          Example: -dir http://127.0.0.1
       -add    Dictionary File Address                                        Example: -dir http://127.0.0.1  -add C:\dic.txt
       -sdn    Subdomain names                                                Example: -sdn baidu.com -types 3  -sdn pku.edu.cn -types 1
       -pro    Protocol                                                       Example: -pro https    Default Protocol is http
       -types  Using different dictionary txt file                            1 2 3 means school gov company website,it can makes the result more reliable
       -url    Butian SRC list url                                            Example: -url https://butian.360.cn/Home/Active/company -page 10
       -page   Butian SRC Pages      Default is 10                            Example: -url https://butian.360.cn/Home/Active/company -page 10
       -help To show help information


优     点:小巧,方便,强大

 1. 扫描特定账主机的端口信息 python scan.py -host 127.0.0.1
    ![](https://raw.githubusercontent.com/spacesec/images/master/scan/scanHost.png) 
    
 2. 扫描一定范围内的存活主机  python scan.py -ah 123.125.115.1-255 -t 200
    ![](https://raw.githubusercontent.com/spacesec/images/master/scan/8.png)
	
 3. 扫描特定主机存活状态 scan.py -sh 127.0.0.1
    ![](https://raw.githubusercontent.com/spacesec/images/master/scan/scanSpecificHost.png)
 
 4. 从文件中读取主机并扫描特定端口存活状态 python scan.py -r D:\info.txt -t 200 -p 80
    ![扫描特定端口存活状态](https://raw.githubusercontent.com/spacesec/images/master/scan/5.png)

 5. 从文件中读取主机并扫描全部端口存活状态 python scan.py -r D:\info.txt -t 200
    ![扫描全部端口存活状态](https://raw.githubusercontent.com/spacesec/images/master/scan/6.png)

 6. 扫描一定范围内的存活主机并且保存至特定的输入出文件中   python scan.py -ah 123.125.115.1-255 -t 200 -o info.txt
    ![扫描结果并保存](https://raw.githubusercontent.com/spacesec/images/master/scan/1.png)
    ![生成的txt文件](https://raw.githubusercontent.com/spacesec/images/master/scan/2.png)
 
 7. 您可以输入任意有效的url程序会自动识别主机
    python scan.py -host "https://tieba.baidu.com/index.html"  
    python scan.py -host "www.baidu.com"  
    python scan.py -host "baidu.com"  
    python scan.py -host "127.0.0.1"
![自动识别主机](https://raw.githubusercontent.com/spacesec/images/master/scan/7.png)
 
 8. 扫描web后台可以访问的目录和文件[默认字典]  
    python scan.py -dir http://127.0.0.1 -t 200
    ![扫描后台可访问目录默认字典](https://raw.githubusercontent.com/spacesec/images/master/scan/9.png)
 
 9. 扫描web后台可以访问的目录和文件[用户自定义字典]  
    python scan.py -dir http://127.0.0.1 -t 200 -add C:\Users\Ma\Desktop\1.txt
    ![扫描后台可访问目录默认字典](https://raw.githubusercontent.com/spacesec/images/master/scan/10.png)

 10. 获取补天公益SRC名单保存为txt文件 python scan.py  -url  https://butian.360.cn/Home/Active/company -page 10 -o 补天名单.txt
     ![补天公益SRC保存为txt文件](https://raw.githubusercontent.com/spacesec/images/master/scan/11.png)
 
 11. 扫描学校网站子域名  python scan.py -sdn pku.edu.cn -types 1 -t 200     //1学校 2公司 3政府类网站,如果不指定类型也可以扫描但是扫描会很慢
     ![子域名扫描](https://raw.githubusercontent.com/spacesec/images/master/scan/12.png)
 

******************************************************************************
分割线 分割线	分割线	分割线	分割线	分割线	分割线
******************************************************************************
English introduction:
=========
This is an powerful scanner based on python

What you need to do is just download it and use it because have packaged all third-part modules

What you need to do is just type python scan.py -help and then you can get the result as follows
 
    Usage:
      -host   To scan the open ports of the Host                             Default scanning ports are most usual ports
       -sh     Specific Host Detective                                        Example: -sh 127.0.0.1
       -ah     All alive Hosts .Find all alive hosts                          Example: -ah 192.168.1.1-255 Default ports is 80 443
       -t      Threads(1-200) Default is 80
       -r      Read hosts file                                                Example: -r "hosts.txt"
       -p      Ports                                                          Example: -p="80,8080,443" or -p 1-255 default are most usual ports
       -o      Output file address                                            Example: -o recoder.txt or -o D:\recoder.txt
       -dir    Scanning visible background directory                          Example: -dir http://127.0.0.1
       -add    Dictionary File Address                                        Example: -dir http://127.0.0.1  -add C:\dic.txt
       -sdn    Subdomain names                                                Example: -sdn baidu.com -types 3  -sdn pku.edu.cn -types 1
       -pro    Protocol                                                       Example: -pro https    Default Protocol is http
       -types  Using different dictionary txt file                            1 2 3 means school gov company website,it can makes the result more reliable
       -url    Butian SRC list url                                            Example: -url https://butian.360.cn/Home/Active/company -page 10
       -page   Butian SRC Pages      Default is 10                            Example: -url https://butian.360.cn/Home/Active/company -page 10
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

 8. Scan Web server Background Directory&Files[Default Dictionary]  
    python scan.py -dir http://127.0.0.1 -t 200
    ![扫描后台可访问目录默认字典](https://raw.githubusercontent.com/spacesec/images/master/scan/9.png)
 
 9. Scan Web server Background Directory&Files[Use user's Dictionary]  
    python scan.py -dir http://127.0.0.1 -t 200 -add C:\Users\Ma\Desktop\1.txt
    ![扫描后台可访问目录默认字典](https://raw.githubusercontent.com/spacesec/images/master/scan/10.png)