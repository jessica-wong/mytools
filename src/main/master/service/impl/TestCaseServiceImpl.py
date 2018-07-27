# -*- coding: utf-8 -*-

import json
import traceback
import copy

from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.TestCaseDao import TestCaseDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer
from src.main.master.dao.WebApiDao import WebApiDaoInterface
from src.main.master.util.dbUtil.dbBaseUtil import Connection

#set log
logger = Log('TestCaseServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"TestCaseServiceImpl.log")

class TestCaseService(object):

    def __init__(self):
        self.testCaseDaoInterface = TestCaseDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addTestCase(self,args,userId):
        logger.info("args={0}".format(args))
        dataResult = DataResult()
        #这里需要事务保证一致性
        if "status" not in args:
            args.setdefault("status",None)
        if "groupId" not in args:
            args.setdefault("groupId",None)
        args.setdefault("userId",userId)
        caseArgs = copy.deepcopy(args)
        projectId = int(caseArgs["projectId"])
        caseArgs.pop("projectId")
        caseArgs.setdefault("projectId",projectId)
        applicationId = int(caseArgs["applicationId"])
        caseArgs.pop("applicationId")
        caseArgs.setdefault("applicationId", applicationId)
        caseArgs.pop("itemsSteps")

        data_1 = self.testCaseDaoInterface.addTestCase(caseArgs)

        if data_1.getSuccess():
            caseId = data_1.getMessage()
            logger.info(caseId)
        else:
            logger.info(data_1.getMessage())
            data_1.setMessage("添加test_case失败")
            return data_1

        for stepItem in args["itemsSteps"]:
            if stepItem["statusStep"] ==0:
                continue
            stepJson={}
            stepJson.setdefault("step_name",stepItem["value"])
            stepJson.setdefault("caseId", caseId)
            stepJson.setdefault("execute_step", stepItem["indexStep"])
            stepJson.setdefault("host", stepItem["host"])
            stepJson.setdefault("path", stepItem["path"])
            stepJson.setdefault("method", stepItem["method"])
            stepJson.setdefault("content_type", stepItem["content_type"])
            stepJson.setdefault("headers",stepItem["header"])
            if stepItem["params"] =="":
                stepJson.setdefault("params", None)
            else:
                stepJson.setdefault("params", stepItem["params"])

            data_2=self.testCaseDaoInterface.addTestCaseContent(stepJson)
            if data_2.getSuccess():
                contentId = data_2.getMessage()
                logger.error(contentId)
            else:
                logger.info(data_2.getMessage())
                data_2.setMessage("添加case_content失败")
                return data_2

            assertDatas=[]
            for assertItem in stepItem["itemsAsserts"]:
                if assertItem["statusAssert"] ==0:
                    continue
                assertJSON ={}
                assertJSON.setdefault("contentId",contentId)
                assertJSON.setdefault("actual",assertItem["actual"])
                assertJSON.setdefault("expect",assertItem["expect"])
                assertJSON.setdefault("type",assertItem["rules"])
                assertDatas.append(assertJSON)
                logger.info(assertDatas)
                data_3 = self.testCaseDaoInterface.addTestCaseAssert(assertJSON)
                logger.info(data_3.getMessage())
            if data_3.getSuccess():
                dataResult.setSuccess(True)
                dataResult.setMessage(caseId)
            else:
                logger.info(data_3.getMessage())
                dataResult.setSuccess(False)
                dataResult.setMessage("添加用例失败")
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
    def updateTestCase(self,args,userId):
        logger.info("args={0}".format(args))
        dataResult = DataResult()
        # 这里需要事务保证一致性
        if "status" not in args:
            args.setdefault("status", None)
        if "groupId" not in args:
            args.setdefault("groupId", None)
        args.setdefault("userId", userId)
        caseArgs = copy.deepcopy(args)
        projectId = int(caseArgs["projectId"])
        caseArgs.pop("projectId")
        caseArgs.setdefault("projectId", projectId)
        applicationId = int(caseArgs["applicationId"])
        caseArgs.pop("applicationId")
        caseArgs.setdefault("applicationId", applicationId)
        caseId = int(caseArgs["caseId"])
        caseArgs.pop("caseId")
        caseArgs.setdefault("caseId", caseId)
        caseArgs.pop("itemsSteps")
        result_1 = self.testCaseDaoInterface.updateTestCase(caseArgs)
        if result_1.getSuccess():
            result_2 = self.testCaseDaoInterface.deleteContentAndAssertIdByCaseId({"caseId":caseId})
        else:
            logger.info(result_1.getMessage())
            result_1.setMessage("更新test_case失败")
            return result_1

        for stepItem in args["itemsSteps"]:
            if stepItem["statusStep"] == 0:
                continue
            stepJson = {}
            stepJson.setdefault("step_name", stepItem["value"])
            stepJson.setdefault("caseId", caseId)
            stepJson.setdefault("execute_step", stepItem["indexStep"])
            stepJson.setdefault("host", stepItem["host"])
            stepJson.setdefault("path", stepItem["path"])
            stepJson.setdefault("method", stepItem["method"])
            stepJson.setdefault("content_type", stepItem["content_type"])
            stepJson.setdefault("headers", stepItem["header"])
            if stepItem["params"] == "":
                stepJson.setdefault("params", None)
            else:
                stepJson.setdefault("params", stepItem["params"])

            data_2 = self.testCaseDaoInterface.addTestCaseContent(stepJson)
            if data_2.getSuccess():
                contentId = data_2.getMessage()
                logger.error(contentId)
            else:
                logger.info(data_2.getMessage())
                data_2.setMessage("更新case_content失败")
                return data_2

            assertDatas = []
            for assertItem in stepItem["itemsAsserts"]:
                if assertItem["statusAssert"] == 0:
                    continue
                assertJSON = {}
                assertJSON.setdefault("contentId", contentId)
                assertJSON.setdefault("actual", assertItem["actual"])
                assertJSON.setdefault("expect", assertItem["expect"])
                assertJSON.setdefault("type", assertItem["rules"])
                assertDatas.append(assertJSON)
                logger.info(assertDatas)
                data_3 = self.testCaseDaoInterface.addTestCaseAssert(assertJSON)
                logger.info(data_3.getMessage())
            if data_3.getSuccess():
                dataResult.setSuccess(True)
                dataResult.setMessage(caseId)
            else:
                logger.info(data_3.getMessage())
                dataResult.setSuccess(False)
                dataResult.setMessage("更新用例失败")

        # 未考虑更新过程中新增步骤的情况
        # for stepItem in args["itemsSteps"]:
        #     if stepItem["statusStep"] == 0:
        #         continue
        #     stepJson = {}
        #     stepJson.setdefault("step_name", stepItem["value"])
        #     stepJson.setdefault("caseId", caseId)
        #     stepJson.setdefault("execute_step", stepItem["indexStep"])
        #     stepJson.setdefault("host", stepItem["host"])
        #     stepJson.setdefault("path", stepItem["path"])
        #     stepJson.setdefault("method", stepItem["method"])
        #     stepJson.setdefault("content_type", stepItem["content_type"])
        #     stepJson.setdefault("headers", stepItem["header"])
        #     if stepItem["params"] == "":
        #         stepJson.setdefault("params", None)
        #     else:
        #         stepJson.setdefault("params", stepItem["params"])
        #
        #     result_2 = self.testCaseDaoInterface.updateTestCaseContent(stepJson)
        #     if result_2.getSuccess()==False:
        #         logger.info(result_2.getMessage())
        #         result_2.setMessage("更新case_content失败")
        #         return result_2
        #
        #     assertDatas = []
        #     for assertItem in stepItem["itemsAsserts"]:
        #         if assertItem["statusAssert"] == 0:
        #             continue
        #         assertJSON = {}
        #         assertJSON.setdefault("caseId", caseId)
        #         assertJSON.setdefault("execute_step", stepItem["indexStep"])
        #         assertJSON.setdefault("actual", assertItem["actual"])
        #         assertJSON.setdefault("expect", assertItem["expect"])
        #         assertJSON.setdefault("type", assertItem["rules"])
        #         assertDatas.append(assertJSON)
        #         logger.info(assertJSON)
        #         result_3 = self.testCaseDaoInterface.updateTestCaseAssert(assertJSON)
        #     if result_3.getSuccess():
        #         dataResult.setSuccess(True)
        #         dataResult.setMessage(caseId)
        #     else:
        #         logger.info(result_3.getMessage())
        #         dataResult.setSuccess(False)
        #         dataResult.setMessage("更新用例失败")

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

    # 当前仅对入参为空的接口进行自动生成用例
    # def createTestCase(self,args):
    #     logger.info(args)
    #     dataResult = DataResult()
    #     # 获取指定应用某个项目中的接口情况
    #     data_1= WebApiDaoInterface().getWebApiPathForProject(args)
    #     if data_1.getSuccess():
    #         if data_1.getMessage()=="":
    #             dataResult.setSuccess(True)
    #             dataResult.setMessage("该版本中还没有接口")
    #             return dataResult
    #         else:
    #             webApiList=data_1.getMessage()
    #     else:
    #         logger.info(data_1.getMessage())
    #         dataResult.setSuccess(False)
    #         dataResult.setMessage("获取接口数据失败")
    #         return dataResult
    #     # 遍历webapilist，自动创建用例
    #     for apiPath in webApiList:
    #         # 查看该版本的接口是否存在该用例用例 用例已经存在时，记录一条日志，并继续，若用例不存在，则创建用例
    #         searchApiInfoData = {}
    #         searchApiInfoData.setdefault("projectId", args["projectId"])
    #         searchApiInfoData.setdefault("applicationId", args["applicationId"])
    #         searchApiInfoData.setdefault("Path", apiPath["Path"])
    #         # 查询指定path的用例
    #         result_1=self.testCaseDaoInterface.getCasePathForProject(searchApiInfoData)
    #         logger.info(result_1.getMessage())
    #         if result_1.getSuccess():
    #             if len(result_1.getMessage()) > 0:
    #                 logger.info(apiPath["Path"] + "的用例已存在")
    #                 continue
    #             else:
    #                 # 构建查询接口参数的数据
    #                 data_3 = WebApiDaoInterface().getWebApiInfosForCase(searchApiInfoData)
    #                 if data_3.getSuccess():
    #                     # 创建test_case
    #                     testCaseData = {}
    #                     testCaseData.setdefault("projectId", args["projectId"])
    #                     testCaseData.setdefault("applicationId", args["applicationId"])
    #                     testCaseData.setdefault("name", "autoTest" + apiPath["Path"])
    #                     testCaseData.setdefault("desc", "为" + apiPath["Path"] + "自动生成冒烟用例")
    #                     data_2 = self.testCaseDaoInterface.createTestCase(testCaseData)
    #                     if data_2.getSuccess():
    #                         caseId = data_2.getMessage()
    #                         # 创建case_content
    #                         content = {}
    #                         contentData = data_3.getMessage()
    #                         logger.info(contentData)
    #                         content.setdefault("caseId", caseId)
    #                         content.setdefault("path", apiPath["Path"])
    #                         content.setdefault("execute_step", "1")
    #                         content.setdefault("step_name", "step1")
    #                         if contentData[0]["Produces"] == "application/json":
    #                             content.setdefault("content_type", 0)
    #                         else:
    #                             # formdata格式置为1,其他格式暂不处理
    #                             content.setdefault("content_type", 1)
    #                         if contentData[0]["Method"] == "get" or contentData[0]["Method"] == "GET" or contentData[0][
    #                             "Method"] == "Get":
    #                             content.setdefault("method", 0)
    #                         elif contentData[0]["Method"] == "post" or contentData[0]["Method"] == "POST" or \
    #                                         contentData[0][
    #                                             "Method"] == "Post":
    #                             content.setdefault("method", 1)
    #                         # 遍历参数，根据参数类型不同，设置入参
    #                         if len(data_3.getMessage()) == 1:
    #                             content.setdefault("params", "")
    #                         elif len(data_3.getMessage()) == 2:
    #                             if contentData[0]["In"] == "query":
    #                                 params = {}
    #                                 params.setdefault(contentData[0]["Name"], "")
    #                                 content.setdefault("params", params)
    #                             elif contentData[0]["In"] == "body":
    #                                 content.setdefault("params", contentData[0]["Schema"])
    #                         elif len(data_3.getMessage()) > 2:
    #                             index = 0
    #                             while index < len(data_3.getMessage()):
    #                                 if contentData[index]["ParameterType"] == 1 and contentData[index]["In"] == "query":
    #                                     params = {}
    #                                     params.setdefault(contentData[index]["Name"], "")
    #                                     index = index + 1
    #                                 else:
    #                                     continue
    #                                 content.setdefault("params", params)
    #                         logger.info(content)
    #                         data_4 = self.testCaseDaoInterface.createTestCaseContent(content)
    #                         # 创建断言
    #                         if data_4.getSuccess():
    #                             contentId = data_4.getMessage()
    #                             assertData = {}
    #                             assertData.setdefault("contentId", contentId)
    #                             assertData.setdefault("actual", "status_code")
    #                             assertData.setdefault("expect", 200)
    #                             assertData.setdefault("type", 0)
    #                             data_5 = self.testCaseDaoInterface.createTestCaseAssert(assertData)
    #                             if data_5.getSuccess():
    #                                 caseIds = []
    #                                 caseIds.append(caseId)
    #                                 dataResult.setMessage(caseIds)
    #                             else:
    #                                 dataResult.setMessage("生成用例失败")
    #                         else:
    #                             logger.info(data_4.getMessage())
    #                             dataResult.setMessage("生成case_content失败")
    #                     else:
    #                         logger.info(data_2.getMessage())
    #                         dataResult.setMessage("创建test_case失败")
    #                 else:
    #                     dataResult.setSuccess(False)
    #                     dataResult.setMessage("获取webapiInfos失败")
    #         else:
    #             logger.info(result_1.getMessage())
    #             dataResult.setSuccess(False)
    #             dataResult.setMessage("获取用例列表失败")
    #     dataResult.setSuccess(True)
    #     return dataResult
    # TODO 根据接口进行自动生成用例
    def syncCreateTestCase(self,args):
        #这里需要用到数据库事务，保证数据一致性和幂等性
        dataResult = DataResult()
        errMessageList =[]
        db = Connection(autocommit=False)
        try:
            logger.info(args)
            # 获取指定应用某个项目中的接口列表
            sql="""
            select Path from webapi where ApplicationId = %(applicationId)s and ProjectId=%(projectId)s
            """
            paths = list(db.read(sql,args))
            logger.info("paths={0}".format(paths))
            if len(paths) == 0:
                dataResult.setSuccess(True)
                dataResult.setMessage("该版本中还没有接口")
                return dataResult
            # 遍历webapilist，自动创建用例
            for apiPath in paths:
                errMessage ={}
                # 查看该版本的接口是否存在该用例用例 用例已经存在时，记录一条日志，并继续，若用例不存在，则创建用例
                searchApiInfoData = {}
                searchApiInfoData.setdefault("projectId", args["projectId"])
                searchApiInfoData.setdefault("applicationId", args["applicationId"])
                searchApiInfoData.setdefault("Path", apiPath["Path"])
                # 查询指定path的用例
                sql="""
                select test_case.id from test_case left join case_content on test_case.id=case_content.case_id 
                where test_case.project_id = %(projectId)s and test_case.application_id =%(applicationId)s 
                and case_content.webapi_path=%(Path)s
                """
                caseInfos = list(db.read(sql,searchApiInfoData))
                if len(caseInfos) > 0:
                    logger.info("用例[{0}]已存在,用例ID:{1}".format(apiPath["Path"],caseInfos[0]["id"]))
                    continue
                else:
                    # 构建查询接口参数的数据,参数详情
                    sql="""
                    select * from webapi left join webapi_parameter on webapi.Id= webapi_parameter.webApiId
                    where webapi.ApplicationId = %(applicationId)s and webapi.ProjectId=%(projectId)s 
                    and webapi.Path=%(Path)s
                    """
                    apiContents = list(db.read(sql,searchApiInfoData))
                    # 创建test_case
                    testCaseData = {}
                    testCaseData.setdefault("projectId", args["projectId"])
                    testCaseData.setdefault("applicationId", args["applicationId"])
                    testCaseData.setdefault("name", "autoTest" + apiPath["Path"])
                    testCaseData.setdefault("desc", "为" + apiPath["Path"] + "自动生成冒烟用例")
                    sql="""
                    insert into test_case (name,case_describe,case_status,project_id,application_id,gmt_create) 
                    values(%(name)s,%(desc)s,0,%(projectId)s,%(applicationId)s,now())
                    """
                    caseId = db.write(sql,testCaseData)
                    # 创建case_content
                    content = {}
                    logger.info("contents={0}".format(content))
                    content.setdefault("caseId", caseId)
                    content.setdefault("path", apiPath["Path"])
                    content.setdefault("execute_step", "1")
                    content.setdefault("step_name", "step1")
                    num =0
                    params ={}
                    for apiContent in apiContents:
                        if num ==0:
                            if apiContent["Produces"] == "application/json":
                                content.setdefault("content_type", 0)
                            else:
                                # formdata格式置为1,其他格式暂不处理
                                content.setdefault("content_type", 1)
                            if apiContent["Method"].lower() == "get":
                                content.setdefault("method", 0)
                            elif apiContent["Method"].lower() == "post":
                                content.setdefault("method", 1)
                            else:
                                errMessage.setdefault("path",apiPath["Path"])
                                errMessage.setdefault("errMessage","请求类型只支持get、post")
                                errMessageList.append(errMessage)
                                break
                            #content.setdefault("outPut", apiContent["Schema"])
                        # 遍历参数，根据参数类型不同，设置入参 注意入参和出参
                        if apiContent["ParameterType"] == 1:
                            if apiContent["In"] == "query":
                                params.setdefault(apiContent["Name"], "")
                            elif apiContent["In"] == "body":
                                params = apiContent["Schema"]
                                break
                    if isinstance(params,dict):
                        content.setdefault("params",json.dumps(params))
                    else:
                        content.setdefault("params",params)
                    sql="""
                    insert into case_content (case_id,webapi_path,method,content_type,requests_params,execute_step,step_name) 
                    values (%(caseId)s,%(path)s,%(method)s,%(content_type)s,%(params)s,%(execute_step)s,%(step_name)s)
                    """
                    contentId = db.write(sql,content)
                    # 创建断言
                    assertData = {}
                    assertData.setdefault("contentId", contentId)
                    assertData.setdefault("actual", "status_code")
                    assertData.setdefault("expect", 200)
                    assertData.setdefault("type", 0)
                    sql="""
                    insert into assert (casecontentid,actual,expect,assert_type) values (%(contentId)s,
                    %(actual)s,%(expect)s,%(type)s)
                    """
                    db.write(sql,assertData)
            db.commit()
            dataResult.setMessage(errMessageList)
            dataResult.setSuccess(True)
            return dataResult
        except Exception as err:
            logger.error(err)
            dataResult.setSuccess(False)
            dataResult.setMessage(errMessageList)
            return dataResult
        finally:
            db.close()