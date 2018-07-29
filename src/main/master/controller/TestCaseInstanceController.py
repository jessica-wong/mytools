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
from src.main.master.service.impl.TestCaseInstanceServiceImpl import TestCaseInstanceService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('TestCaseInstanceController')
logger.write_to_file(SystemConfig.logPathPrefix+"TestCaseInstanceController.log")

class TestCaseInstanceHandler(tornado.web.RequestHandler):
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
                'getTaskInstanceInfoById' : lambda : self.getTaskInstanceInfoById(),
                'getTaskInstanceInfos': lambda: self.getTaskInstanceInfos()

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
                'addTestInstance' : lambda : self.addTestInstance(),
                'updateTestInstance':lambda :self.updateTestInstance()
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

    def getTaskInstanceInfoById(self):
        instanceId = self.get_argument('instanceId')
        return TestCaseInstanceService().getTestInstanceInfoById(instanceId)

    def getTaskInstanceInfos(self):
        return TestCaseInstanceService().getTaskInstanceInfos()

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addTestInstance(self):
        return TestCaseInstanceService().addTestInstance(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def updateTestInstance(self):
        return TestCaseInstanceService().updateTestInstance(json.loads(self.request.body))
