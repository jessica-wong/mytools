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
        if "remarks" not in args:
            args.setdefault("remarks",None)
        caseArgs = copy.deepcopy(args)
        projectId = int(caseArgs["projectId"])
        caseArgs.pop("projectId")
        caseArgs.setdefault("projectId",projectId)
        caseArgs.pop("itemsSteps")
        db = Connection(autocommit=False)
        test_case_sql="""
        insert into testcase (name,create_userid,create_username,update_userid,update_username,
        case_describe,projectid,groupid,gmt_create) values (%(name)s,%(userId)s,%(userName)s,
        %(userId)s,%(userName)s,%(desc)s,%(projectId)s,%(groupId)s,now())
        """
        db.write(test_case_sql,caseArgs)
        caseId = db.read("SELECT LAST_INSERT_ID() AS id",{})
        logger.error("caseId={0}".format(caseId))
        case_content_sql="""
        insert into casecontent (step_name,caseid,step,interfaceid,url,method,format,request_params,
        type,sqlcontent,response_type) values (%(name)s,%(caseId)s,%(step)s,%(interfaceId)s,%(url)s,%(method)s,
        %(format)s,%(request_params)s,%(type)s,%(sqlcontent)s,%(response_type)s)"""
        for stepItem in args["itemsSteps"]:
            if stepItem["statusStep"] ==0:
                continue
            stepJson={}
            stepJson.setdefault("name",stepItem["value"])
            stepJson.setdefault("caseId", caseId[0]["id"])
            stepJson.setdefault("step", stepItem["indexStep"])
            stepJson.setdefault("interfaceId", None)
            stepJson.setdefault("url", stepItem["path"])
            stepJson.setdefault("method", stepItem["method"])
            stepJson.setdefault("format", stepItem["format"])
            stepJson.setdefault("response_type", stepItem["response_type"])
            if stepItem["params"] =="":
                stepJson.setdefault("request_params", None)
            else:
                stepJson.setdefault("request_params", stepItem["params"])
            stepJson.setdefault("type", stepItem["type"])
            if stepItem["sql"]=="":
                stepJson.setdefault("sqlcontent", None)
            else:
                stepJson.setdefault("sqlcontent", stepItem["sql"])
            db.write(case_content_sql,stepJson)
            contentId = db.read("SELECT LAST_INSERT_ID() AS id",{})
            logger.error("contentId={0}".format(contentId))
            assert_sql="""
            insert into assert (casecontentid,actual,expect,assert_type) values (%(contentId)s,
            %(actual)s,%(expect)s,%(type)s)
            """
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
            db.write(assert_sql,assertDatas,True)
        db.commit()
        db.close()
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
                    data["groupId"] = item["groupid"]
                    data["projectId"] = item["projectid"]
                    data["status"] = item["status"]
                if item["contentId"] not in tmpSteps:
                    tmpStepJson = {}
                    tmpSteps[item["contentId"]]=tmpStepJson
                    tmpStepJson["type"]= item["type"]
                    tmpStepJson["method"] = item["method"]
                    tmpStepJson["path"] = item["url"]
                    tmpStepJson["header"] = ""
                    tmpStepJson["params"] = item["request_params"]
                    tmpStepJson["format"] =item["format"]
                    tmpStepJson["sql"] =item["sqlcontent"]
                    tmpStepJson["response_type"] = item["response_type"]
                    tmpStepJson["indexStep"] = item["step"]
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
