# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.WebApiMapper import WebApiSQLMapper

#set log
logger = Log('WebApiDao')
logger.write_to_file(SystemConfig.logPathPrefix+"WebApiDao.log")

class WebApiDaoInterface:

    def addWebApi(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = WebApiSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getWebApiForVersion(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = WebApiSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def deleteWebApi(self,args):
        logger.info(inspect.stack()[0][3])
        sql = WebApiSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def updateWebApi(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = WebApiSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getWebApiInfoById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = WebApiSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getWebApiList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = WebApiSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getWebApiRequest(self,args):
        logger.info(inspect.stack()[0][3])
        sql = WebApiSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getWebApiResponse(self,args):
        logger.info(inspect.stack()[0][3])
        sql = WebApiSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getWebApiInfoByPath(self,args):
        logger.info(inspect.stack()[0][3])
        sql = WebApiSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()