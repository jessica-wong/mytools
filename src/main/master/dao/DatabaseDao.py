# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.DatabaseMapper import DatabaseSQLMapper

#set log
logger = Log('DatabaseDao')
logger.write_to_file(SystemConfig.logPathPrefix+"DatabaseDao.log")

class DatabaseDaoInterface:

    def addDatabase(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def deleteDatabase(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getDatabaseInfoById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getDatabaseAllInfoById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getDatabasePwdById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getDatabaseList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def editDatabase(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editDatabasePwdById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def addTableGroup(self,args,is_execute_many=False):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args,is_execute_many)
        return daoOperate.write()

    def deleteTableGroup(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getTableGroupInfoById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getTableGroupInfoByName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getTableGroupList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def editTableGroup(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def addTableGroupRelation(self,args,is_execute_many=False):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args,is_execute_many)
        return daoOperate.write()

    def deleteTableGroupRelation(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getTableGroupRelationList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def updateTableGroupRelation(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def updateTableGroupRelationByGroupId(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def deleteTableGroupByDB(self, args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def deleteTableGroupRelationByDB(self, args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()
    
    def addTable(self,args,is_execute_many=False):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args,is_execute_many)
        return daoOperate.write()

    def deleteTable(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getTableInfoById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getTableInfoByName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getTableList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def editTable(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editTableByName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editTableCNameById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editTableRemarkById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def discardTableByName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def addColumn(self,args,is_execute_many=False):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args,is_execute_many)
        return daoOperate.write()

    def deleteColumn(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getColumnInfoById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getColumnInfoByEname(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getIdColumnInfoByTableName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getIdColumnListByTableName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getColumnListByTableId(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getColumnListByTableName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def editColumn(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editColumnRemarkById(self,args, is_execute_many):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        logger.info(sql)
        daoOperate = DbBaseHelper(sql, args, is_execute_many)
        return daoOperate.write()

    def editColumnTypeById(self,args, is_execute_many):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args, is_execute_many)
        return daoOperate.write()

    def editColumnDiscardById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editColumnHideById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editColumnUnlinkById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def isInitSynchronize(self, args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getSynchronizeDatabase(self, args, **kwargs):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read(**kwargs)

    def getSynchronizeTable(self, args, **kwargs):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read(**kwargs)

    def getSynchronizeColumn(self, args, **kwargs):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read(**kwargs)

    def getTableComment(self, args, **kwargs):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read(**kwargs)

    def initSynchronizeDatabase(self, args):
        #  todo 没有sql
        logger.info(inspect.stack()[0][3])
        daoOperate = DbBaseHelper()
        return daoOperate.read()

    def SynchronizeDatabase(self, args):
        #  todo 没有sql
        logger.info(inspect.stack()[0][3])
        daoOperate = DbBaseHelper()
        return daoOperate.read()

    def getSearchByTable(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getSearchByTableColumn(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getSearchByColumn(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getSearchByColumnRemark(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def addDBLog(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getDBLogList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def addColumnLink(self,args,is_execute_many=False):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args, is_execute_many)
        return daoOperate.write()

    def deleteColumnLink(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getDBLogList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getLinkTableList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getLinkColumnList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getTableListByTableName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getColumnListByColName(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def addTableRoute(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def addDataNode(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def addDataRoute(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getTableRouteList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getViewLinks(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getViewTableInfo(self,args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()


