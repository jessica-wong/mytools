# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.TestSuiteMapper import TestSuiteSQLMapper

#set log
logger = Log('TestSuiteDao')
logger.write_to_file(SystemConfig.logPathPrefix+"TestSuiteDao.log")

class TestSuiteDaoInterface:

    def addTestSuite(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestSuiteSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getSuiteInfoById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestSuiteSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def updateTestSuite(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestSuiteSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def deleteTestSuite(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestSuiteSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getSuiteList(self):
        logger.info(inspect.stack()[0][3])
        sql = TestSuiteSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql)
        return daoOperate.read()

    def editTestSuiteName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestSuiteSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()