# -*- coding: utf-8 -*-
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
from src.main.master.service.impl.ApplicationServiceImpl import ApplicationService
from src.main.master.service.impl.UserServiceImpl import UserService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('ApplicationController')
logger.write_to_file(SystemConfig.logPathPrefix+"ApplicationController.log")

class ApplicationHandler(tornado.web.RequestHandler):
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
                'getApplicationByProjectId' : lambda : self.getApplicationByProjectId(),
                'getApplicationList': lambda : self.getApplicationList(),
                'getVersionConfig': lambda :self.getVersionConfig(),
                'getApplicationCountByProject':lambda :self.getApplicationCountByProject(),
                'getApplicationById' :lambda :self.getApplicationById(),

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
                'addApplication' : lambda : self.addApplication(),
                'addApplicationVersion' : lambda : self.addApplicationVersion(),
                'deleteApplicationVersion' : lambda :self.deleteApplicationVersion(),
                'addApplicationVersionConfig' : lambda :self.addApplicationVersionConfig(),
                'editVersionConfig' : lambda :self.editVersionConfig(),
                'editApplication': lambda: self.editApplication(),
                'deleteApplication' :lambda :self.deleteApplication(),
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
    def addApplication(self):
        logger.info(self.request.body)
        data = json.loads(self.request.body)
        #数据库该字段可为空,入参没有时,需要补充key,否则访问sql
        if "applicationDescribe" not in data:
            data.setdefault("applicationDescribe",None)
        return ApplicationService().addApplication(data)

    def addApplicationVersion(self):
        logger.info(self.request.body)
        data = json.loads(self.request.body)
        return ApplicationService().addApplicationVersion(data)

    # def getApplicationVersionInfo(self):
    #     return

    def getApplicationList(self):
        userId = self.get_secure_cookie("userId")
        id=userId
        data=UserService().getUserInfoById(id).getMessage()[0]
        if data["isleader"]==0:
            dataResult=ApplicationService().getApplicationList(userId)
        else:
            dataResult=ApplicationService().getApplicationListLeader()
        return dataResult

    def getApplicationByProjectId(self):
        projectId= self.get_argument("projectId")
        return ApplicationService().getApplicationByProjectId(projectId)

    def deleteApplicationVersion(self):
        data = json.loads(self.request.body)
        return ApplicationService().deleteApplicationVersion(data)

    def addApplicationVersionConfig(self):
        data = json.loads(self.request.body)
        return ApplicationService().addApplicationVersionConfig(data)

    def editVersionConfig(self):
        data=json.loads(self.request.body)
        return ApplicationService().editVersionConfig(data)

    def getVersionConfig(self):
        projectId = self.get_argument("projectId")
        applicationId = self.get_argument("applicationId")
        return ApplicationService().getVersionConfig(projectId,applicationId)

    def getApplicationCountByProject(self):
        projectId = self.get_argument("projectId")
        return ApplicationService().getApplicationCountByProject(projectId)

    def getApplicationById(self):
        Id=self.get_argument("id")
        return ApplicationService().getApplicationById(Id)

    def editApplication(self):
        data = json.loads(self.request.body)
        return ApplicationService().editApplication(data)

    def deleteApplication(self):
        data = json.loads(self.request.body)
        return ApplicationService().deleteApplication(data)