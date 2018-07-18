# -*- coding: utf-8 -*-

import json
import traceback
import copy
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.TestCaseDao import TestCaseDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer
from src.main.master.util.dbUtil.dbBaseUtil import Connection

#set log
logger = Log('TestCaseServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"TestCaseServiceImpl.log")

class TestCaseService(object):

    def __init__(self):
        self.testCaseDaoInterface = TestCaseDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addTestCase(self,args):
        logger.error("args={0}".format(args))
        dataResult = DataResult()
        #这里需要事务保证一致性
        if "status" not in args:
            args.setdefault("status",None)

        caseArgs = copy.deepcopy(args)
        projectId = int(caseArgs["projectId"])
        caseArgs.pop("projectId")
        caseArgs.setdefault("projectId",projectId)
        applicationId = int(caseArgs["applicationId"])
        caseArgs.pop("applicationId")
        caseArgs.setdefault("applicationId", applicationId)
        caseArgs.pop("itemsSteps")
        data_1 = self.testCaseDaoInterface.addTestCase(caseArgs)
        db = Connection(autocommit=False)

        caseId = self.testCaseDaoInterface.newInsertTestCase()
        logger.error("caseId={0}".format(caseId))

        for stepItem in args["itemsSteps"]:
            if stepItem["statusStep"] ==0:
                continue
            stepJson={}
            stepJson.setdefault("step_name",stepItem["value"])
            stepJson.setdefault("caseId", caseId[0]["id"])
            stepJson.setdefault("execute_step", stepItem["indexStep"])
            stepJson.setdefault("host", stepItem["host"])
            stepJson.setdefault("path", stepItem["path"])
            stepJson.setdefault("method", stepItem["method"])
            stepJson.setdefault("content_type", stepItem["content_type"])
            stepJson.setdefault("headers",stepItem["headers"])
            if stepItem["params"] =="":
                stepJson.setdefault("request_params", None)
            else:
                stepJson.setdefault("request_params", stepItem["params"])

            data_2=self.testCaseDaoInterface.addTestCaseContent(stepJson)
            contentId = self.testCaseDaoInterface.newInsertTestCase()
            logger.error("contentId={0}".format(contentId))

            assertDatas=[]
            for assertItem in stepItem["itemsAsserts"]:
                if assertItem["statusAssert"] ==0:
                    continue
                assertJSON ={}
                assertJSON.setdefault("contentId",contentId[0]["id"])
                assertJSON.setdefault("actual",assertItem["actual"])
                assertJSON.setdefault("expect",assertItem["expect"])
                assertJSON.setdefault("type",assertItem["rules"])
                assertDatas.append(assertJSON)
            data_3 = self.testCaseDaoInterface.addTestCaseAssert(assertDatas)
        dataResult.setSuccess(True)
        dataResult.setMessage(caseId)
        return dataResult

    @AdminDecoratorServer.execImplDecorator()
    def getCaseInfosByCondition(self,projectId,groupId,offset=0,limit=10):
        args={}
        args.setdefault("projectId",projectId)
        args.setdefault("groupId", groupId)
        args.setdefault("offset", int(offset))
        args.setdefault("limit", int(limit))
        return self.testCaseDaoInterface.getCaseInfosByCondition(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteTestCase(self,args):
        return self.testCaseDaoInterface.deleteTestCase(args)

    @AdminDecoratorServer.execImplDecorator()
    def getCaseInfosById(self,caseId):
        args={}
        args.setdefault("caseId",caseId)
        dataResult = self.testCaseDaoInterface.getCaseDetailInfoById(args)
        if dataResult.getMessage():
            data={}
            tmpSteps={}
            for item in dataResult.getMessage():
                if 'id' not in data:
                    data["desc"]= item["case_describe"]
                    data["name"] = item["name"]
                    data["applicationId"] = item["application_id"]
                    data["projectId"] = item["project_id"]
                    data["status"] = item["case_status"]
                if item["contentId"] not in tmpSteps:
                    tmpStepJson = {}
                    tmpSteps[item["contentId"]]=tmpStepJson
                    tmpStepJson["method"] = item["method"]
                    tmpStepJson["host"] = item["ip_url"]
                    tmpStepJson["path"] = item["webapi_path"]
                    tmpStepJson["header"] = item["headers"]
                    tmpStepJson["params"] = item["requests_params"]
                    tmpStepJson["content_type"] =item["content_type"]
                    tmpStepJson["indexStep"] = item["execute_step"]
                    tmpStepJson["statusStep"] = 1
                    tmpStepJson["value"] = item["step_name"]
                if 'itemsAsserts' not in tmpSteps[item["contentId"]]:
                    tmpSteps[item["contentId"]]["itemsAsserts"]=[]
                tmpAssertJson ={}
                tmpAssertJson["statusAssert"] = 1
                tmpAssertJson["index"] = len(tmpSteps[item["contentId"]]["itemsAsserts"])+1
                tmpAssertJson["actual"] = item["actual"]
                tmpAssertJson["rules"] = item["assert_type"]
                tmpAssertJson["expect"] = item["expect"]
                tmpSteps[item["contentId"]]["itemsAsserts"].append(tmpAssertJson)
            data["itemsSteps"]=[]
            for step in tmpSteps:
                data["itemsSteps"].append(tmpSteps[step])
            dataResult.setMessage(data)
            dataResult.setSuccess(True)
        return dataResult

    @AdminDecoratorServer.execImplDecorator()
    def updateTestCase(self,args):
        dataResult = self.testCaseDaoInterface.getCaseInfosById(args)
        if dataResult.getSuccess() and len(dataResult.getMessage())>0:
            for key,value in dataResult.getMessage()[0].items():
                if key not in args:
                    args.setdefault(key,value)
            return self.testCaseDaoInterface.updateTestCase(args)
        logger.error("caseId [{}] is invalid".format(args.get("caseId")))
        dataResult.setMessage("caseId [{}] is invalid".format(args.get("caseId")))
        return dataResult

    def getTestCaseCount(self):
        return TestCaseDaoInterface().getTestCaseCount()

    def getCaseList(self,applicationId,projectId):
        args={}
        args.setdefault("applicationId",applicationId)
        args.setdefault("projectId", projectId)
        return self.testCaseDaoInterface.getCaseList(args)

    def searchCaseByName(self,searchValue,applicationId,projectId):
        args={}
        args.setdefault("searchValue",searchValue)
        args.setdefault("applicationId", applicationId)
        args.setdefault("projectId", projectId)
        return self.testCaseDaoInterface.searchCaseByName(args)
