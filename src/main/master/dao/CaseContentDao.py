# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.CaseContentMapper import CaseContentSQLMapper

#set log
logger = Log('CaseContentDao')
logger.write_to_file(SystemConfig.logPathPrefix+"CaseContentDao.log")

class CaseContentDaoInterface:

    def addCaseContent(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = CaseContentSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getContentInfosByCaseId(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = CaseContentSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def deleteTestContentByContentId(self,args):
        logger.info(inspect.stack()[0][3])
        sql = CaseContentSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def deleteTestContentByCaseId(self,args):
        logger.info(inspect.stack()[0][3])
        sql = CaseContentSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def updateTestContent(self,args):
        logger.info(inspect.stack()[0][3])
        sql = CaseContentSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getContentInfosByContentId(self,args):
        logger.info(inspect.stack()[0][3])
        sql = CaseContentSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()
