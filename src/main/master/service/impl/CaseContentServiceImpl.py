# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.CaseContentDao import CaseContentDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('CaseContentServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"CaseContentServiceImpl.log")

class CaseContentService(object):

    def __init__(self):
        self.caseContentDaoInterface = CaseContentDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addCaseContent(self,args):
        if "interfaceId" not in args:
            args.setdefault("interfaceId",None)
        if "url" not in args:
            args.setdefault("url",None)
        if "method" not in args:
            args.setdefault("method",None)
        if "format" not in args:
            args.setdefault("format",None)
        if "requestParams" not in args:
            args.setdefault("requestParams",None)
        else:
            request_params = json.dumps(args.get("requestParams"))
            args.pop("requestParams")
            args.setdefault("requestParams", request_params)
        if "timeout" not in args:
            args.setdefault("timeout",None)
        if "type" not in args:
            args.setdefault("type",None)
        if "sqlContent" not in args:
            args.setdefault("sqlContent", None)
        return self.caseContentDaoInterface.addCaseContent(args)

    @AdminDecoratorServer.execImplDecorator()
    def getContentInfosByCaseId(self,caseId):
        args={}
        args.setdefault("caseId",caseId)
        return self.caseContentDaoInterface.getContentInfosByCaseId(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteTestContentByContentId(self,args):
        logger.error(args)
        return self.caseContentDaoInterface.deleteTestContentByContentId(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteTestContentByCaseId(self,args):
        return self.caseContentDaoInterface.deleteTestContentByCaseId(args)

    @AdminDecoratorServer.execImplDecorator()
    def updateTestContent(self,args):
        if "interfaceId" not in args:
            args.setdefault("interfaceId",None)
        if "url" not in args:
            args.setdefault("url",None)
        if "method" not in args:
            args.setdefault("method",None)
        if "format" not in args:
            args.setdefault("format",None)
        if "requestParams" not in args:
            args.setdefault("requestParams",None)
        else:
            request_params = json.dumps(args.get("requestParams"))
            args.pop("requestParams")
            args.setdefault("requestParams", request_params)
        if "timeout" not in args:
            args.setdefault("timeout",None)
        if "type" not in args:
            args.setdefault("type",None)
        if "sqlContent" not in args:
            args.setdefault("sqlContent", None)
        dataResult =self.caseContentDaoInterface.getContentInfosByContentId(args)
        if dataResult.getSuccess() and len(dataResult.getMessage()) > 0:
            for key, value in dataResult.getMessage()[0].items():
                if key not in args:
                    args.setdefault(key, value)
            return self.caseContentDaoInterface.updateTestContent(args)
        logger.error("contentId [{}] is invalid".format(args.get("contentId")))
        dataResult.setMessage("contentId [{}] is invalid".format(args.get("contentId")))
        return dataResult

    def getContentInfosByContentId(self,contentId):
        args = {}
        args.setdefault("contentId", contentId)
        return self.caseContentDaoInterface.getContentInfosByContentId(args)