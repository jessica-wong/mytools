# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.TestSuiteDao import TestSuiteDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('TestSuiteServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"TestSuiteServiceImpl.log")

class TestSuiteService(object):

    def __init__(self):
        self.testSuiteDaoInterface = TestSuiteDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addTestSuite(self,args):
        if "testcaseids" not in args:
            args.setdefault("testcaseids",None)
        if "remarks" not in args:
            args.setdefault("remarks",None)
        if "status" not in args:
            args.setdefault("status", None)
        return self.testSuiteDaoInterface.addTestSuite(args)

    @AdminDecoratorServer.execImplDecorator()
    def getSuiteInfoById(self,suiteId):
        args={}
        args.setdefault("suiteId",suiteId)
        return self.testSuiteDaoInterface.getSuiteInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteTestSuite(self,args):
        return self.testSuiteDaoInterface.deleteTestSuite(args)

    @AdminDecoratorServer.execImplDecorator()
    def updateTestSuite(self,args):
        dataResult = self.testSuiteDaoInterface.getSuiteInfoById(args)
        if dataResult.getSuccess() and len(dataResult.getMessage())>0:
            for key,value in dataResult.getMessage()[0].items():
                if key not in args:
                    args.setdefault(key,value)
            return self.testSuiteDaoInterface.updateTestSuite(args)
        logger.error("suiteId [{}] is invalid".format(args.get("suiteId")))
        dataResult.setMessage("suiteId [{}] is invalid".format(args.get("suiteId")))
        return dataResult

    def getSuiteList(self):
        return self.testSuiteDaoInterface.getSuiteList()

    def editTestSuiteName(self,args):
        return self.testSuiteDaoInterface.editTestSuiteName(args)