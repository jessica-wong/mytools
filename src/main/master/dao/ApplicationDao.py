# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.ApplicationMapper import ApplicationSQLMapper

#set log
logger = Log('ApplicationDao')
logger.write_to_file(SystemConfig.logPathPrefix+"ApplicationDao.log")

class ApplicationDaoInterface:

    def addApplication(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = ApplicationSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def addApplicationVersion(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ApplicationSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getApplicationList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ApplicationSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql,args)
        return daoOperate.read()

    def getApplicationListLeader(self):
        logger.info(inspect.stack()[0][3])
        sql = ApplicationSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql)
        return daoOperate.read()

    def getApplicationByProjectId(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = ApplicationSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def getInterfaceCountByApplicationVersion(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = ApplicationSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def deleteApplicationVersion(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ApplicationSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def addApplicationVersionConfig(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ApplicationSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editVersionConfig(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ApplicationSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getVersionConfig(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ApplicationSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getApplicationCountByProject(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ApplicationSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getApplicationCount(self):
        logger.info(inspect.stack()[0][3])
        sql = ApplicationSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql)
        return daoOperate.read()

    def getApplicationById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ApplicationSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql,args)
        return daoOperate.read()

    def editApplication(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ApplicationSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        logger.info(sql)
        logger.info(args)
        return daoOperate.write()

    def deleteApplication(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ApplicationSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()