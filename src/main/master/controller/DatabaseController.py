# -*- coding: utf-8 -*-

import json
import traceback
import tornado.web
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.util.commonUtil.commonToolUtil import CommonTool
from src.main.master.common.errCodeManage import DBErrCode
from src.main.master.entity.DataResult import DataResult
from src.main.master.service.impl.DatabaseServiceImpl import DatabaseService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('DatabaseController')
logger.write_to_file(SystemConfig.logPathPrefix+"DatabaseController.log")

class DatabaseHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(30)

    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request)
        self.application = application
        self.request = request

        self.commonTool = CommonTool()
        self.errCode = DBErrCode()

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,APIName):
        yield self.execute_get(APIName)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self,APIName):
        yield self.execute_post(APIName)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Authorization,Origin,x-requested-with,Content-Type, Accept")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self,APIName):
        # no body
        self.set_status(204)
        self.finish()

    @run_on_executor
    def execute_get(self,APIName):
        dataResult = DataResult()
        try:
            tasks = {
                'getDatabaseInfoById': lambda: self.getDatabaseInfoById(),
                'getDatabaseList':lambda :self.getDatabaseList(),
                'getTableGroupInfoById': lambda: self.getTableGroupInfoById(),
                'getTableGroupList': lambda: self.getTableGroupList(),
                'getTableGroupRelationList': lambda: self.getTableGroupRelationList(),
                'getTableInfoById': lambda: self.getTableInfoById(),
                'getTableList': lambda: self.getTableList(),
                'getColumnInfoById': lambda: self.getColumnInfoById(),
                'getColumnListByTableId': lambda: self.getColumnListByTableId(),
                'isInitSynchronize': lambda: self.isInitSynchronize(),
                'getDBLogList': lambda: self.getDBLogList(),
                'getLinkTableList': lambda: self.getLinkTableList(),
                'getLinkColumnList': lambda: self.getLinkColumnList(),
                'getViewLinks': lambda: self.getViewLinks(),
                # lambda alias
            }
            self.write(json.dumps(tasks[APIName]().__dict__,cls=CJsonEncoder))
        except:
            logger.error(traceback.format_exc())
            dataResult.setMessage(traceback.format_exc())
            dataResult.setSuccess(False)
            dataResult.setStatusCode(500)
            self.write(json.dumps(dataResult.__dict__))
        finally:
            try:
                self.finish()
            except:
                pass

    @run_on_executor
    def execute_post(self,APIName):
        dataResult = DataResult()
        try:
            tasks = {
                'addDatabase' : lambda : self.addDatabase(),
                'deleteDatabase':lambda :self.deleteDatabase(),
                'editDatabase':lambda :self.editDatabase(),
                'addTableGroup': lambda: self.addTableGroup(),
                'deleteTableGroup': lambda: self.deleteTableGroup(),
                'editTableGroup': lambda: self.editTableGroup(),
                'addTableGroupRelation': lambda: self.addTableGroupRelation(),
                'deleteTableGroupRelation': lambda: self.deleteTableGroupRelation(),
                'updateTableGroupRelation': lambda: self.updateTableGroupRelation(),
                'getTableInfoByName': lambda: self.getTableInfoByName(),
                'addTable': lambda: self.addTable(),
                'deleteTable': lambda: self.deleteTable(),
                'editTable': lambda: self.editTable(),
                'editTableByName': lambda: self.editTableByName(),
                'discardTableByName': lambda: self.discardTableByName(),
                'getColumnListByTableName': lambda: self.getColumnListByTableName(),
                'addColumn': lambda: self.addColumn(),
                'deleteColumn': lambda: self.deleteColumn(),
                'editColumn': lambda: self.editColumn(),
                'initSynchronizeDatabase': lambda: self.initSynchronizeDatabase(),
                'synchronizeDatabase': lambda: self.synchronizeDatabase(),
                'initSynchronizeTable': lambda: self.initSynchronizeTable(),
                'initSynchronizeColumn': lambda: self.initSynchronizeColumn(),
                'editColumnRemarkById': lambda: self.editColumnRemarkById(),
                'editColumnDiscardById': lambda: self.editColumnDiscardById(),
                'editColumnHideById': lambda: self.editColumnHideById(),
                'editColumnUnlinkById': lambda: self.editColumnUnlinkById(),
                'getSearchByTable': lambda: self.getSearchByTable(),
                'getSearchByTableColumn': lambda: self.getSearchByTableColumn(),
                'getSearchByColumn': lambda: self.getSearchByColumn(),
                'getSearchByColumnRemark': lambda: self.getSearchByColumnRemark(),
                'addColumnLink': lambda: self.addColumnLink(),
                'deleteColumnLink': lambda: self.deleteColumnLink(),
                'getTableListByTableName': lambda: self.getTableListByTableName(),
                'getColumnListByColName': lambda: self.getColumnListByColName(),
                'updateComment': lambda: self.updateComment(),
                'editTableRemarkById': lambda: self.editTableRemarkById(),
                'addLinkByMatchRule': lambda: self.addLinkByMatchRule(),
            }
            self.write(json.dumps(tasks[APIName]().__dict__,cls=CJsonEncoder))
        except:
            logger.error(traceback.format_exc())
            dataResult.setMessage(traceback.format_exc())
            dataResult.setSuccess(False)
            dataResult.setStatusCode(500)
            self.write(json.dumps(dataResult.__dict__))
        finally:
            try:
                self.finish()
            except:
                pass

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addDatabase(self):
        logger.info(self.request.body)
        data = json.loads(self.request.body)
        #数据库该字段可为空,入参没有时,需要补充key,否则访问sql
        result = DataResult()
        if self.commonTool.is_none_str(data["name"]):
            result.setMessage(self.errCode.NONE_DB_CONN_NAME)
            return result
        if self.commonTool.is_none_str(data["host"]):
            result.setMessage(self.errCode.NONE_DB_HOST)
            return result
        if self.commonTool.is_zero(data["port"]):
            result.setMessage(self.errCode.NONE_DB_PORT)
            return result
        if self.commonTool.is_none_str(data["username"]):
            result.setMessage(self.errCode.NONE_DB_USERNAME)
            return result
        if self.commonTool.is_none_str(data["password"]):
            result.setMessage(self.errCode.NONE_DB_PSD)
            return result
        if self.commonTool.is_none_str(data["schema_name"]):
            result.setMessage(self.errCode.NONE_DB_SCHEMAA)
            return result
        return DatabaseService().addDatabase(data)

    def getDatabaseInfoById(self):
        db_id= self.get_argument("id")
        return DatabaseService().getDatabaseInfoById(db_id)

    def getDatabaseList(self):
        # todo 后面传了bu的Id
        business_unit = self.get_argument("id")
        return DatabaseService().getDatabaseList(business_unit)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteDatabase(self):
        return DatabaseService().deleteDatabase(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editDatabase(self):
        data = json.loads(self.request.body)
        result = DataResult()
        if self.commonTool.is_none_str(data["name"]):
            result.setMessage(self.errCode.NONE_DB_CONN_NAME)
            return result
        if self.commonTool.is_none_str(data["host"]):
            result.setMessage(self.errCode.NONE_DB_HOST)
            return result
        if self.commonTool.is_zero(data["port"]):
            result.setMessage(self.errCode.NONE_DB_PORT)
            return result
        if self.commonTool.is_none_str(data["username"]):
            result.setMessage(self.errCode.NONE_DB_USERNAME)
            return result
        if self.commonTool.is_none_str(data["password"]):
            result.setMessage(self.errCode.NONE_DB_PSD)
            return result
        if self.commonTool.is_none_str(data["schema_name"]):
            result.setMessage(self.errCode.NONE_DB_SCHEMAA)
            return result
        if self.commonTool.is_zero(data["id"]):
            result.setMessage(self.errCode.NONE_DB_ID)
            return result
        return DatabaseService().editDatabase(data)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addTableGroup(self):
        data = json.loads(self.request.body)
        result = DataResult()
        if self.commonTool.is_none_str(data["name"]):
            result.setMessage(self.errCode.NONE_DB_NAME)
            return result
        if self.commonTool.is_zero(data["db_id"]):
            result.setMessage(self.errCode.NONE_DB_ID)
            return result
        return DatabaseService().addTableGroup(data)

    def getTableGroupInfoById(self):
        table_group_id = self.get_argument("id")
        return DatabaseService().getTableGroupInfoById(table_group_id)

    def getTableGroupList(self):
        db_id = self.get_argument("id")
        return DatabaseService().getTableGroupList(db_id)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteTableGroup(self):
        data = json.loads(self.request.body)
        result = DataResult()
        if self.commonTool.is_zero(data["define"]):
            result.setMessage(self.errCode.NOT_DEL_GROUP)
            return result
        return DatabaseService().deleteTableGroup(data)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editTableGroup(self):
        data = json.loads(self.request.body)
        result = DataResult()
        if self.commonTool.is_none_str(data["name"]):
            result.setMessage(self.errCode.NONE_DB_NAME)
            return result
        if self.commonTool.is_zero(data["db_id"]):
            result.setMessage(self.errCode.NONE_DB_ID)
            return result
        if self.commonTool.is_zero(data["id"]):
            result.setMessage(self.errCode.NONE_GROUP_ID)
            return result
        if self.commonTool.is_zero(data["define"]):
            result.setMessage(self.errCode.NOT_EDIT_GROUP)
            return result
        return DatabaseService().editTableGroup(data)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addTableGroupRelation(self):
        data = json.loads(self.request.body)
        result = DataResult()
        if self.commonTool.is_zero(args["table_id"]):
            result.setMessage(self.errCode.NONE_TABLE_ID)
            return result
        if self.commonTool.is_zero(args["group_id"]):
            result.setMessage(self.errCode.NONE_GROUP_ID)
            return result
        return DatabaseService().addTableGroupRelation(data)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteTableGroupRelation(self):
        relation_id = self.get_argument("id")
        return DatabaseService().deleteTableGroupRelation(relation_id)

    def getTableGroupRelationList(self):
        relation_id = self.get_argument("id")
        return DatabaseService().getTableGroupRelationList(relation_id)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def updateTableGroupRelation(self):
        data = json.loads(self.request.body)
        result = DataResult()
        if self.commonTool.is_zero(data["db_id"]):
            result.setMessage(self.errCode.NONE_DB_ID)
            return result
        if self.commonTool.is_zero(data["group_id"]):
            result.setMessage(self.errCode.NONE_GROUP_ID)
            return result
        if self.commonTool.is_none_list(data["tables"]):
            result.setMessage(self.errCode.NONE_TABLE_ID)
            return result
        return DatabaseService().updateTableGroupRelation(data)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addTable(self):
        data = json.loads(self.request.body)
        result = DataResult()
        if self.commonTool.is_zero(data["db_id"]):
            result.setMessage(self.errCode.NONE_DB_ID)
            return result
        if self.commonTool.is_none_str(data["e_name"]):
            result.setMessage(self.errCode.NONE_TABLE_E_NAME)
            return result
        return DatabaseService().addTable(data)

    def getTableInfoById(self):
        table_id = self.get_argument("id")
        return DatabaseService().getTableInfoById(table_id)

    def getTableInfoByName(self):
        data = json.loads(self.request.body)
        return DatabaseService().getTableInfoByName(data)

    def getTableList(self):
        db_id = self.get_argument("id")
        return DatabaseService().getTableList(db_id)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteTable(self):
        return DatabaseService().deleteTable(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editTable(self):
        data = json.loads(self.request.body)
        result = DataResult()
        if self.commonTool.is_zero(data["db_id"]):
            result.setMessage(self.errCode.NONE_DB_ID)
            return result
        if self.commonTool.is_none_str(data["e_name"]):
            result.setMessage(self.errCode.NONE_TABLE_E_NAME)
            return result
        return DatabaseService().editTable(data)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editTableByName(self):
        data = json.loads(self.request.body)
        result = DataResult()
        if self.commonTool.is_zero(data["db_id"]):
            result.setMessage(self.errCode.NONE_DB_ID)
            return result
        if self.commonTool.is_none_str(data["e_name"]):
            result.setMessage(self.errCode.NONE_TABLE_E_NAME)
            return result
        return DatabaseService().editTableByName(data)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def discardTableByName(self):
        return DatabaseService().discardTableByName(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addColumn(self):
        data = json.loads(self.request.body)
        result = DataResult()
        if self.commonTool.is_zero(data["table_id"]):
            result.setMessage(self.errCode.NONE_TABLE_ID)
            return result
        if self.commonTool.is_none_str(data["e_name"]):
            result.setMessage(self.errCode.NONE_COL_E_NAME)
            return result
        return DatabaseService().addColumn(data)

    def getColumnInfoById(self):
        column_id = self.get_argument("id")
        return DatabaseService().getTableInfoById(column_id)

    def getColumnListByTableId(self):
        table_id = self.get_argument("id")
        return DatabaseService().getColumnListByTableId(table_id)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def getColumnListByTableName(self):
        return DatabaseService().getColumnListByTableName(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteColumn(self):
        return DatabaseService().deleteColumn(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editColumnRemarkById(self):
        data = json.loads(self.request.body)
        result = DataResult()
        if self.commonTool.is_zero(data["table_id"]):
            result.setMessage(self.errCode.NONE_TABLE_ID)
            return result
        if self.commonTool.is_none_str(data["e_name"]):
            result.setMessage(self.errCode.NONE_COL_E_NAME)
            return result
        return DatabaseService().editColumnRemarkById()

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editColumnDiscardById(self):
        return DatabaseService().editColumnDiscardById(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editColumnHideById(self):
        return DatabaseService().editColumnHideById(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editColumnUnlinkById(self):
        return DatabaseService().editColumnUnlinkById(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editColumn(self):
        return DatabaseService().editColumn(json.loads(self.request.body))

    def isInitSynchronize(self):
        db_id = self.get_argument("id")
        return DatabaseService().isInitSynchronize(db_id)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def initSynchronizeDatabase(self):
        return DatabaseService().initSynchronizeDatabase(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def synchronizeDatabase(self):
        return DatabaseService().synchronizeDatabase(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def initSynchronizeTable(self):
        return DatabaseService().initSynchronizeTable(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def initSynchronizeColumn(self):
        return DatabaseService().initSynchronizeColumn(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def getSearchByTable(self):
        return DatabaseService().getSearchByTable(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def getSearchByTableColumn(self):
        return DatabaseService().getSearchByTableColumn(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def getSearchByColumn(self):
        return DatabaseService().getSearchByColumn(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def getSearchByColumnRemark(self):
        return DatabaseService().getSearchByColumnRemark(json.loads(self.request.body))

    def getDBLogList(self):
        db_id = self.get_argument("id")
        return DatabaseService().getDBLogList(db_id)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def addColumnLink(self):
        data = json.loads(self.request.body)
        result = DataResult()
        if self.commonTool.is_zero(data["src_column_id"]):
            result.setMessage(self.errCode.NONE_COL_SRC)
            return result
        if self.commonTool.is_zero(data["link_column_id"]):
            result.setMessage(self.errCode.NONE_COL_DEST)
            return result
        if self.commonTool.is_zero(data["src_table_id"]):
            result.setMessage(self.errCode.NONE_TABLE_SRC)
            return result
        if self.commonTool.is_zero(data["link_table_id"]):
            result.setMessage(self.errCode.NONE_TABLE_DEST)
            return result
        if self.commonTool.is_zero(data["relation_type"]):
            result.setMessage(self.errCode.NONE_LINK_TYPE)
            return result
        return DatabaseService().addColumnLink(data)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteColumnLink(self):
        return DatabaseService().deleteColumnLink(json.loads(self.request.body))

    def getLinkTableList(self):
        db_id = self.get_argument("id")
        return DatabaseService().getLinkTableList(db_id)

    def getLinkColumnList(self):
        table_id = self.get_argument("id")
        return DatabaseService().getLinkColumnList(table_id)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def getTableListByTableName(self):
        data = json.loads(self.request.body)
        return DatabaseService().getTableListByTableName(data)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def getColumnListByColName(self):
        data = json.loads(self.request.body)
        return DatabaseService().getColumnListByColName(data)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def updateComment(self):
        data = json.loads(self.request.body)
        return DatabaseService().updateComment(data)

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editTableRemarkById(self):
        data = json.loads(self.request.body)
        return DatabaseService().editTableRemarkById(data)

    def getViewLinks(self):
        table_id = self.get_argument("id")
        return DatabaseService().getViewLinks(table_id)

    def addLinkByMatchRule(self):
        data = json.loads(self.request.body)
        return DatabaseService().addLinkByMatchRule(data)
