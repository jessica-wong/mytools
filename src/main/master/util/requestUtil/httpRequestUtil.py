# -*- coding: utf-8 -*-

import sys
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

class RequestBase(object):

    def __init__(self,url,method="GET",format="application/json",params={},timeout=1000,
                 object=None,saveSession=False,userId=None):
        self.url =url
        self.method = method
        self.format = format
        self.params = params
        self.timeout = timeout
        self.Object = object
        self.saveSession =saveSession
        self.userId=userId
        self.dataResult = DataResult()
        self.test = "https://testpay.schoolpal.cn/"

    @AdminDecoratorServer.execImplDecorator()
    def getRequestInstance(self):
        if self.Object is None:
            return requests.Session()
        return self.Object

    @AdminDecoratorServer.execImplDecorator()
    def parseDomain(self):
        self.dataResult.setSuccess(True)
        self.dataResult.setMessage(self.url.replace("http://","").split("/")[0])
        return self.dataResult

    def route(self):
        if self.method=="GET":
            return self.getByCase()
        elif self.method=="POST":
            return self.postByCase()
        else:
            logger.error("Request method [{0}] not support".format(self.method))
            self.dataResult.setSuccess(False)
            self.dataResult.setMessage("Request method [{0}] not support".format(self.method))
            return self.dataResult

    @AdminDecoratorServer.execImplDecorator()
    def get(self):
        headers ={}
        if self.format is not None:
            headers["contentType"]=self.format
        if self.saveSession and self.userId:
            #debug
            dataResult = self.parseDomain()
            if dataResult.getSuccess():
                args = {}
                args["userId"] = self.userId
                args["domain"] = dataResult.getMessage()
                sessionResult = SessionManageDaoInterface().getSessionInfo(args)
                if sessionResult.getSuccess() and len(sessionResult.getMessage()) > 0:
                    headers["cookie"] = "SessionId={0}".format(sessionResult.getMessage()[0].get("session"))
        r = self.getRequestInstance().get(self.url,parmas=self.params,headers=headers,verify=False)
        if self.saveSession and self.userId:
            if len(r.cookies.values()) > 0:
                dataResult = self.parseDomain()
                if dataResult.getSuccess():
                    args={}
                    args["userId"]=self.userId
                    args["domain"]=dataResult.getMessage()
                    args["session"] = r.cookies.values()[0]
                    sessionResult =SessionManageDaoInterface().getSessionInfo(args)
                    if sessionResult.getSuccess() and len(sessionResult.getMessage()) <=0:
                        SessionManageDaoInterface().addSession(args)
                    else:
                        SessionManageDaoInterface().updateSession(args)
            else:
                logger.warn("get session fail:Result [{0}]".format(r.text))
        return r.text,self.getRequestInstance()

    @AdminDecoratorServer.execImplDecorator()
    def post(self):
        headers ={}
        if self.format is not None:
            headers["contentType"]=self.format
        if self.saveSession and self.userId:
            #pre debug
            dataResult = self.parseDomain()
            if dataResult.getSuccess():
                args = {}
                args["userId"] = self.userId
                args["domain"] = dataResult.getMessage()
                sessionResult = SessionManageDaoInterface().getSessionInfo(args)
                if sessionResult.getSuccess() and len(sessionResult.getMessage()) > 0:
                    headers["cookie"] = "SessionId={0}".format(sessionResult.getMessage()[0].get("session"))
        r = self.getRequestInstance().post(self.url,parmas=self.params,headers=headers,verify=False)
        if self.saveSession and self.userId:
            #post debug
            if len(r.cookies.values()) > 0:
                dataResult = self.parseDomain()
                if dataResult.getSuccess():
                    args={}
                    args["userId"]=self.userId
                    args["domain"]=dataResult.getMessage()
                    args["session"] = r.cookies.values()[0]
                    sessionResult =SessionManageDaoInterface().getSessionInfo(args)
                    if sessionResult.getSuccess() and len(sessionResult.getMessage()) <=0:
                        SessionManageDaoInterface().addSession(args)
                    else:
                        SessionManageDaoInterface().updateSession(args)
            else:
                logger.warn("get session fail:Result [{0}]".format(r.text))
        return r.text,self.getRequestInstance()

    def init(self,s):
        url =self.test + "apiBusiness/MerchantBusiness/InitCurrentUser"
        data={"token":"9dd3e3fd4cf042adc0652527d04f297c","phone":"18201115228"}
        print (url)
        r = s.get(url,params=data)
        print (r.headers)
        return r.cookies.values()[0]

    def getSchool(self,s,session=""):
        url=self.test + "apiBusiness/TransactionBusiness/GetTransactionInfos"
        data ={"PageIndex":1,"PageSize":10}
        #headers ={"cookie":"SessionId={0}".format(session)}
        #r = s.get(url,data=data,headers=headers)
        r = s.get(url, data=data)
        return r.cookies.values()

    @AdminDecoratorServer.execImplDecorator()
    def getByCase(self):
        dataResult = DataResult()
        headers ={}
        if self.format is not None:
            headers["contentType"]=self.format
        r = requests.Session().get(self.url,params=self.params,headers=headers,verify=False)
        dataResult.setMessage(r.text)
        dataResult.setSuccess(True)
        return dataResult

    @AdminDecoratorServer.execImplDecorator()
    def postByCase(self):
        dataResult = DataResult()
        headers ={}
        if self.format is not None:
            headers["contentType"]=self.format
        r = requests.Session().post(self.url,params=self.params,headers=headers,verify=False)
        dataResult.setMessage(r.text)
        dataResult.setSuccess(True)
        return dataResult

if __name__=="__main__":
    s= requests.Session()
    req = RequestBase("","","","","")
    #r= s.get("http://localhost:8090/v1/interface/getInterfaceInfoById?apiId=1")
    #print (req.init(s))
    print (req.getSchool(s))

