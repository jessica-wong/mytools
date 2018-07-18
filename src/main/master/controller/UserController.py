# -*- coding: utf-8 -*-

import json
import traceback
import tornado.web
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.service.impl.UserServiceImpl import UserService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer
import requests

#set log
logger = Log('UserController')
logger.write_to_file(SystemConfig.logPathPrefix+"UserController.log")

class UserHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(30)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,APIName):
        yield self.execute_get(APIName)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self,APIName):
        yield self.execute_post(APIName)

    @run_on_executor
    def execute_get(self,APIName):
        dataResult = DataResult()
        # try:
        #     if not self.current_user:
        #         dataResult.setSuccess(False)
        #         dataResult.setMessage("目前处于未登录状态，请登录")
        #         self.write(json.dumps(dataResult.__dict__, cls=CJsonEncoder))
        #     else:
        #         tasks = {
        #             'getUserInfo' : lambda : self.getUserInfo(),
        #             'get_user_info_by_user_id' : lambda :self.get_user_info_by_user_id(),
        #             'getUserList' : lambda :self.getUserList()
        #             # lambda alias
        #         }
        #         self.write(json.dumps(tasks[APIName]().__dict__,cls=CJsonEncoder))
        try:
            tasks = {
                'getUserInfo' : lambda : self.getUserInfo(),
                'get_user_info_by_user_id' : lambda :self.get_user_info_by_user_id(),
                'getUserList' : lambda :self.getUserList(),
                'getUserByUnionid' : lambda :self.getUserByUnionid(),
                'getUserDingDingInfo' : lambda :self.getUserDingDingInfo(),
                'getCurrentUser': lambda: self.getCurrentUser(),
                # lambda alias
            }
            self.write(json.dumps(tasks[APIName]().__dict__,cls=CJsonEncoder))
        except:
            logger.error(traceback.format_exc())
            dataResult.setMessage(traceback.format_exc())
            dataResult.setSuccess(False)
            dataResult.setStatusCode(500)
            self.write(json.dumps(dataResult.__dict__))
        finally:
            try:
                self.finish()
            except:
                pass

    @run_on_executor
    def execute_post(self,APIName):
        dataResult = DataResult()
        try:
            tasks = {
                'addUser' : lambda : self.addUser(),
                'delete_user_info':lambda :self.delete_user_info(),
                'deleteUserInfoByName':lambda :self.deleteUserInfoByName(),

            }
            self.write(json.dumps(tasks[APIName]().__dict__,cls=CJsonEncoder))
        except:
            logger.error(traceback.format_exc())
            dataResult.setMessage(traceback.format_exc())
            dataResult.setSuccess(False)
            dataResult.setStatusCode(500)
            self.write(json.dumps(dataResult.__dict__))
        finally:
            try:
                self.finish()
            except:
                pass


    def getUserInfo(self):
        logger.error(self.request.body)
        userName = self.get_argument('userName')
        return UserService().getUserInfo(userName)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addUser(self):
        logger.error(self.request.body)
        data = json.loads(self.request.body)
        #数据库该字段可为空,入参没有时,需要补充key,否则访问sql
        if "userPasswd" not in  data:
            data.setdefault("userPasswd","123456")
        logger.info(data)
        dataResult = UserService().addUser(data)
        self.set_secure_cookie("userName",str(data["userName"]),version=1)
        self.set_secure_cookie("userId",str(dataResult.getMessage()),version=1)
        return dataResult

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def delete_user_info(self):
        return UserService().deleteUser(json.loads(self.request.body))

    def get_user_info_by_user_id(self):
        userId = self.get_argument('userId')
        return UserService().getUserInfoById(userId)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteUserInfoByName(self):
        return UserService().deleteUserInfoByName(json.loads(self.request.body))

    # @tornado.web.authenticated
    def getUserList(self):
        logger.error(self.request.body)
        return UserService().getUserList()

    def getUserByUnionid(self):
        unionid = self.get_argument('unionid')
        logger.info(unionid)
        return UserService().getUserByUnionid(unionid)

    def getUserDingDingInfo(self):
        unionid = self.get_argument('unionid')
        args={}
        args.setdefault("unionid", unionid)
        userInfo=requests.post(url="http://dev2-stpuser.greedyint.com/user/GetDingTalkUserDetail",data=json.dumps(args),headers={"Content-Type":"application/json"})
        dataResult=json.loads(userInfo.text)
        Result=DataResult()
        Result.setSuccess(True)
        Result.setMessage(dataResult)
        logger.info(Result)
        return Result

    def getCurrentUser(self):
        useId = self.get_secure_cookie("userId")
        logger.info(useId)
        return UserService().getCurrentUser(useId)
