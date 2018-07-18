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
from src.main.master.service.impl.InterfaceServiceImpl import InterfaceService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('InterfaceController')
logger.write_to_file(SystemConfig.logPathPrefix+"InterfaceController.log")

class InterfaceHandler(tornado.web.RequestHandler):
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
                'getInterfaceInfosByProject' : lambda : self.getInterfaceInfosByProject(),
                'getInterfaceInfoById': lambda: self.getInterfaceInfoById()
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
                'addInterfaceItem' : lambda : self.addInterfaceItem(),
                'deleteInterfaceItem':lambda :self.deleteInterfaceItem(),
                'updateInterfaceItem': lambda : self.updateInterfaceItem(),
                'enableInterfaceItem': lambda: self.enableInterfaceItem(),
                'disableInterfaceItem': lambda: self.disableInterfaceItem(),
                'setInterfaceGroup': lambda :self.setInterfaceGroup(),
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
    def addInterfaceItem(self):
        return InterfaceService().addInterfaceItem(json.loads(self.request.body))

    def getInterfaceInfoById(self):
        interfaceId = self.get_argument('interfaceId')
        return InterfaceService().getInterfaceInfoById(interfaceId)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteInterfaceItem(self):
        return InterfaceService().deleteInterfaceItem(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def disableInterfaceItem(self):
        return InterfaceService().disableInterfaceItem(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def updateInterfaceItem(self):
        return InterfaceService().updateInterfaceItem(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def enableInterfaceItem(self):
        return InterfaceService().enableInterfaceItem(json.loads(self.request.body))

    def getInterfaceInfosByProject(self):
        projectId = self.get_argument('projectId')
        groupId = self.get_argument('groupId')
        offset = self.get_argument('offset')
        limit = self.get_argument('limit')
        return InterfaceService().getInterfaceInfosByProject(projectId,groupId,offset,limit)

    def setInterfaceGroup(self):
        return InterfaceService().setInterfaceGroup(json.loads(self.request.body))