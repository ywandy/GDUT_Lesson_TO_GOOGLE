# 广东工业大学课程表导入到Google 日历

### 操作步骤: 
1.确保程序源码目录下面有.credentials文件夹，没有需要创建，并且保证里面有一个calendar-python-quickstart.json的文件，空的也行    

2.在Google API 里面打开Google Calendar 的API授权，并且开启网页验证Oauth2 ，下载client_secret_xxxxxx.json文件到程序源码的根目录，改名为client_secret.json   

3.在有程序全局代理的情况下，执行  
 'python login.py --noauth_local_webserver'  
 
4.关于日历id在谷歌日历设置里面，选择日历，进去想要的日历里面有日历网址  

5.然后坐和放宽，就可把课程表导入  

### python库
numpy requests google-api-python-client  
关于验证部分可以参考谷歌API说明文档:  
https://developers.google.com/google-apps/calendar/quickstart/python