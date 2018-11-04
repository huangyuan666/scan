# -- coding: utf-8 --
from module import printc
try:
    import requests
except:
    msg1="[-] 您还没有安装requests依赖包,请使用 pip install requests安装"
    printc.printf(msg1,'red')
try:
    import json
except:
    msg1="[-] 您还没有安装json依赖包,请使用 pip install json安装"
    printc.printf(msg1,'red')
def get_src_name(url,page):
    headers={
            "Accept":"application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': 'gzip,deflate',
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Connection":"keep-alive",
            "Content-Length":"10",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie":"test_cookie_enable=null; __huid=11dIp+4cPb2UVUJ3VSi+9EVDK78UjhPklT9MlHV6Ie07w=; __guid=234331335.4509499323344900096.1540959090001.0793; Q=u%3DZe.%25O0%25Q7%25P3%25N8%26n%3D%26le%3D%26m%3DZGH3WGWOWGWOWGWOWGWOWGWOAmL4%26qid%3D3079140265%26im%3D1_t01923d359dad425928%26src%3Dpcw_webscan%26t%3D1; T=s%3Df30e5e66f2d4794fa9b2d8b974748402%26t%3D1541128157%26lm%3D%26lf%3D2%26sk%3D436d43112e82763129e391715c5d1de2%26mt%3D1541128157%26rc%3D%26v%3D2.0%26a%3D1; PHPSESSID=t9g270t8kpui73agmocdiet0h0; __DC_sid=138613664.1651958209988403700.1541225064082.334; test_cookie_enable=null; __DC_monitor_count=5; __q__=1541225536933; __DC_gid=138613664.814850830.1541034025004.1541225553418.33",
            "Host":"butian.360.cn",
            "Origin":"https://butian.360.cn",
            "Referer":"https://butian.360.cn/Home/Active/hd.html",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"}
    try:
        for p in range(1,int(page)+1):
            data={"type":1,"p":p}
            res=requests.post(url=url,data=data,headers=headers)
            content=res.content
            content=json.loads(content)
            msg1="++++++++++++++++++++++++++++++++++第{p}页++++++++++++++++++++++++++++++++++++++++++".format(p=p)
            printc.printf(msg1,'yellow')
            for i in content['data']["list"]:
                msg2="名字:"+str(i["company_name"])+'   公司ID:'+str(i["company_id"]+"  创办时间:"+str(i["create_time"]))
                printc.printf(msg2,'green')
    except:
        msg3="----------------------------好像出了一点问题----------------------------------"
        printc.printf(msg3,'red')
        pass


# if __name__=='__main__':
#     get_src_name(url,page)
