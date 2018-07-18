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
from src.main.master.service.impl.AssertServiceImpl import AssertService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('AssertController')
logger.write_to_file(SystemConfig.logPathPrefix+"AssertController.log")

class AssertHandler(tornado.web.RequestHandler):
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
                'getAssertInfosByContentId' : lambda : self.getAssertInfosByContentId(),
                'getAssertInfoById': lambda: self.getAssertInfoById()
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
                'addAssert' : lambda : self.addAssert(),
                'deleteAssert':lambda :self.deleteAssert(),
                'updateAssert': lambda: self.updateAssert(),
                'deleteAssertByContentId': lambda :self.deleteAssertByContentId()
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

    def getAssertInfoById(self):
        assertId = self.get_argument('assertId')
        return AssertService().getAssertInfoById(assertId)

    def getAssertInfosByContentId(self):
        contentId = self.get_argument('contentId')
        return AssertService().getAssertInfosByContentId(contentId)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addAssert(self):
        return AssertService().addAssert(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteAssert(self):
        return AssertService().deleteAssert(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def updateAssert(self):
        return AssertService().updateAssert(json.loads(self.request.body))

    def deleteAssertByContentId(self):
        return AssertService().deleteAssertByContentId(json.loads(self.request.body))