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
from src.main.master.service.impl.EnvironmentServiceImpl import EnvironmentService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('EnvironmentController')
logger.write_to_file(SystemConfig.logPathPrefix+"EnvironmentController.log")

class EnvironmentHandler(tornado.web.RequestHandler):
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
                'getEnvironmentInfoById' : lambda : self.getEnvironmentInfoById(),
                'getEnvironmentInfos' : lambda : self.getEnvironmentInfos(),
                'getEnvironmentInfoByUserId': lambda :self.getEnvironmentInfoByUserId()
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
                'addEnvironmentItem' : lambda : self.addEnvironmentItem(),
                'deleteEnvironmentItem':lambda :self.deleteEnvironmentItem(),
                'editEnvironmentItem' : lambda :self.editEnvironmentItem()
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

    def getEnvironmentInfoById(self):
        envId = self.get_argument('envId')
        return EnvironmentService().getEnvironmentInfoById(envId)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addEnvironmentItem(self):
        return EnvironmentService().addEnvironmentItem(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteEnvironmentItem(self):
        return EnvironmentService().deleteEnvironmentItem(json.loads(self.request.body))

    def editEnvironmentItem(self):
        return EnvironmentService().editEnvironmentItem(json.loads(self.request.body))

    def getEnvironmentInfos(self):
        return EnvironmentService().getEnvironmentInfos()

    @tornado.web.authenticated
    def getEnvironmentInfoByUserId(self):
        #useId = self.get_argument('userId')
        useId = self.get_secure_cookie("userId")
        logger.error("userId=" + useId)
        return EnvironmentService().getEnvironmentInfosByUserId(useId)