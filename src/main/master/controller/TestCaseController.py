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
from src.main.master.service.impl.TestCaseServiceImpl import TestCaseService
from src.main.master.service.impl.TaskCenterServiceImpl import TaskCenterService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('TestCaseController')
logger.write_to_file(SystemConfig.logPathPrefix+"TestCaseController.log")

class TestCaseHandler(tornado.web.RequestHandler):
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
                'getCaseInfosByCondition' : lambda : self.getCaseInfosByCondition(),
                'getCaseInfosById': lambda: self.getCaseInfosById(),
                'getCaseList' : lambda : self.getCaseList(),
                'searchCaseByName' : lambda : self.searchCaseByName(),
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
                'addTestCase' : lambda : self.addTestCase(),
                'deleteTestCase':lambda :self.deleteTestCase(),
                'updateTestCase': lambda : self.updateTestCase(),
                'startTaskBySingleCase': lambda :self.startTaskBySingleCase(),
                'createTestCase': lambda :self.createTestCase(),
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
    def addTestCase(self):
        userId = self.get_secure_cookie("userId")
        return TestCaseService().addTestCase(json.loads(self.request.body),userId)

    def getCaseInfosById(self):
        caseId = self.get_argument('caseId')
        return TestCaseService().getCaseInfosById(caseId)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteTestCase(self):
        return TestCaseService().deleteTestCase(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def updateTestCase(self):
        userId = self.get_secure_cookie("userId")
        return TestCaseService().updateTestCase(json.loads(self.request.body),userId)

    def getCaseInfosByCondition(self):
        projectId = self.get_argument('projectId')
        groupId = self.get_argument('groupId')
        offset = self.get_argument('offset')
        limit = self.get_argument('limit')
        return TestCaseService().getCaseInfosByCondition(projectId,groupId,offset,limit)

    # @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    # def startTaskBySingleCase(self):
    #     return TaskCenterService().startTaskBySingleCase(json.loads(self.request.body))

    def getCaseList(self):
        projectId = self.get_argument('projectId')
        applicationId=self.get_argument('applicationId')
        return TestCaseService().getCaseList(applicationId,projectId)

    def searchCaseByName(self):
        searchValue=self.get_argument("searchValue")
        projectId = self.get_argument('projectId')
        applicationId = self.get_argument('applicationId')
        return TestCaseService().searchCaseByName(searchValue,projectId,applicationId)

    def createTestCase(self):
        return TestCaseService().syncCreateTestCase(json.loads(self.request.body))
