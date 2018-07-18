# -*- coding: utf-8 -*-

class SystemConfig:
    #后端日志存放路径,具体日志文件为logPathPrefix + 方法所在文件名称
    logPathPrefix="./LogFiles/"
    #后端http服务的端口,前端默认端口为8080
    httpPost=8090
    #钉钉通知webhook
    dingTalkWebHook=""
    #consumer 消费消息最大个数
    maxThreadSize= 20
    #api访问白名单
    adminHost="::1,127.0.0.1"


class DbConfig:
    #host="localhost"
    host="127.0.0.1"
    user="root"
    passwd="root"
    db="dba"
    port=3306



""""
cd /d H:\shareDDD
python build.py 

cd H:\shareDDD\src\main\master
python server.py


--------------------

cd /d H:\shareDDD\src\main\web
npm run dev


"""
