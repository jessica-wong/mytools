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
from src.main.master.service.impl.UserServiceImpl import UserService
from src.main.master.service.impl.ProjectServiceImpl import ProjectService
from src.main.master.service.impl.ApplicationServiceImpl import ApplicationService
from src.main.master.service.impl.TestCaseServiceImpl import TestCaseService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('CommonController')
logger.write_to_file(SystemConfig.logPathPrefix+"CommonController.log")

class CommonHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(30)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,APIName):
        yield self.execute_get(APIName)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self,APIName):
        yield self.execute_post(APIName)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Authorization,Origin,x-requested-with,Content-Type, Accept")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self,APIName):
        # no body
        self.set_status(204)
        self.finish()

    @run_on_executor
    def execute_get(self,APIName):
        dataResult = DataResult()
        try:
            tasks = {
                'getCount': lambda : self.getCount(),
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
    def getCount(self):
        args={}
        args["createUser"]=UserService().getUserCount().getMessage()[0]["userCount"]
        args["project"]=ProjectService().getProjectCount().getMessage()[0]["projectCount"]
        args["application"]=ApplicationService().getApplicationCount().getMessage()[0]["applicationCount"]
        args["testCase"]=TestCaseService().getTestCaseCount().getMessage()[0]["testCaseCount"]
        dataResult = DataResult()
        dataResult.setMessage(args)
        dataResult.setSuccess(True)
        logger.info(dataResult)
        return dataResult
