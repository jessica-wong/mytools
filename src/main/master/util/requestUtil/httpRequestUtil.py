# -*- coding: utf-8 -*-

import sys
import re
import time
import requests
import json
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.core.AdminDecorator import AdminDecoratorServer
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.SessionManageDao import SessionManageDaoInterface

#content-type: multipart/form-data
#set log
logger = Log('requestUtil')
logger.write_to_file(SystemConfig.logPathPrefix +"requestUtil.log")
absolute_http_url_regexp = re.compile(r"^https?://", re.I)

# class RequestBase(object):
#
#     def __init__(self,url,method="GET",format="application/json",params={},timeout=1000,
#                  object=None,saveSession=False,userId=None):
#         self.url =url
#         self.method = method
#         self.format = format
#         self.params = params
#         self.timeout = timeout
#         self.Object = object
#         self.saveSession =saveSession
#         self.userId=userId
#         self.dataResult = DataResult()
#         self.test = "https://testpay.schoolpal.cn/"
#
#     @AdminDecoratorServer.execImplDecorator()
#     def getRequestInstance(self):
#         if self.Object is None:
#             return requests.Session()
#         return self.Object
#
#     @AdminDecoratorServer.execImplDecorator()
#     def parseDomain(self):
#         self.dataResult.setSuccess(True)
#         self.dataResult.setMessage(self.url.replace("http://","").split("/")[0])
#         return self.dataResult
#
#     def route(self):
#         if self.method=="GET":
#             return self.getByCase()
#         elif self.method=="POST":
#             return self.postByCase()
#         else:
#             logger.error("Request method [{0}] not support".format(self.method))
#             self.dataResult.setSuccess(False)
#             self.dataResult.setMessage("Request method [{0}] not support".format(self.method))
#             return self.dataResult
#
#     @AdminDecoratorServer.execImplDecorator()
#     def get(self):
#         headers ={}
#         if self.format is not None:
#             headers["contentType"]=self.format
#         if self.saveSession and self.userId:
#             #debug
#             dataResult = self.parseDomain()
#             if dataResult.getSuccess():
#                 args = {}
#                 args["userId"] = self.userId
#                 args["domain"] = dataResult.getMessage()
#                 sessionResult = SessionManageDaoInterface().getSessionInfo(args)
#                 if sessionResult.getSuccess() and len(sessionResult.getMessage()) > 0:
#                     headers["cookie"] = "SessionId={0}".format(sessionResult.getMessage()[0].get("session"))
#         r = self.getRequestInstance().get(self.url,parmas=self.params,headers=headers,verify=False)
#         if self.saveSession and self.userId:
#             if len(r.cookies.values()) > 0:
#                 dataResult = self.parseDomain()
#                 if dataResult.getSuccess():
#                     args={}
#                     args["userId"]=self.userId
#                     args["domain"]=dataResult.getMessage()
#                     args["session"] = r.cookies.values()[0]
#                     sessionResult =SessionManageDaoInterface().getSessionInfo(args)
#                     if sessionResult.getSuccess() and len(sessionResult.getMessage()) <=0:
#                         SessionManageDaoInterface().addSession(args)
#                     else:
#                         SessionManageDaoInterface().updateSession(args)
#             else:
#                 logger.warn("get session fail:Result [{0}]".format(r.text))
#         return r.text,self.getRequestInstance()
#
#     @AdminDecoratorServer.execImplDecorator()
#     def post(self):
#         headers ={}
#         if self.format is not None:
#             headers["contentType"]=self.format
#         if self.saveSession and self.userId:
#             #pre debug
#             dataResult = self.parseDomain()
#             if dataResult.getSuccess():
#                 args = {}
#                 args["userId"] = self.userId
#                 args["domain"] = dataResult.getMessage()
#                 sessionResult = SessionManageDaoInterface().getSessionInfo(args)
#                 if sessionResult.getSuccess() and len(sessionResult.getMessage()) > 0:
#                     headers["cookie"] = "SessionId={0}".format(sessionResult.getMessage()[0].get("session"))
#         r = self.getRequestInstance().post(self.url,parmas=self.params,headers=headers,verify=False)
#         if self.saveSession and self.userId:
#             #post debug
#             if len(r.cookies.values()) > 0:
#                 dataResult = self.parseDomain()
#                 if dataResult.getSuccess():
#                     args={}
#                     args["userId"]=self.userId
#                     args["domain"]=dataResult.getMessage()
#                     args["session"] = r.cookies.values()[0]
#                     sessionResult =SessionManageDaoInterface().getSessionInfo(args)
#                     if sessionResult.getSuccess() and len(sessionResult.getMessage()) <=0:
#                         SessionManageDaoInterface().addSession(args)
#                     else:
#                         SessionManageDaoInterface().updateSession(args)
#             else:
#                 logger.warn("get session fail:Result [{0}]".format(r.text))
#         return r.text,self.getRequestInstance()
#
#     def init(self,s):
#         url =self.test + "apiBusiness/MerchantBusiness/InitCurrentUser"
#         data={"token":"9dd3e3fd4cf042adc0652527d04f297c","phone":"18201115228"}
#         print (url)
#         r = s.get(url,params=data)
#         print (r.headers)
#         return r.cookies.values()[0]
#
#     @AdminDecoratorServer.execImplDecorator()
#     def getByCase(self):
#         dataResult = DataResult()
#         headers ={}
#         if self.format is not None:
#             headers["contentType"]=self.format
#         r = requests.Session().get(self.url,params=self.params,headers=headers,verify=False)
#         dataResult.setMessage(r.text)
#         dataResult.setSuccess(True)
#         return dataResult
#
#     @AdminDecoratorServer.execImplDecorator()
#     def postByCase(self):
#         dataResult = DataResult()
#         headers ={}
#         if self.format is not None:
#             headers["contentType"]=self.format
#         r = requests.Session().post(self.url,params=self.params,headers=headers,verify=False)
#         dataResult.setMessage(r.text)
#         dataResult.setSuccess(True)
#         return dataResult

class RequestBase(object):

    def __init__(self,url,method="GET",saveSession=False,userId=None,name=None,data=None,
                 headers=None):
        self.url =url
        self.method = method
        #提交参数 包括params、data、json
        self.data = data
        #请求超时时间 秒
        #self.timeout = timeout
        self.Object = object
        self.saveSession =saveSession
        self.userId=userId
        self.headers=headers
        self.name=name
        self.dataResult = DataResult()

    #获取request实例对象
    @AdminDecoratorServer.execImplDecorator()
    def getRequestInstance(self):
        if self.Object is None:
            return requests.Session()
        return self.Object

    # 验证url是否为全路径
    @AdminDecoratorServer.execImplDecorator()
    def parseDomain(self,url):
        if absolute_http_url_regexp.match(url):
            return self.url
        else:
            return "base url missed!"

    # def sendRequest(self,method,url,data,headers):
    #     try:
    #         response=requests.Session().request(method,url,data,headers, verify=False)
    #         # self.dataResult.setSuccess(True)
    #         # self.dataResult.setMessage(response.text)
    #         return response
    #     except:
    #         # self.dataResult.setSuccess(False)
    #         # self.dataResult.setMessage("Request method [{0}] not support".format(self.method)+","+"Request url[{0}] not support".format(self.url))
    #         return ("Request method [{0}] not support".format(self.method)+","+"Request url[{0}] not support".format(self.url))

    @AdminDecoratorServer.execImplDecorator()
    def httpRequest(self, method, url, name=None,data=None,headers=None,**kwargs):
        # store detail data of request and response
        self.meta_data = {}

        # prepend url with hostname unless it's already an absolute URL
        url = self.parseDomain(url)
        # set up pre_request hook for attaching meta data to the request object
        self.meta_data["method"] = method
        kwargs.setdefault("timeout", 1000)
        self.meta_data["request_time"] = time.time()
        response = requests.Session().request(method=method, url=url,data=data,headers=headers,verify=False)
        logger.info(response)
        # record the consumed time
        self.meta_data["response_time_ms"] = round((time.time() - self.meta_data["request_time"]) * 1000, 2)
        self.meta_data["elapsed_ms"] = response.elapsed.microseconds / 1000.0
        self.meta_data["url"] = (response.history and response.history[0] or response) \
            .request.url
        self.meta_data["request_headers"] = response.request.headers
        self.meta_data["request_body"] = response.request.body
        self.meta_data["status_code"] = response.status_code
        self.meta_data["response_headers"] = response.headers
        logger.info(self.meta_data)
        return response

if __name__=="__main__":
    s= requests.Session()