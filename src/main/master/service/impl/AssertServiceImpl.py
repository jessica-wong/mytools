# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.AssertDao import AssertDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('AssertServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"AssertServiceImpl.log")

class AssertService(object):

    def __init__(self):
        self.assertDaoInterface = AssertDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addAssert(self,args):
        if "expect" not in args:
            args.setdefault("expect",None)
        if "sqlContent" not in args:
            args.setdefault("sqlContent",None)
        return self.assertDaoInterface.addAssert(args)

    @AdminDecoratorServer.execImplDecorator()
    def getAssertInfosByContentId(self,contentId):
        args={}
        args.setdefault("contentId",contentId)
        return self.assertDaoInterface.getAssertInfosByContentId(args)

    @AdminDecoratorServer.execImplDecorator()
    def getAssertInfoById(self,assertId):
        args={}
        args.setdefault("assertId",assertId)
        return self.assertDaoInterface.getAssertInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteAssert(self,args):
        return self.assertDaoInterface.deleteAssert(args)

    @AdminDecoratorServer.execImplDecorator()
    def updateAssert(self,args):
        dataResult =self.assertDaoInterface.getAssertInfoById(args)
        if dataResult.getSuccess() and len(dataResult.getMessage()) > 0:
            for key, value in dataResult.getMessage()[0].items():
                if key not in args:
                    args.setdefault(key, value)
            return self.assertDaoInterface.updateAssert(args)
        logger.error("assertId [{}] is invalid".format(args.get("assertId")))
        dataResult.setMessage("assertId [{}] is invalid".format(args.get("assertId")))
        return dataResult

    def deleteAssertByContentId(self,args):
        return self.assertDaoInterface.deleteAssertByContentId(args)