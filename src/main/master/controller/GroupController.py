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
from src.main.master.service.impl.GroupServiceImpl import GroupService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('GroupController')
logger.write_to_file(SystemConfig.logPathPrefix+"GroupController.log")

class GroupHandler(tornado.web.RequestHandler):
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
                'getGroupInfoByProjectId' : lambda : self.getGroupInfoByProjectId(),
                'getGroupByProjectId' : lambda :self.getGroupByProjectId()
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
                'addParentGroup' : lambda : self.addParentGroup(),
                'addChildGroup' : lambda : self.addChildGroup(),
                'deleteGroup':lambda :self.deleteGroup(),
                'editGroup' : lambda :self.editGroup()
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

    def getGroupInfoByProjectId(self):
        projectId = self.get_argument('projectId')
        type = self.get_argument('type',0)
        return GroupService().getGroupInfoByProjectId(projectId,type)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addParentGroup(self):
        return GroupService().addParentGroup(json.loads(self.request.body))

    def addChildGroup(self):
        return GroupService().addChildGroup(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteGroup(self):
        return GroupService().deleteGroup(json.loads(self.request.body))

    def editGroup(self):
        return GroupService().editGroup(json.loads(self.request.body))

    def getGroupInfoByParentGroupId(self):
        return GroupService().getGroupInfoByParentGroupId(self.request.body)

    def getGroupByProjectId(self):
        projectId = self.get_argument('projectId')
        type = self.get_argument('type')
        return GroupService().getGroupByProjectId(projectId, type)