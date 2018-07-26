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
from src.main.master.service.impl.TaskCenterServiceImpl import TaskCenterService
from src.main.master.service.impl.UserServiceImpl import UserService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('TaskCenterController')
logger.write_to_file(SystemConfig.logPathPrefix+"TaskCenterController.log")

class TaskCenterHandler(tornado.web.RequestHandler):
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
                'startTaskBySingleCase' : lambda : self.startTaskBySingleCase(),
                'startTaskByBatchCase' : lambda : self.startTaskByBatchCase(),
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

    # @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def startTaskBySingleCase(self):
        data = json.loads(self.request.body)
        logger.info(data)
        return TaskCenterService().startTaskBySingleCase(data)

    def startTaskByBatchCase(self):
        data = json.loads(self.request.body)
        logger.info(data)
        userId = self.get_secure_cookie("userId")
        userName = self.get_secure_cookie("userName")
        data["userId"]=userId
        data["userName"]=userName
        return TaskCenterService().startTask(data)