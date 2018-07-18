# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.ApplicationDao import ApplicationDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('ApplicationServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"ApplicationServiceImpl.log")

class ApplicationService(object):

    def __init__(self):
        self.ApplicationDaoInterface = ApplicationDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addApplication(self,args):

        return self.ApplicationDaoInterface.addApplication(args)

    def addApplicationVersion(self,args):
        logger.info(args)
        return self.ApplicationDaoInterface.addApplicationVersion(args)

    def getApplicationList(self,userId):
        args={}
        args.setdefault("userId",userId)
        logger.info(args)
        return self.ApplicationDaoInterface.getApplicationList(args)

    def getApplicationListLeader(self):
        return self.ApplicationDaoInterface.getApplicationListLeader()

    @AdminDecoratorServer.execImplDecorator()
    def getApplicationByProjectId(self,projectId):
        args={}
        args.setdefault("projectId",projectId)
        return self.ApplicationDaoInterface.getApplicationByProjectId(args)

    @AdminDecoratorServer.execImplDecorator()
    def getInterfaceCountByApplicationVersion(self, projectId,applicationId):
        args = {}
        args.setdefault("projectId", projectId)
        args.setdefault("applicationId",applicationId)
        return self.ApplicationDaoInterface.getInterfaceCountByApplicationVersion(args)

    def deleteApplicationVersion(self,args):
        logger.info(args)
        return self.ApplicationDaoInterface.deleteApplicationVersion(args)

    def addApplicationVersionConfig(self,args):
        logger.info(args)
        return self.ApplicationDaoInterface.addApplicationVersionConfig(args)

    def editVersionConfig(self,args):
        return self.ApplicationDaoInterface.editVersionConfig(args)

    def getVersionConfig(self,projectId,applicationId):
        args = {}
        args.setdefault("projectId", projectId)
        args.setdefault("applicationId", applicationId)
        return self.ApplicationDaoInterface.getVersionConfig(args)

    def getApplicationCountByProject(self,projectId):
        args = {}
        args.setdefault("projectId", projectId)
        return self.ApplicationDaoInterface.getApplicationCountByProject(args)

    def getApplicationCount(self):
        return self.ApplicationDaoInterface.getApplicationCount()

    def getApplicationById(self,Id):
        args = {}
        args.setdefault("Id", Id)
        return self.ApplicationDaoInterface.getApplicationById(args)

    def editApplication(self,id,applicationDescribe,applicationName,departmentId):
        args={}
        args.setdefault("id", id)
        args.setdefault("applicationDescribe", applicationDescribe)
        args.setdefault("applicationName", applicationName)
        args.setdefault("departmentId", departmentId)
        return self.ApplicationDaoInterface.editApplication(args)

    def deleteApplication(self,id):
        args = {}
        args.setdefault("id", id)
        return self.ApplicationDaoInterface.deleteApplication(args)