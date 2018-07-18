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
from src.main.master.service.impl.CaseContentServiceImpl import CaseContentService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('CaseContentController')
logger.write_to_file(SystemConfig.logPathPrefix+"CaseContentController.log")

class CaseContentHandler(tornado.web.RequestHandler):
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
                'getContentInfosByCaseId' : lambda : self.getContentInfosByCaseId(),
                'getContentInfosByContentId': lambda: self.getContentInfosByContentId()
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
                'addCaseContent' : lambda : self.addCaseContent(),
                'deleteTestContentByContentId':lambda :self.deleteTestContentByContentId(),
                'deleteTestContentByCaseId': lambda: self.deleteTestContentByCaseId(),
                'updateTestContent': lambda: self.updateTestContent()
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

    def getContentInfosByCaseId(self):
        caseId = self.get_argument('caseId')
        return CaseContentService().getContentInfosByCaseId(caseId)

    def getContentInfosByContentId(self):
        contentId = self.get_argument('contentId')
        return CaseContentService().getContentInfosByContentId(contentId)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addCaseContent(self):
        return CaseContentService().addCaseContent(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteTestContentByContentId(self):
        return CaseContentService().deleteTestContentByContentId(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteTestContentByCaseId(self):
        return CaseContentService().deleteTestContentByCaseId(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def updateTestContent(self):
        return CaseContentService().updateTestContent(json.loads(self.request.body))