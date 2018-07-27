# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.UserDao import UserDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('UserServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"UserServiceImpl.log")

class UserService(object):

    def __init__(self):
        self.userDaoInterface = UserDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addUser(self,args):
        logger.error(args)
        logger.error(type(args))
        return self.userDaoInterface.addUser(args)

    @AdminDecoratorServer.execImplDecorator()
    def getUserInfo(self,userName):
        args={}
        #此处的user_name必须与sql定义中参数一致，即 %(user_name)s
        args.setdefault("userName",userName)
        return self.userDaoInterface.getUserInfo(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteUser(self,args):
        return self.userDaoInterface.deleteUser(args)

    @AdminDecoratorServer.execImplDecorator()
    def getUserInfoById(self,id):
        args={}
        #此处的user_name必须与sql定义中参数一致，即 %(user_name)s
        args.setdefault("userId",id)
        return self.userDaoInterface.getUserInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteUserInfoByName(self,args):
        return self.userDaoInterface.deleteUserInfoByName(args)

    @AdminDecoratorServer.execImplDecorator()
    def getUserList(self):
        return self.userDaoInterface.getUserList()

    def getUserByUnionid(self,unionid):
        args={}
        args.setdefault("unionid", unionid)
        return self.userDaoInterface.getUserByUnionid(args)

    def getCurrentUser(self,userId):
        args={}
        args.setdefault("userId", userId)
        logger.info(args)
        return self.userDaoInterface.getCurrentUser(args)

    def getUserCount(self):
        return self.userDaoInterface.getUserCount()

    def getCurrentUserIsleader(self,userId):
        args = {}
        args.setdefault("userId", userId)
        logger.info(args)
        return self.userDaoInterface.getCurrentUserIsleader(args)