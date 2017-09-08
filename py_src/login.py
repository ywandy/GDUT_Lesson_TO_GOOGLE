#encoding:utf-8
import requests
import re
import numpy as np
import datetime
from google_ca import *

#global account
#global pwd

url = 'http://222.200.98.147/'
login_url = url + 'login!doLogin.action'                # 登录        
welcome_url = url + 'login!welcome.action'              # 主页面内容   （Html）
verified_url = url + 'yzm?'
Inquire_url = url + 'xsgrkbcx!xsAllKbList.action?xnxqdm=201701'

proxies = {'http':'http://127.0.0.1:8500', 'https':'https://127.0.0.1:8500'}

headers = {
        '(Request-Line)':'POST /login!doLogin.action HTTP/1.1',
        'Host':'222.200.98.147',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'en-US,en;q=0.5',
        'Accept-Encoding':'gzip, deflate',
}

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def login():
    s = requests.Session()
    login_html = s.get(url)
    r = s.get(verified_url, stream=True)

    with open("./" + "verimg.jpg", 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    print("打开这个脚本的根目录里面的验证码图片，并输入验证码")
    vercode = input()
    data_login = {
        'account' : account,
        'pwd' : pwd,
        'verifycode' : vercode
    }
    print("your account:"+account  + "verifycode:" + vercode)
    res = s.post(login_url, data=data_login, headers=headers)    # 登录
    print(res.text)
    dict_res = eval(res.text)
    if 'y' in dict_res['status']:
        print('登录成功！')
    else:
        print('登录失败... 请检查用户名与密码')
    main_html = s.get(welcome_url, headers=headers)                 # 进入主界面
    return s

def Inquire_Lesson(gdata,login_session):
    inquire_html = login_session.get(Inquire_url,headers=headers)
    inquire_html.encoding='utf-8'

    str_get = re.findall(r'{".+"}',inquire_html.text)[0]
    t = eval(str_get)
    for i in t:
        Apart_Infomation(gdata,i)
    #Apart_Infomation(gdata,t[0])


def Apart_Infomation(gdata,element):
    print("科目："+ element["kcmc"])
    print("班级:" + element["jxbmc"])
    print("第：" + element["jcdm2"] + "节")
    print("课室:" + element["jxcdmcs"])
    Parse_Week(gdata,element)
    print("----------------------")

def Parse_Week(gdata,element):
    str_element_week = element["zcs"]
    str_element_time = element["jcdm2"]
    str_element_day =  element["xq"]
    str_element_suject = element["kcmc"]
    str_element_jieshu = element["jcdm2"]
    str_element_location = element["jxcdmcs"]
    lesson_count = int(str_element_time[0:2])
    lesson_day = int(str_element_day) - 1
    l = str_element_week.split(",")
    list_array = np.array(l)
    list_array = list_array.astype('int32')
    list_array.sort()
    print(list_array)
    print("周次:")
    for loop in range(len(list_array)):
        if (lesson_count==1):
            t = datetime.time(8, 30, 0)
        elif(lesson_count==3):
            t = datetime.time(10, 25, 0)
        elif (lesson_count == 5):
            t = datetime.time(13, 50, 0)
        elif (lesson_count == 6):
            t = datetime.time(14, 40, 0)
        elif (lesson_count == 8):
            t = datetime.time(16, 30, 0)
        elif (lesson_count == 10):
            t = datetime.time(18, 30, 0)
        else:
            print("采用默认时间")
        d = datetime.date(2017, 9 , 4+lesson_day)
        dt_c = datetime.datetime.combine(d, t)
        date_tmp = datetime.timedelta(days=int(7*(list_array[loop]-1)))
        starttime = date_tmp+dt_c
        if(loop==0):
            print("第一次上课时间是"+starttime.isoformat("T")+"有"+str(len(list_array))+"条记录")
        print("上课时间:" + starttime.isoformat("T"))
        Add_Lesson(gdata,google_calendar_id,str_element_suject+"  第：" + str_element_jieshu + "节",starttime,str_element_location)


def User_Info_UI():
    print("输入你的教务系统账号:")
    global account
    account = input()
    print("输入你的教务系统密码:")
    global pwd
    pwd = input()
    print(str(account)+str(pwd))
    print("输入你想汇入的日历id，可以从谷歌日历设置查询")
    global google_calendar_id
    google_calendar_id = input()




if __name__ == "__main__":
    gdata = init_google(flags)
    User_Info_UI()
    lg_session = login()
    Inquire_Lesson(gdata,lg_session)
