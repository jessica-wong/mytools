# -*- coding: utf-8 -*-

import json
import traceback
import threadpool
import os
import re
import time
import datetime
import socket
from jinja2 import Template
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.TaskMetaqInfoDao import TaskMetaqInfoDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer
from src.main.master.dao.TestCaseInstanceDao import TestCaseInstanceDaoInterface
from src.main.master.dao.TestSuiteDao import TestSuiteDaoInterface
from src.main.master.dao.TestCaseDao import TestCaseDaoInterface
from src.main.master.dao.CaseContentDao import CaseContentDaoInterface
from src.main.master.dao.AssertDao import AssertDaoInterface
from src.main.master.dao.CaseResultDao import CaseResultDaoInterface
from src.main.master.dao.EnvironmentDao import EnvironmentDaoInterface
from operator import attrgetter
from src.main.master.util.requestUtil.httpRequestUtil import RequestBase
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.assertUtil.assertUtil import AssertInstance

#set log
logger = Log('TaskCenterServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"TaskCenterServiceImpl.log")

#global
pool = threadpool.ThreadPool(10)

class TaskCenterService(object):

    def __init__(self):
        pass

    #2
    @staticmethod
    @AdminDecoratorServer.execImplDecorator()
    def __sendTaskJob(taskInfo):
        #set task queue status is send
        tmp_args={}
        tmp_args.setdefault("status","1")
        tmp_args.setdefault("taskId",taskInfo.get("id"))
        dataResult = TaskMetaqInfoDaoInterface().updateTaskStatus(tmp_args)
        if dataResult.getSuccess():
            #exec task
            return TaskCenterService.__execTaskJob(taskInfo)
        else:
            #set task is invaild
            logger.error("send task failed.reason:{0}".format(dataResult.getMessage()))
            return TaskMetaqInfoDaoInterface().deleteTaskInfo(tmp_args)

    #3
    @staticmethod
    @AdminDecoratorServer.execImplDecorator()
    def __execTaskJob(taskInfo):
        taskInstanceId = taskInfo.get("instanceid")
        logger.info("exec task [{0}]:".format(taskInstanceId))
        args = {}
        args.setdefault("instanceId", taskInstanceId)
        args.setdefault("build_start",datetime.datetime.now())
        result = DataResult()
        taskGlobalStatus = "Error"
        try:
            #set metaq queue status is received
            metaq_args={}
            metaq_args.setdefault("status", "2")
            #hostname
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            metaq_args.setdefault("running_consumer", "{0}|{1}".format(ip, hostname))
            metaq_args.setdefault("msg_id", os.getpid())
            metaq_args.setdefault("taskId", taskInfo.get("id"))
            TaskMetaqInfoDaoInterface().updateTaskInfo(metaq_args)
            #query task instance info by id
            logger.info("query task instance [{0}] ...".format(taskInstanceId))
            dataResult = TestCaseInstanceDaoInterface().getTestInstanceInfoById(args)
            if dataResult.getSuccess() and len(dataResult.getMessage()) > 0:
                suiteId = dataResult.getMessage()[0].get("suite_id")
                userId = dataResult.getMessage()[0].get("create_userid")
                #set instance Running
                args.setdefault("build_end", None)
                args.setdefault("status", "Running")
                TestCaseInstanceDaoInterface().updateTestInstance(args)
                logger.info("query suite [{0}]by instance [{1}] ...".format(suiteId,taskInstanceId))
                dataResult =TestSuiteDaoInterface().getSuiteInfoById({"suiteId":suiteId})
                if dataResult.getSuccess() and len(dataResult.getMessage()) > 0:
                    envId = dataResult.getMessage()[0].get("envid")
                    caseIds = dataResult.getMessage()[0].get("testcaseids")
                    #get global env param
                    envResult = EnvironmentDaoInterface().getEnvironmentInfoById({"envId":envId})
                    if envResult.getSuccess() and len(envResult.getMessage()) <= 0:
                        logger.error("Test suite [{0}]:No env config".format(suiteId))
                        taskGlobalStatus = "Failed"
                        return result
                    if caseIds is None or len(caseIds) == 0:
                        logger.info("Test suite [{0}]:No case".format(suiteId))
                        taskGlobalStatus="Success"
                    else:
                        # get init case for save session
                        initResult = TaskCenterService.__getInitCaseJob(caseIds)
                        if not initResult.getSuccess():
                            logger.error("Test suite [{0}]:No init case".format(suiteId))
                            taskGlobalStatus = "Failed"
                            return result
                        initCaseInfo = initResult.getMessage()[0]
                        initCaseId = initCaseInfo.get("id")
                        #return request Object
                        initRequest = TaskCenterService.__execTaskCaseJob(initCaseId,userId,envResult[0],None,True,taskInstanceId,"init")
                        for caseId in list(caseIds):
                            if caseId == initCaseId:
                                continue
                            dataResult =TestCaseInstanceDaoInterface().getTestInstanceInfoById(args)
                            if dataResult.getMessage()[0].get("status") not in ["Stopped","TimeOut"]:
                                execResult = TaskCenterService.__execTaskCaseJob(caseId,None,envResult[0],initRequest.getMessage(),True,taskInstanceId,None)
                                if not execResult.getSuccess():
                                    #set instance db
                                    taskGlobalStatus = execResult.getMessage()
                                    return result
                            else:
                                logger.error("Task instance [{0}] is stopped".format(args.get("instanceId")))
                                taskGlobalStatus = dataResult.getMessage()[0].get("status")
                                return result
                        taskGlobalStatus = "Success"
                        result.setSuccess(True)
                        return result
        except Exception as e:
            logger.error("Exception:{0}".format(traceback.format_exc()))
            return result
        finally:
            args.setdefault("build_end", datetime.datetime.now())
            args.setdefault("status",taskGlobalStatus)
            TestCaseInstanceDaoInterface().updateTestInstance(args)

    #4
    @staticmethod
    @AdminDecoratorServer.execImplDecorator()
    def __execTaskCaseJob(caseId,userId=None,envConfig=False,requestObject=None,init=False, \
                          instanceId=None,caseName=None):
        if not envConfig:
            caseInfo = TestCaseDaoInterface().getCaseInfosById({"caseId",caseId})
            if caseInfo.getSuccess() and len(caseInfo.getMessage()) >0:
                envId = caseInfo.getMessage()[0].get("envid")
                envResult = EnvironmentDaoInterface().getEnvironmentInfoById({"envId": envId})
                if envResult.getSuccess() and len(envResult.getMessage()) <= 0:
                    logger.error("Test envId [{0}]:No env config".format(envId))
                    return
                envConfig = envResult[0]
            else:
                return
        if init:
            saveSession =False
        elif requestObject is not None:
            saveSession =False
        else:
            saveSession =True
        exec_start_flag=time.time()
        exec_start=datetime.datetime.now()
        contentResult = CaseContentDaoInterface().getContentInfosByCaseId(caseId)
        Presult ={}
        statusFlag =True
        if contentResult.getSuccess() and len(contentResult.getMessage()) > 0:
            for content in sorted(ontentResult.getMessage(), key=attrgetter('step')):
                #TODO "DATARESULT" + STEP
                response=None
                #request api
                if content.get("type")==0:
                    if envConfig.get("datatemplate").endswith("/"):
                        url = envConfig.get("datatemplate")[:-1] + content.get("url")
                    else:
                        url = envConfig.get("datatemplate") + content.get("url")
                    params = TaskCenterService.__rendeTemplate(content.get("request_params"),envConfig.get("datatemplate"),Presult)
                    requestUtil = RequestBase(url=url,method=content.get("method"),format=content.get("format"),params=params,
                                              object=requestObject,userId=userId,saveSession=saveSession)
                    response,obj = requestUtil.route()
                    try:
                        response = json.loads(response)
                    except Exception as e:
                        logger.warn("return result is not json:{0} Exception:{1}".format(response,e))
                #request sql
                elif content.get("type")==1:
                    dbConfig={}
                    dbConfig.setdefault("db",envConfig.get("dbname"))
                    dbConfig.setdefault("host", envConfig.get("dbhostname"))
                    dbConfig.setdefault("user", envConfig.get("dbusername"))
                    dbConfig.setdefault("passwd", envConfig.get("dbpasswd"))
                    dbConfig.setdefault("port", envConfig.get("dbport"))
                    dbUtil = DbBaseHelper()
                    response = dbUtil.execReadOnlySQL(dbConfig,TaskCenterService.__rendeTemplate(content.get("sqlcontent"),envConfig.get("datatemplate"),Presult,False))
                Presult.setdefault("DATAREAULT"+str(content.get("step")),response)
                #assert
                assertResult = AssertDaoInterface().getAssertInfosByContentId(content.get("id"))
                if assertResult.getSuccess():
                    for assertInfo in assertResult:
                        result = TaskCenterService.__execAssertJob(eval("Presult."+assertInfo.get("actual")),assertInfo.get("expect"),assertInfo.get("assert_type"))
                        if not result.getSuccess():
                            statusFlag = False
                            break
        if saveSession:
            exec_end_flag = time.time()
            exec_end = datetime.datetime.now()
            if statusFlag:
                status = "Success"
            else:
                status = "Failed"
            #caseResult
            caseResultInfo={}
            caseResultInfo.setdefault("instanceid",instanceId)
            caseResultInfo.setdefault("caseid",caseId)
            caseResultInfo.setdefault("casename",caseName)
            caseResultInfo.setdefault("runtime",exec_end_flag-exec_start_flag)
            caseResultInfo.setdefault("exec_start",exec_start)
            caseResultInfo.setdefault("exec_end",exec_end)
            caseResultInfo.setdefault("status",status)
            caseResultInfo.setdefault("messaga",response)
            caseResultInfo.setdefault("remarks",None)
            CaseResultDaoInterface().addCaseResult(caseResultInfo)
        dataResult =DataResult()
        dataResult.setSuccess(statusFlag)
        if init:
            dataResult.setMessage(obj)
        else:
            dataResult.setMessage(status)
        return dataResult

    @staticmethod
    @AdminDecoratorServer.execImplDecorator()
    def __execAssertJob(actual,expect,assert_type="0"):
        #equal
        if assert_type=="0":
            result=AssertInstance.get_instance().isEqual(actual,expect)
        #not equal
        elif assert_type=="1":
            result=AssertInstance.get_instance().notEqual(actual, expect)
        #contain
        elif assert_type=="2":
            result=AssertInstance.get_instance().isContain(actual, expect)
        #not contain
        elif assert_type=="3":
            result=AssertInstance.get_instance().notContain(actual, expect)
        else:
            result = False
        assertResult = DataResult()
        assertResult.setSuccess(result)
        assertResult.setMessage("Notice:actual={0},expect={1}\n".format(actual,expect))
        return assertResult

    @staticmethod
    @AdminDecoratorServer.execImplDecorator()
    def __getInitCaseJob(caseIds):
        #eg:[1,2,3,4,5,6,7]
        args={}
        Ids = caseIds[1:-1]
        logger.info("get init case:{0}".format(Ids))
        args["caseIds"] = Ids
        dataResult =TestCaseDaoInterface().getInitCaseInfoByIds(args)
        if dataResult.getSuccess() and len(dataResult.getMessage()) > 0:
            return dataResult
        dataResult.setSuccess(False)
        return dataResult

    @staticmethod
    @AdminDecoratorServer.execImplDecorator()
    def __rendeTemplate(tmpl,param,Presult,isJson=True):
        template = Template(tmpl)
        tmplString = template.render(param)
        if isJson:
            tmplJson = json.loads(tmplString)
            for k,v in tmplJson.items():
                if type(v) =="str" and re.match("##",v):
                    tmplJson.setdefault(k,eval("Presult."+v[2:]))
            return tmplJson
        return eval("Presult."+tmplString)

    #1
    @AdminDecoratorServer.execImplDecorator()
    def sendTask(self):
        args={}
        args.setdefault("limit",SystemConfig.maxThreadSize)
        dataResult = TaskMetaqInfoDaoInterface().getWaitingTaskInfos(args)
        if dataResult.getSuccess():
            logger.info("send Task start:{0}".format(dataResult.getMessage()))
            #目前支持local执行,后期可支持远程consumer或者jenkins
            requests = threadpool.makeRequests(self.__sendTaskJob,dataResult.getMessage())
            for req in requests:
                time.sleep(0.1)
                pool.putRequest(req)
            pool.wait()
            return dataResult
        else:
            logger.error("get waiting task failure:{0}".format(dataResult.getMessage()))
            return dataResult

    @AdminDecoratorServer.execImplDecorator()
    def stopTask(self,args):
        pass

    @AdminDecoratorServer.execImplDecorator()
    def startTask(self,args):
        # 暂时不支持套件
        args.setdefault("suiteName","")
        args.setdefault("suiteId",0)
        # 排队中
        args.setdefault("status",0)
        # 手工触发
        args.setdefault("triggerType",0)
        return TestCaseInstanceDaoInterface().addTestInstance(args)


    @AdminDecoratorServer.execImplDecorator()
    def execTask(self,args):
        pass

    @AdminDecoratorServer.execImplDecorator()
    def crontabTask(self):
        args={}
        args.setdefault("limit",SystemConfig.maxThreadSize)
        pendingTasks = TestCaseInstanceDaoInterface().getPengdingInstanceInfos(args)
        for pendingTask in list(pendingTasks):
            # 回写master 实例状态  排队--->运行中
            pendingTask["status"] = 1
            dateResult = TestCaseInstanceDaoInterface().updateTestInstanceStatus(pendingTask)
            if dateResult.getSuccess():
                # 异步执行测试任务 需要用到线程池
                self.startTaskByBatchCase(pendingTask)

    @AdminDecoratorServer.execImplDecorator()
    def queryTask(self):
        pass

    # def startTaskBySingleCase(self,args):
    #     message=[]
    #     contents = CaseContentDaoInterface().getContentInfosByCaseId(args)
    #     if contents.getSuccess():
    #         for content in contents.getMessage():
    #             if int(content["method"]) == 0:
    #                 method = "GET"
    #             else:
    #                 method= "POST"
    #             if int(content["content_type"]) ==0:
    #                 format ="application/json"
    #             else:
    #                 format="application/x-www-form-urlencoded"
    #             if content["requests_params"] is None or content["requests_params"] =="":
    #                 params={}
    #             else:
    #                 params = json.loads(content["requests_params"])
    #             logger.error(content["webapi_path"])
    #             logger.error(method)
    #             logger.error(format)
    #             logger.error(params)
    #             requestUtil = RequestBase(url=content["ip_url"]+content["webapi_path"], method=method, format=format,params=params)
    #             response = requestUtil.route()
    #             logger.error(response.getMessage())
    #             logger.error(response.getSuccess())
    #             tmpArgs={}
    #             tmpArgs[content["step_name"]]= response.getMessage()
    #             message.append(tmpArgs)
    #         logger.error(message)
    #         contents.setSuccess(True)
    #         contents.setMessage(message)
    #     return contents

    @AdminDecoratorServer.execImplDecorator()
    def startTaskBySingleCase(self,args):
        message=[]
        logger.info(args)
        contents = CaseContentDaoInterface().getContentInfosByCaseId(args)

        if contents.getSuccess():
            for content in contents.getMessage():

                if int(content["method"]) == 0:
                    method = "GET"
                else:
                    method= "POST"
                if int(content["content_type"]) ==0:
                    contentType ="application/json"
                    if content["requests_params"] is None or content["requests_params"] == "":
                        data = {}
                    else:
                        data = eval(content["requests_params"])
                        data = json.dumps(data)
                else:
                    contentType="application/x-www-form-urlencoded"
                    if content["requests_params"] is None or content["requests_params"] == "":
                        data = {}
                    else:
                        data = eval(content["requests_params"])
                        data = data

                if len(args["envName"])>0:
                    environments = EnvironmentDaoInterface().getEnvironmentInfoByName(args)
                    environment=environments.getMessage()[0]
                    logger.info(environment["pre_url"])
                    if environment["pre_url"] is None or environment["pre_url"]=="":
                        if content["webapi_path"] is None or content["webapi_path"] == "":
                            contents.setSuccess(False)
                            contents.setMessage("缺少请求接口path")
                            return contents
                        else:
                            if content["ip_url"] is None or content["ip_url"]=="":
                                contents.setSuccess(False)
                                contents.setMessage("缺少请求地址")
                                return contents
                            else:
                                url=content["ip_url"]+content["webapi_path"]
                    else:
                        if content["webapi_path"] is None or content["webapi_path"] == "":
                            contents.setSuccess(False)
                            contents.setMessage("缺少请求接口path")
                            return contents
                        else:
                            url = environment["pre_url"] + content["webapi_path"]

                    if environment["headers"] is None or environment["headers"]=="":
                        if content["headers"] is None or content["headers"]=="":
                            headers={}
                            headers.setdefault("content-type", contentType)
                        else:
                            header = content["headers"]
                            headers = eval(header)
                            headers.setdefault("content-type", contentType)
                    else:
                        header=environment["headers"]
                        headers = eval(header)
                        headers.setdefault("content-type", contentType)
                else:
                    if content["webapi_path"] is None or content["webapi_path"] == "":
                        contents.setSuccess(False)
                        contents.setMessage("缺少请求接口path")
                        return contents
                    else:
                        if content["ip_url"] is None or content["ip_url"] == "":
                            contents.setSuccess(False)
                            contents.setMessage("缺少请求地址")
                            return contents
                        else:
                            url = content["ip_url"] + content["webapi_path"]
                    if content["headers"] is None or content["headers"]=="":
                        headers={}
                        headers.setdefault("content-type", contentType)
                    else:
                        header=content["headers"]
                        headers=eval(header)
                        headers.setdefault("content-type", contentType)

                requestUtil = RequestBase(url=url, method=method,data=data,headers=headers)
                response = requestUtil.httpRequest(url=url, method=method,data=data,headers=headers)
                tmpArgs={}
                tmpArgs[content["step_name"]]= response.text
                message.append(tmpArgs)
            logger.error(message)
            contents.setSuccess(True)
            contents.setMessage(message)
            contents.setStatusCode(200)
        else:
            contents.setSuccess(False)
            contents.setMessage("获取用例内容失败")
        return contents

    def startTaskByBatchCase(self,args):
        logger.info(args)
        isSuccess = True
        dataResult = DataResult()
        getCaseIds = TestCaseDaoInterface().getCaseIds(args)
        if getCaseIds.getSuccess():
            if len(getCaseIds.getMessage()) > 0:
                caseIds = getCaseIds.getMessage()
                for caseId in caseIds:
                    # caseId.setdefault("envName", args["envName"])
                    # dataResult = self.startTaskBySingleCase(caseId)
                    contents = CaseContentDaoInterface().getContentInfosByCaseId(caseId)
                    caseResult = {}
                    caseName = TestCaseDaoInterface().getCaseInfosById(caseId)
                    caseResult.setdefault("caseName",caseName.getMessage()[0]["name"])
                    caseResult.setdefault("caseId", caseId["caseId"])
                    caseResult.setdefault("instanceId", 0)
                    message = []
                    exec_start = time.time()
                    caseResult.setdefault("exec_start", exec_start)
                    if contents.getSuccess():
                        for content in contents.getMessage():
                            if int(content["method"]) == 0:
                                method = "GET"
                            else:
                                method = "POST"
                            if int(content["content_type"]) == 0:
                                contentType = "application/json"
                                if content["requests_params"] is None or content["requests_params"] == "":
                                    data = {}
                                else:
                                    data = eval(content["requests_params"])
                                    data = json.dumps(data)
                            else:
                                contentType = "application/x-www-form-urlencoded"
                                if content["requests_params"] is None or content["requests_params"] == "":
                                    data = {}
                                else:
                                    data = eval(content["requests_params"])
                                    data = data
                            if len(args["envName"]) > 0:
                                environments = EnvironmentDaoInterface().getEnvironmentInfoByName(args)
                                environment = environments.getMessage()[0]
                                if environment["pre_url"] is None or environment["pre_url"] == "":
                                    if content["webapi_path"] is None or content["webapi_path"] == "":
                                        logger.info("缺少接口path")
                                        continue
                                    else:
                                        if content["ip_url"] is None or content["ip_url"] == "":
                                            logger.info("缺少请求地址")
                                            continue
                                        else:
                                            url = content["ip_url"] + content["webapi_path"]
                                else:
                                    if content["webapi_path"] is None or content["webapi_path"] == "":
                                        logger.info("缺少接口path")
                                        continue
                                    else:
                                        url = environment["pre_url"] + content["webapi_path"]

                                if environment["headers"] is None or environment["headers"] == "":
                                    if content["headers"] is None or content["headers"] == "":
                                        headers = {}
                                        headers.setdefault("content-type", contentType)
                                    else:
                                        header = content["headers"]
                                        headers = eval(header)
                                        headers.setdefault("content-type", contentType)
                                else:
                                    header = environment["headers"]
                                    headers = eval(header)
                                    headers.setdefault("content-type", contentType)
                            else:
                                if content["webapi_path"] is None or content["webapi_path"] == "":
                                    logger.info("缺少接口path")
                                    continue
                                else:
                                    if content["ip_url"] is None or content["ip_url"] == "":
                                        logger.info("缺少请求地址")
                                        continue
                                    else:
                                        url = content["ip_url"] + content["webapi_path"]
                                if content["headers"] is None or content["headers"] == "":
                                    headers = {}
                                    headers.setdefault("content-type", contentType)
                                else:
                                    header = content["headers"]
                                    headers = eval(header)
                                    headers.setdefault("content-type", contentType)
                            requestUtil = RequestBase(url=url, method=method, data=data, headers=headers)
                            response = requestUtil.httpRequest(url=url, method=method, data=data, headers=headers)
                            tmpArgs = {}
                            tmpArgs[content["step_name"]] = response.text
                            tmpArgs["status_code"]=response.status_code
                            tmpArgs["elapsed_ms"]=response.elapsed.microseconds / 1000.0
                            message.append(tmpArgs)
                            if response.status_code == 200:
                                #此处需要验证用户自定义断言
                                caseResult.setdefault("exe_status", "success")
                            else:
                                caseResult.setdefault("exe_status", "fail")
                                isSuccess=False
                        caseResult.setdefault("message",str(message))
                        caseResult.setdefault("runtime", (time.time()-exec_start)*1000)
                        logger.info(caseResult)
                        createCaseResult=CaseResultDaoInterface().addCaseResult(caseResult)
                        logger.info(createCaseResult.getSuccess())
                        logger.info(createCaseResult.getMessage())
            else:
                dataResult.setMessage("项目中无可执行的用例")
                isSuccess = False
        else:
            dataResult.setMessage("获取用例失败")
            isSuccess = False
        if isSuccess:
            args["status"] = 2
        else:
            args["status"] = 3
        TestCaseInstanceDaoInterface().updateTestInstanceStatus(args)
        return dataResult
