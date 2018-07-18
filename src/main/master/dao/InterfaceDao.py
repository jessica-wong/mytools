# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.InterfaceMapper import InterfaceSQLMapper

#set log
logger = Log('InterfaceDao')
logger.write_to_file(SystemConfig.logPathPrefix+"InterfaceDao.log")

class InterfaceDaoInterface:

    def addInterfaceItem(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = InterfaceSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getInterfaceInfoById(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = InterfaceSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def deleteInterfaceItem(self,args):
        logger.info(inspect.stack()[0][3])
        sql = InterfaceSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def updateInterfaceItem(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = InterfaceSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def enableInterfaceItem(self,args):
        logger.info(inspect.stack()[0][3])
        sql = InterfaceSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getInterfaceInfosByProject(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = InterfaceSQLMapper().getSQL(inspect.stack()[0][3])
        # logger.error(sql)
        # logger.error(args)
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def disableInterfaceItem(self,args):
        logger.info(inspect.stack()[0][3])
        sql = InterfaceSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def setInterfaceGroup(self,args):
        logger.info(inspect.stack()[0][3])
        sql = InterfaceSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()