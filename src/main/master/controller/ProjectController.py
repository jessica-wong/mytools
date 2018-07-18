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
from src.main.master.service.impl.ProjectServiceImpl import ProjectService
from src.main.master.service.impl.UserServiceImpl import UserService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('ProjectController')
logger.write_to_file(SystemConfig.logPathPrefix+"ProjectController.log")

class ProjectHandler(tornado.web.RequestHandler):
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
                'getProjectInfoByName' : lambda : self.getProjectInfoByName(),
                'getProjectInfoById': lambda: self.getProjectInfoById(),
                'getProjectList':lambda :self.getProjectList(),
                'getProjectLogListData':lambda :self.getProjectLogListData(),
                'getProjectListByApplicationId' :lambda :self.getProjectListByApplicationId(),
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
                'addProject' : lambda : self.addProject(),
                'deleteProject' :lambda :self.deleteProject(),
                'editProject' : lambda :self.editProject()
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
    def addProject(self):
        logger.info(self.request.body)
        data = json.loads(self.request.body)
        #数据库该字段可为空,入参没有时,需要补充key,否则访问sql
        if "project_describe" not in data:
            data.setdefault("project_describe",None)
        if "version" not in  data:
            data.setdefault("version",None)
        return ProjectService().addProject(data)

    def getProjectInfoByName(self):
        name= self.get_argument("name")
        return ProjectService().getProjectInfoByName(name)

    def getProjectInfoById(self):
        projectId= self.get_argument("projectId")
        return ProjectService().getProjectInfoById(projectId)

    def getProjectList(self):
        userId = self.get_secure_cookie("userId")
        id = userId
        data = UserService().getUserInfoById(id).getMessage()[0]
        logger.info(data)
        if data["isleader"] == 0:
            dataResult = ProjectService().getProjectList(userId)
        else:
            dataResult = ProjectService().getProjectListLeader()
        return dataResult

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteProject(self):
        return ProjectService().deleteProject(json.loads(self.request.body))

    def editProject(self):
        data = json.loads(self.request.body)
        if "release_time" not in data:
            data.setdefault("release_time",None)
        if "project_describe" not in data:
            data.setdefault("project_describe",None)
        if "name" not in  data:
            data.setdefault("name",None)
        return ProjectService().editProject(json.loads(self.request.body))

    def getProjectLogListData(self):
        projectId = self.get_argument("projectId")
        return ProjectService().getProjectLogListData(projectId)

    def getProjectListByApplicationId(self):
        applicationId = self.get_argument("applicationId")
        return ProjectService().getProjectListByApplicationId(applicationId)
