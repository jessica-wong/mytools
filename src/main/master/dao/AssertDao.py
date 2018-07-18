# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.AssertMapper import AssertSQLMapper

#set log
logger = Log('AssertDao')
logger.write_to_file(SystemConfig.logPathPrefix+"AssertDao.log")

class AssertDaoInterface:

    def addAssert(self,args):
        logger.info(inspect.stack()[0][3])
        sql = AssertSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getAssertInfosByContentId(self,args):
        logger.info(inspect.stack()[0][3])
        sql = AssertSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def deleteAssert(self,args):
        logger.info(inspect.stack()[0][3])
        sql = AssertSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def updateAssert(self,args):
        logger.info(inspect.stack()[0][3])
        sql = AssertSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getAssertInfoById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = AssertSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def deleteAssertByContentId(self,args):
        logger.info(inspect.stack()[0][3])
        sql = AssertSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()