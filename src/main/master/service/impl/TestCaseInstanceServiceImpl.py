# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.TestCaseInstanceDao import TestCaseInstanceDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('TestCaseInstanceServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"TestCaseInstanceServiceImpl.log")

class TestCaseInstanceService(object):

    def __init__(self):
        self.testCaseInstanceDaoInterface = TestCaseInstanceDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addTestInstance(self,args):
        if "trigger_type" not in args:
            args.setdefault("trigger_type",None)
        return self.testCaseInstanceDaoInterface.addTestInstance(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTestInstanceInfoById(self,instanceId):
        args={}
        args.setdefault("instanceId",instanceId)
        return self.testCaseInstanceDaoInterface.getTestInstanceInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def updateTestInstance(self,args):
        dataResult =self.testCaseInstanceDaoInterface.getTestInstanceInfoById(args.get("instanceId"))
        if dataResult.getSuccess() and len(dataResult.getMessage()) > 0:
            for key, value in dataResult.getMessage()[0].items():
                if key not in args:
                    args.setdefault(key, value)
            return self.testCaseInstanceDaoInterface.updateTestInstance(args)
        logger.error("instanceId [{}] is invalid".format(args.get("instanceId")))
        dataResult.setMessage("instanceId [{}] is invalid".format(args.get("instanceId")))
        return dataResult
