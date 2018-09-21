﻿﻿中文说明:
========
这是一款基于python3的小巧的扫描工具

我已经将需要的模块封装好了,只需要下载即可使用

您只需要输入python scan.py就可以并且得到如下结果:
	 	
       Usage:
       -host To scan the open ports of the Host
       -sh  Specific Host Detective                                        Example: -sh 127.0.0.1
       -ah  All alive Hosts Find all alive alive hosts                     Example: -ah 192.168.1.1-255
       --h To show help information

优     点:小巧,方便,强大

 1. 扫描特定账主机的端口信息 python scan.py -host 127.0.0.1
    ![](images/scanHost.png) 
    
2. 扫描一定范围内的存活主机  python scan.py -ah 10.86.65.1-255
    ![](images/scanAlive.png)
	
 3. 扫描特定主机存活状态 scan.py -sp 127.0.0.1
    ![](images/scanSpecificHost.png)

	
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
       --h To show help information


Advantage:small but powerful 

1. Scan a specific Host's opened ports information python scan.py -host 127.0.0.1
    ![](images/scanHost.png)

2. Scan to get all alive hosts in a range  python scan.py -ah 10.86.65.1-255
    ![](images/scanAlive.png)

3. Scan a specific host python scan.py 127.0.0.1 
    ![](images/scanSpecificHost.png)
