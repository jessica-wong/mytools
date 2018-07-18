
# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.TestCaseMapper import TestCaseSQLMapper

#set log
logger = Log('TestCaseDao')
logger.write_to_file(SystemConfig.logPathPrefix+"TestCaseDao.log")

class TestCaseDaoInterface:

    def addTestCase(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = TestCaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def newInsertTestCase(self):
        logger.info(inspect.stack()[0][3])
        sql = TestCaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql)
        return daoOperate.read()

    def addTestCaseContent(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestCaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def addTestCaseAssert(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestCaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getCaseInfosByCondition(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = TestCaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def deleteTestCase(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestCaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def updateTestCase(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestCaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getCaseInfosById(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = TestCaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def getInitCaseInfoByIds(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = TestCaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def getCaseDetailInfoById(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = TestCaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def getTestCaseCount(self):
        logger.info(inspect.stack()[0][3])
        sql = TestCaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql)
        return daoOperate.read()

    def getCaseList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestCaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql,args)
        return daoOperate.read()

    def searchCaseByName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TestCaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()
