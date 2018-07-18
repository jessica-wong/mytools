# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.CaseResultMapper import CaseResultSQLMapper

#set log
logger = Log('CaseResultDao')
logger.write_to_file(SystemConfig.logPathPrefix+"CaseResultDao.log")

class CaseResultDaoInterface:

    def addCaseResult(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = CaseResultSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getCaseResultInfoByCaseId(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = CaseResultSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def deleteCaseResult(self,args):
        logger.info(inspect.stack()[0][3])
        sql = CaseResultSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def updateCaseResult(self,args):
        logger.info(inspect.stack()[0][3])
        sql = CaseResultSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getCaseResultInfosByCondition(self,args):
        logger.info(inspect.stack()[0][3])
        sql = CaseResultSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()
