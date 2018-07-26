# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.EnvironmentDao import EnvironmentDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('EnvironmentServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"EnvironmentServiceImpl.log")

class EnvironmentService(object):

    def __init__(self):
        self.EnvironmentDaoInterface = EnvironmentDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addEnvironmentItem(self,args):
        return self.EnvironmentDaoInterface.addEnvironmentItem(args)

    @AdminDecoratorServer.execImplDecorator()
    def getEnvironmentInfoById(self,envId):
        args={}
        args.setdefault("envId",envId)
        return self.EnvironmentDaoInterface.getEnvironmentInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def getEnvironmentInfosByUserId(self,userId):
        args={}
        args.setdefault("userId",userId)
        return self.EnvironmentDaoInterface.getEnvironmentInfosByUserId(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteEnvironmentItem(self,args):
        return self.EnvironmentDaoInterface.deleteEnvironmentItem(args)

    def editEnvironmentItem(self,args):
        if "template" not in args:
            args.setdefault("template",None)
        else:
            if not isinstance(args.get("template"),dict):
                try:
                    #验证data模板是否为json
                    logger.info("template is not dict:{0}".format(args.get("template")))
                    datatemplate = json.dumps(json.loads(args.get("template")))
                    args.pop("template")
                    args.setdefault("template", datatemplate)
                except Exception as e:
                    logger.error(traceback.format_exc())
                    dataResult = DataResult()
                    dataResult.setMessage("template param [{0}]is invalid, must be dict".format(args.get("template")))
                    dataResult.setSuccess(False)
                    return dataResult
            else:
                logger.info("template is dict:{0}".format(args.get("template")))
                datatemplateJSONString = json.dumps(args.get("template"))
                args.pop("template")
                args.setdefault("template",datatemplateJSONString)
        if "headers" not in args:
            args.setdefault("headers",None)
        else:
            if not isinstance(args.get("headers"),dict):
                try:
                    #验证authInfo是否为json
                    logger.info("headers is not dict:{0}".format(args.get("headers")))
                    datatemplate = json.dumps(json.loads(args.get("headers")))
                    args.pop("headers")
                    args.setdefault("headers", datatemplate)
                except Exception as e:
                    logger.error(traceback.format_exc())
                    dataResult = DataResult()
                    dataResult.setMessage("headers param [{0}]is invalid, must be dict".format(args.get("headers")))
                    dataResult.setSuccess(False)
                    return dataResult
            else:
                logger.info("headers is dict:{0}".format(args.get("headers")))
                datatemplateJSONString = json.dumps(args.get("headers"))
                args.pop("headers")
                args.setdefault("headers",datatemplateJSONString)
        if "authInfo" not in args:
            args.setdefault("authInfo",None)
        else:
            if not isinstance(args.get("authInfo"),dict):
                try:
                    #验证authInfo是否为json
                    logger.info("authInfo is not dict:{0}".format(args.get("authInfo")))
                    datatemplate = json.dumps(json.loads(args.get("authInfo")))
                    args.pop("authInfo")
                    args.setdefault("authInfo", datatemplate)
                except Exception as e:
                    logger.error(traceback.format_exc())
                    dataResult = DataResult()
                    dataResult.setMessage("authInfo param [{0}]is invalid, must be dict".format(args.get("authInfo")))
                    dataResult.setSuccess(False)
                    return dataResult
            else:
                logger.info("authInfo is dict:{0}".format(args.get("authInfo")))
                datatemplateJSONString = json.dumps(args.get("authInfo"))
                args.pop("authInfo")
                args.setdefault("authInfo",datatemplateJSONString)

        dataResult = self.EnvironmentDaoInterface.getEnvironmentInfoById(args)
        if dataResult.getSuccess() and len(dataResult.getMessage()) > 0:
            for key,value in dataResult.getMessage()[0].items():
                if key not in args:
                    args.setdefault(key,value)
            return self.EnvironmentDaoInterface.editEnvironmentItem(args)
        dataResult.setMessage("apiId [{0}] is invalid".format(args.get("envId")))
        return dataResult

    def getEnvironmentInfos(self):
        return self.EnvironmentDaoInterface.getEnvironmentInfos()
