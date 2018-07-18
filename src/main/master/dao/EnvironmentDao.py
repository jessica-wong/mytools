# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.EnvironmentMapper import EnvironmentSQLMapper

#set log
logger = Log('EnvironmentDao')
logger.write_to_file(SystemConfig.logPathPrefix+"EnvironmentDao.log")

class EnvironmentDaoInterface:

    def addEnvironmentItem(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = EnvironmentSQLMapper().getSQL(inspect.stack()[0][3])
        logger.error(sql)
        logger.error(args)
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getEnvironmentInfoById(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = EnvironmentSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def deleteEnvironmentItem(self,args):
        logger.info(inspect.stack()[0][3])
        sql = EnvironmentSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editEnvironmentItem(self,args):
        logger.info(inspect.stack()[0][3])
        sql = EnvironmentSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getEnvironmentInfos(self):
        logger.info(inspect.stack()[0][3])
        sql = EnvironmentSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql)
        return daoOperate.read()

    def getEnvironmentInfosByUserId(self,args):
        logger.info(inspect.stack()[0][3])
        sql = EnvironmentSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql,args)
        return daoOperate.read()