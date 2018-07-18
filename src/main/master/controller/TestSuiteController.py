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
from src.main.master.service.impl.TestSuiteServiceImpl import TestSuiteService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('TestSuiteController')
logger.write_to_file(SystemConfig.logPathPrefix+"TestSuiteController.log")

class TestSuiteHandler(tornado.web.RequestHandler):
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
                'getSuiteInfoById': lambda: self.getSuiteInfoById(),
                'getSuiteList' : lambda : self.getSuiteList()
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
                'addTestSuite' : lambda : self.addTestSuite(),
                'deleteTestSuite':lambda :self.deleteTestSuite(),
                'updateTestSuite': lambda : self.updateTestSuite(),
                'editTestSuiteName' : lambda :self.editTestSuiteName()
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
    def addTestSuite(self):
        return TestSuiteService().addTestSuite(json.loads(self.request.body))

    def getSuiteInfoById(self):
        suiteId = self.get_argument('suiteId')
        return TestSuiteService().getSuiteInfoById(suiteId)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteTestSuite(self):
        return TestSuiteService().deleteTestSuite(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def updateTestSuite(self):
        return TestSuiteService().updateTestSuite(json.loads(self.request.body))

    def getSuiteList(self):
        return TestSuiteService().getSuiteList()

    def editTestSuiteName(self):
        return TestSuiteService().editTestSuiteName(json.loads(self.request.body))