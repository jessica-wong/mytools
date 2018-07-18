# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.SessionManageMapper import SessionManageSQLMapper

#set log
logger = Log('SessionManageDao')
logger.write_to_file(SystemConfig.logPathPrefix+"SessionManageDao.log")

class SessionManageDaoInterface:

    def addSession(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = SessionManageSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getSessionInfo(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = SessionManageSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def updateSession(self,args):
        logger.info(inspect.stack()[0][3])
        sql = SessionManageSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()