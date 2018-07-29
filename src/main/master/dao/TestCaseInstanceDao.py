# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.TestCaseInstanceMapper import TestInstanceSQLMapper

#set log
logger = Log('TestCaseInstanceDao')
logger.write_to_file(SystemConfig.logPathPrefix+"TestCaseInstanceDao.log")

class TestCaseInstanceDaoInterface:

    def addTestInstance(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestInstanceSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getTestInstanceInfoById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestInstanceSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def updateTestInstance(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestInstanceSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getPengdingInstanceInfos(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestInstanceSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def updateTestInstanceStatus(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestInstanceSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getTaskInstanceInfos(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestInstanceSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()
