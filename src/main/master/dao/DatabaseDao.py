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
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def deleteDatabase(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getDatabaseInfoById(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getDatabaseAllInfoById(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getDatabasePwdById(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getDatabaseList(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def editDatabase(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editDatabasePwdById(self, args):
        logger.info(inspect.stack()[0][3])
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()
    
    def addTableGroup(self,args,is_execute_many=False):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args,is_execute_many)
        return daoOperate.write()

    def deleteTableGroup(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getTableGroupInfoById(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getTableGroupInfoByName(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getTableGroupList(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def editTableGroup(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def addTableGroupRelation(self,args,is_execute_many=False):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args,is_execute_many)
        return daoOperate.write()

    def deleteTableGroupRelation(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getTableGroupRelationList(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def updateTableGroupRelation(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def updateTableGroupRelationByGroupId(self,args):
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
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args,is_execute_many)
        return daoOperate.write()

    def deleteTable(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getTableInfoById(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getTableInfoByName(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getTableList(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def editTable(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editTableByName(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editTableCNameById(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editTableRemarkById(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def discardTableByName(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def addColumn(self,args,is_execute_many=False):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args,is_execute_many)
        return daoOperate.write()

    def deleteColumn(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getColumnInfoById(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getColumnInfoByEname(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getIdColumnInfoByTableName(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getIdColumnListByTableName(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getColumnListByTableId(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getColumnListByTableName(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def editColumn(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editColumnRemarkById(self,args, is_execute_many):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        logger.info(sql)
        daoOperate = DbBaseHelper(sql, args, is_execute_many)
        return daoOperate.write()

    def editColumnTypeById(self,args, is_execute_many):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args, is_execute_many)
        return daoOperate.write()

    def editColumnDiscardById(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editColumnHideById(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def editColumnUnlinkById(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def isInitSynchronize(self, args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getSynchronizeDatabase(self, args, **kwargs):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read(**kwargs)

    def getSynchronizeTable(self, args, **kwargs):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read(**kwargs)

    def getSynchronizeColumn(self, args, **kwargs):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read(**kwargs)

    def getTableComment(self, args, **kwargs):
        
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read(**kwargs)

    def initSynchronizeDatabase(self, args):
        #  todo 没有sql
        daoOperate = DbBaseHelper()
        return daoOperate.read()

    def SynchronizeDatabase(self, args):
        #  todo 没有sql
        daoOperate = DbBaseHelper()
        return daoOperate.read()

    def getSearchByTable(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getSearchByTableColumn(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getSearchByColumn(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getSearchByColumnRemark(self,args):
        
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def addDBLog(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getDBLogList(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def addColumnLink(self,args,is_execute_many=False):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args, is_execute_many)
        return daoOperate.write()

    def deleteColumnLink(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getDBLogList(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getLinkTableList(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getLinkColumnList(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getTableListByTableName(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getColumnListByColName(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def addTableRoute(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def addDataNode(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def addDataRoute(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getTableRouteList(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getViewLinks(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getViewTableInfo(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getViewLinksByGroup(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getViewTableInfoByGroup(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getViewTableByGroup(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getViewTableInfoByGroup(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getViewLinksByGroup(self,args):
        sql = DatabaseSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()


