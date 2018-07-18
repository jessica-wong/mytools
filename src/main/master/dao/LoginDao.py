# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.LoginMapper import LoginSQLMapper

#set log
logger = Log('LoginDao')
logger.write_to_file(SystemConfig.logPathPrefix+"LoginDao.log")

class LoginDaoInterface:

    def getUserInfo(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = LoginSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()
