# -*- coding: utf-8 -*-

import json
import traceback
import tornado.web
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.service.impl.WebApiServiceImpl import WebApiService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer
import requests
#set log
logger = Log('WebApiController')
logger.write_to_file(SystemConfig.logPathPrefix+"WebApiController.log")

class WebApiHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(30)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,APIName):
        yield self.execute_get(APIName)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self,APIName):
        yield self.execute_post(APIName)

    @run_on_executor
    def execute_get(self,APIName):
        dataResult = DataResult()
        try:
            tasks = {
                'getWebApiForVersion': lambda: self.getWebApiForVersion(),
                'getWebApiInfoById':lambda :self.getWebApiInfoById(),
                'getWebApiList': lambda : self.getWebApiList(),
                'getWebApiInfoByPath':lambda :self.getWebApiInfoByPath(),
                'synchronizeWebApi':lambda :self.synchronizeWebApi(),
                # lambda alias
            }
            self.write(json.dumps(tasks[APIName]().__dict__,cls=CJsonEncoder))
        except:
            logger.error(traceback.format_exc())
            dataResult.setMessage(traceback.format_exc())
            dataResult.setSuccess(False)
            dataResult.setStatusCode(500)
            self.write(json.dumps(dataResult.__dict__))
        finally:
            try:
                self.finish()
            except:
                pass

    @run_on_executor
    def execute_post(self,APIName):
        dataResult = DataResult()
        try:
            tasks = {
                'addWebApi' : lambda : self.addWebApi(),
                'deleteWebApi':lambda :self.deleteWebApi(),
                'updateWebApi': lambda : self.updateWebApi(),
                'setWebApiDiff': lambda : self.setWebApiDiff(),
            }
            self.write(json.dumps(tasks[APIName]().__dict__,cls=CJsonEncoder))
        except:
            logger.error(traceback.format_exc())
            dataResult.setMessage(traceback.format_exc())
            dataResult.setSuccess(False)
            dataResult.setStatusCode(500)
            self.write(json.dumps(dataResult.__dict__))
        finally:
            try:
                self.finish()
            except:
                pass

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addWebApi(self):
        return WebApiService().addWebApi(json.loads(self.request.body))

    def synchronizeWebApi(self):
        swaggerJsonOrUrl = self.get_argument('swaggerJsonOrUrl')
        projectId = self.get_argument('projectId')
        applicationId=self.get_argument('applicationId')
        args = {}
        args.setdefault("swaggerJsonOrUrl", swaggerJsonOrUrl)
        args.setdefault("projectId", projectId)
        args.setdefault("applicationId", applicationId)
        response = requests.post(url="http://192.168.50.27:83/api/swaggerservice/createwebapis",
                                 data=json.dumps(args), headers={"Content-Type": "application/json"})
        dataResult = json.loads(response.text)
        Result = DataResult()
        Result.setSuccess(True)
        Result.setMessage(dataResult)
        logger.info(Result)
        return Result

    def getWebApiForVersion(self):
        applicationId = self.get_argument('applicationId')
        projectId = self.get_argument('projectId')
        return WebApiService().getWebApiForVersion(applicationId,projectId)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteWebApi(self):
        return WebApiService().deleteWebApi(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def updateWebApi(self):
        return WebApiService().updateWebApi(json.loads(self.request.body))

    def getWebApiInfoById(self):
        return WebApiService().getWebApiInfoById(json.loads(self.request.body))

    def getWebApiList(self):
        applicationId = self.get_argument('applicationId')
        projectId = self.get_argument('projectId')
        return WebApiService().getWebApiList(applicationId,projectId)

    def getWebApiInfoByPath(self):
        Path=self.get_argument('Path')
        applicationId = self.get_argument('applicationId')
        projectId = self.get_argument('projectId')
        return WebApiService().getWebApiInfoByPath(applicationId,projectId,Path)

    def setWebApiDiff(self):
        return WebApiService().setWebApiDiff(json.loads(self.request.body))
