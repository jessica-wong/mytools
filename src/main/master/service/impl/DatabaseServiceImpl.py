# -*- coding: utf-8 -*-

import json, itertools
from copy import deepcopy
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.DatabaseDao import DatabaseDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('DatabaseServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"DatabaseServiceImpl.log")

#新建和编辑做非空校验

class DatabaseService(object):

    def __init__(self):
        self.DatabaseDaoInterface = DatabaseDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addDatabase(self,args):
        result = self.DatabaseDaoInterface.addDatabase(args)
        # todo 要处理，用事务,none判断
        # 添加默认表分组
        db_id = result.getMessage()
        group_dict = {}
        group_dict["db_id"] = db_id
        group_dict["name"] = "未分组"
        group_dict["define"] = 0
        group_dict["sort"] = 0
        self.addTableGroup(group_dict)
        return result

    @AdminDecoratorServer.execImplDecorator()
    def deleteDatabase(self, args):
        self.deleteColumn(args)
        self.deleteTableGroupRelationByDB(args)
        self.deleteTableGroupByDB(args)
        self.deleteTable(args)
        return self.DatabaseDaoInterface.deleteDatabase(args)

    @AdminDecoratorServer.execImplDecorator()
    def getDatabaseInfoById(self, db_id):
        args={}
        args.setdefault("id", db_id)
        return self.DatabaseDaoInterface.getDatabaseInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def getDatabaseAllInfoById(self, db_id):
        args = {}
        args.setdefault("id", db_id)
        return self.DatabaseDaoInterface.getDatabaseAllInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def getDatabasePwdById(self, db_id):
        args = {}
        args.setdefault("id", db_id)
        return self.DatabaseDaoInterface.getDatabasePwdById(args)

    @AdminDecoratorServer.execImplDecorator()
    def getDatabaseList(self, business_unit):
        args = {}
        args.setdefault("business_unit", business_unit)
        return self.DatabaseDaoInterface.getDatabaseList(args)

    @AdminDecoratorServer.execImplDecorator()
    def editDatabase(self, args):
        return self.DatabaseDaoInterface.editDatabase(args)

    @AdminDecoratorServer.execImplDecorator()
    def editDatabasePwdById(self, args):
        return self.DatabaseDaoInterface.editDatabasePwdById(args)

    @AdminDecoratorServer.execImplDecorator()
    def confirmDatabasePwdById(self, args):
        result = DataResult()
        bu = args["bu"]
        src_key = args["key"]
        str_bu = ""
        if bu == 1:
            str_bu = "NBU"
        elif bu == 2:
            str_bu = "TBU"
        elif bu == 3:
            str_bu = "IBU"
        key = "{}{}".format(bu, str_bu)
        if key == src_key:
            result.setMessage("秘钥正确")
            result.setSuccess(True)
        else:
            result.setMessage("秘钥错误")
        return result

    @AdminDecoratorServer.execImplDecorator()
    def addTableGroup(self, args):
        return self.DatabaseDaoInterface.addTableGroup(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteTableGroup(self, args):
        #todo 创建事务
        src_group_id = args["id"]
        db_id = args["db_id"]
        name = "未分组"
        dest_group_id = (self.getTableGroupInfoByName(db_id, name).getMessage())[0]["id"]
        self.updateTableGroupRelationByGroupId(src_group_id, dest_group_id)
        return self.DatabaseDaoInterface.deleteTableGroup(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableGroupInfoById(self, group_id):
        args = {}
        args.setdefault("id", group_id)
        return self.DatabaseDaoInterface.getTableGroupInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableGroupInfoByName(self, db_id, name):
        args = {}
        args.setdefault("db_id", db_id)
        args.setdefault("name", name)
        return self.DatabaseDaoInterface.getTableGroupInfoByName(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableGroupList(self, db_id):
        args = {}
        args.setdefault("db_id", db_id)
        return self.DatabaseDaoInterface.getTableGroupList(args)

    @AdminDecoratorServer.execImplDecorator()
    def editTableGroup(self, args):
        return self.DatabaseDaoInterface.editTableGroup(args)

    @AdminDecoratorServer.execImplDecorator()
    def addTableGroupRelation(self, args):
        return self.DatabaseDaoInterface.addTableGroupRelation(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteTableGroupRelation(self, relationId):
        args = {}
        args.setdefault("id", relationId)
        return self.DatabaseDaoInterface.deleteTableGroupRelation(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableGroupRelationList(self, db_id):
        args = {}
        args.setdefault("db_id", db_id)
        result = self.DatabaseDaoInterface.getTableGroupRelationList(args)
        db_name = (self.getDatabaseInfoById(db_id).getMessage())[0]["name"]
        # 先排序再分组，不然会被隔开
        handle_result = sorted(result.getMessage(), key= lambda x: x["sort"])
        handle_result = itertools.groupby(handle_result, key= lambda x: x["sort"])
        end_result = []
        index = 0
        for key, group in handle_result:
            group_dict = {}
            #  先转为list
            group=list(group)
            group_dict.setdefault("title", group[0]["name"])
            group_dict.setdefault("id", group[0]["tg_id"])
            group_dict.setdefault("children", [{"title":l["e_name"]+"（"+l["c_name"]+"）","id":l["id"],"table_id":l["table_id"]} for l in group])
            # 用于设置默认展开
            if index == 0:
                group_dict.setdefault("expand", True)
                itme_dict = group_dict["children"][0]
                itme_dict.setdefault("selected", True)
            index += 1
            end_result.append(group_dict)
        message = {}
        message.setdefault("db_name", db_name)
        message.setdefault("group_info", end_result)
        result.setMessage(message)
        return result

    @AdminDecoratorServer.execImplDecorator()
    def updateTableGroupRelation(self, infos):
        args = {}
        ids = ",".join(infos["tables"])
        args.setdefault("db_id", int(infos["db_id"]))
        args.setdefault("group_id", infos["group_id"])
        args.setdefault("ids", ids)
        return self.DatabaseDaoInterface.updateTableGroupRelation(args)

    @AdminDecoratorServer.execImplDecorator()
    def updateTableGroupRelationByGroupId(self, group_id, dest_group_id):
        args = {}
        args.setdefault("src_group_id", group_id)
        args.setdefault("dest_group_id", dest_group_id)
        return self.DatabaseDaoInterface.updateTableGroupRelationByGroupId(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteTableGroupByDB(self, args):
        return self.DatabaseDaoInterface.deleteTableGroupByDB(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteTableGroupRelationByDB(self, args):
        return self.DatabaseDaoInterface.deleteTableGroupRelationByDB(args)

    @AdminDecoratorServer.execImplDecorator()
    def addTable(self, args):
        return self.DatabaseDaoInterface.addTable(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteTable(self, args):
        return self.DatabaseDaoInterface.deleteTable(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableInfoById(self, id):
        args = {}
        args.setdefault("id", id)
        return self.DatabaseDaoInterface.getTableInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableInfoByName(self, args):
        return self.DatabaseDaoInterface.getTableInfoByName(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableList(self, db_id):
        args = {}
        args.setdefault("db_id", db_id)
        return self.DatabaseDaoInterface.getTableList(args)

    @AdminDecoratorServer.execImplDecorator()
    def editTable(self, args):
        return self.DatabaseDaoInterface.editTable(args)

    @AdminDecoratorServer.execImplDecorator()
    def editTableByName(self, args):
        return self.DatabaseDaoInterface.editTableByName(args)

    @AdminDecoratorServer.execImplDecorator()
    def discardTableByName(self, args):
        return self.DatabaseDaoInterface.discardTableByName(args)

    @AdminDecoratorServer.execImplDecorator()
    def addColumn(self, args):
        return self.DatabaseDaoInterface.addColumn(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteColumn(self, args):
        return self.DatabaseDaoInterface.deleteColumn(args)

    @AdminDecoratorServer.execImplDecorator()
    def getColumnInfoById(self, product_id):
        args = {}
        args.setdefault("id", product_id)
        return self.DatabaseDaoInterface.getColumnInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def getColumnListByTableId(self, table_id):
        args = {}
        args.setdefault("table_id", table_id)
        result = self.DatabaseDaoInterface.getColumnListByTableId(args)
        message = []
        lines = result.getMessage()
        lines = sorted(lines, key=lambda x: x["id"])
        groups = itertools.groupby(lines, key=lambda x:x["id"])
        for key, value in groups:
            infos = list(value)
            row = {}
            row["id"] = infos[0]["id"]
            row["table_id"] = infos[0]["table_id"]
            row["e_name"] = infos[0]["e_name"]
            row["type"] = infos[0]["type"]
            row["remark"] = infos[0]["remark"]
            row["discarded"] = infos[0]["discarded"]
            row["hide"] = infos[0]["hide"]
            row["unlink"] = infos[0]["unlink"]
            row["gmt_create"] = infos[0]["gmt_create"]
            row["gmt_modify"] = infos[0]["gmt_modify"]
            links = []
            for i in infos:
                if i["tb_id"] is not None:
                    link = {}
                    link["key"] = i["tb_id"]
                    link["val"] = "{}.{}.{}".format(i["db_name"], i["tb_name"], i["col_name"])
                    link["db"] = i["db_id"]
                    link["cl"] = i["cl_id"]
                    links.append(link)
            row["links"] = links
            message.append(row)
        result.setMessage(message)
        return result

    @AdminDecoratorServer.execImplDecorator()
    def getColumnListByTableName(self, args):
        return self.DatabaseDaoInterface.getColumnListByTableName(args)

    @AdminDecoratorServer.execImplDecorator()
    def editColumn(self, args):
        return self.DatabaseDaoInterface.editColumn(args)

    @AdminDecoratorServer.execImplDecorator()
    def editColumnRemarkById(self, args, is_execute_many=False):
        return self.DatabaseDaoInterface.editColumnRemarkById(args, is_execute_many)

    @AdminDecoratorServer.execImplDecorator()
    def editColumnTypeById(self, args, is_execute_many=False):
        return self.DatabaseDaoInterface.editColumnTypeById(args, is_execute_many)

    @AdminDecoratorServer.execImplDecorator()
    def editColumnDiscardById(self, args):
        return self.DatabaseDaoInterface.editColumnDiscardById(args)

    @AdminDecoratorServer.execImplDecorator()
    def editColumnHideById(self, args):
        return self.DatabaseDaoInterface.editColumnHideById(args)

    @AdminDecoratorServer.execImplDecorator()
    def editColumnUnlinkById(self, args):
        return self.DatabaseDaoInterface.editColumnUnlinkById(args)

    @AdminDecoratorServer.execImplDecorator()
    def isInitSynchronize(self, db_id):
        args = {}
        args.setdefault("db_id", db_id)
        return self.DatabaseDaoInterface.isInitSynchronize(args)

    @AdminDecoratorServer.execImplDecorator()
    def initSynchronizeDatabase(self, args):
        # 初始化同步，先同步所有表，再同步表里的所有字段
        dao_db = self.DatabaseDaoInterface
        db_id = args["id"]
        count_info = self.isInitSynchronize(db_id)
        count = (count_info.getMessage())[0]["tableCount"]
        if count == 0:
            db_info = dao_db.getDatabaseAllInfoById({"id": db_id}).getMessage()
            db_src = {'host': db_info[0]["host"], 'user': db_info[0]["username"], 'passwd': db_info[0]["password"],
                      'db': db_info[0]["schema_name"], 'port': db_info[0]["port"]}
            db_schema = db_info[0]["schema_name"]
            args = {}
            args.setdefault("schema_name", db_schema)
            tables = dao_db.getSynchronizeDatabase(args, **db_src).getMessage()
            insertTableList = []
            insertColumnList = []
            insertGroupList = []
            logTableList = []
            for i in tables:
                db_table = i["TABLE_NAME"]
                tableDict = {}
                tableDict["db_id"] = db_id
                tableDict["c_name"] = i["TABLE_COMMENT"]
                tableDict["e_name"] = db_table
                tableDict["remark"] = ""
                tableDict["discarded"] = 0
                insertTableList.append(tableDict)
                logTableList.append(db_table)
            result_table = dao_db.addTable(insertTableList, True).getSuccess()

            args = {}
            args["db_id"] = db_id
            args["name"] = "未分组"
            group_id = (dao_db.getTableGroupInfoByName(args).getMessage())[0]["id"]
            if result_table:
                args = {}
                args.setdefault("db_id", db_id)
                tables = dao_db.getTableList(args).getMessage()
                for i in tables:
                    table_id = i["id"]
                    db_table = i["e_name"]
                    args = {}
                    args.setdefault("schema_name", db_schema)
                    args.setdefault("table_name", db_table)
                    columns = dao_db.getSynchronizeTable(args, **db_src).getMessage()
                    relationDict = {}
                    relationDict["table_id"] = table_id
                    relationDict["group_id"] = group_id
                    dao_db.addTableGroupRelation(relationDict)
                    for j in columns:
                        columnDict = {}
                        columnDict["table_id"] = table_id
                        e_name = j["COLUMN_NAME"]
                        columnDict["e_name"] = e_name
                        columnDict["type"] = j["COLUMN_TYPE"]
                        remark = j["COLUMN_COMMENT"]
                        columnDict["remark"] = remark
                        if e_name[0:2] == "~~":
                            columnDict["discarded"] = 1
                        else:
                            columnDict["discarded"] = 0
                        insertColumnList.append(columnDict)

                dao_db.addColumn(insertColumnList, True)

                # 输出log记录信息都是表
                return self.addDBLog(db_id, logTableList)

            else:
                return result_table
        else:
            return count_info

    @AdminDecoratorServer.execImplDecorator()
    def synchronizeDatabase(self, args):
        # 后续同步，比较表差和字段差
        dao_db = self.DatabaseDaoInterface
        dao_db = self.DatabaseDaoInterface
        db_id = args["id"]
        db_info = dao_db.getDatabaseAllInfoById({"id": db_id}).getMessage()
        db_src = {'host': db_info[0]["host"], 'user': db_info[0]["username"], 'passwd': db_info[0]["password"],
                  'db': db_info[0]["schema_name"], 'port': db_info[0]["port"]}
        db_schema = db_info[0]["schema_name"]
        args = {}
        args.setdefault("schema_name", db_schema)
        tables_src = dao_db.getSynchronizeDatabase(args, **db_src).getMessage()
        tables_src_list = [i["TABLE_NAME"] for i in tables_src]
        tables_dest = self.getTableList(db_id).getMessage()
        tables_dest_list = [i["e_name"] for i in tables_dest]
        # 获取源数据库和目标数据库的差集，用于增加整表
        tables_diff = set(tables_src_list) - set(tables_dest_list)
        tables_diff_list = list(tables_diff)
        tables_diff_dict = [i for i in tables_src if tables_diff_list.count(i["TABLE_NAME"]) > 0]
        # 获取需要比较表字段的数据表，排除上面差集的数据表
        tables_compare = set(tables_src_list) - tables_diff
        # 增加表
        logTableList = []
        for i in tables_diff_dict:
            db_table = i["TABLE_NAME"]
            tableDict = {}
            tableDict["db_id"] = db_id
            tableDict["c_name"] = i["TABLE_COMMENT"]
            tableDict["e_name"] = db_table
            tableDict["remark"] = ""
            tableDict["discarded"] = 0
            logTableList.append(db_table)
            result_table = dao_db.addTable(tableDict).getSuccess()
            insertColumnList = []
            args = {}
            args["db_id"] = db_id
            args["name"] = "未分组"
            groupinfo = dao_db.getTableGroupInfoByName(args)
            group_id = (dao_db.getTableGroupInfoByName(args).getMessage())[0]["id"]
            args = {}
            args.setdefault("db_id", db_id)
            args.setdefault("e_name", db_table)
            tables = dao_db.getTableInfoByName(args).getMessage()
            table_id = tables[0]["id"]
            # 添加默认表关系
            relationDict = {}
            relationDict["table_id"] = table_id
            relationDict["group_id"] = group_id
            dao_db.addTableGroupRelation(relationDict)

            if result_table:
                args = {}
                args.setdefault("db_id", db_id)
                args.setdefault("e_name", db_table)
                tables = dao_db.getTableInfoByName(args).getMessage()
                table_id = tables[0]["id"]
                db_table = tables[0]["e_name"]

                # 获取源数据库表字段
                args = {}
                args.setdefault("schema_name", db_schema)
                args.setdefault("table_name", db_table)
                columns = dao_db.getSynchronizeTable(args, **db_src).getMessage()
                for j in columns:
                    columnDict = {}
                    columnDict["table_id"] = table_id
                    e_name = j["COLUMN_NAME"]
                    columnDict["e_name"] = e_name
                    columnDict["type"] = j["COLUMN_TYPE"]
                    remark = j["COLUMN_COMMENT"]
                    columnDict["remark"] = remark
                    if e_name[0:2] == "~~":
                        columnDict["discarded"] = 1
                    else:
                        columnDict["discarded"] = 0
                    insertColumnList.append(columnDict)
                dao_db.addColumn(insertColumnList, True)

        # 比较表，根据缺少的字段，增加字段
        logColumnList = []
        for i in tables_compare:
            args = {}
            args.setdefault("db_id", db_id)
            args.setdefault("e_name", i)
            table_info = dao_db.getTableInfoByName(args).getMessage()
            table_id = table_info[0]["id"]
            db_table = table_info[0]["e_name"]
            args = {}
            args.setdefault("schema_name", db_schema)
            args.setdefault("table_name", db_table)
            columns_src = dao_db.getSynchronizeTable(args, **db_src).getMessage()
            columns_src_list = [i["COLUMN_NAME"] for i in columns_src]
            columns_dest = self.getColumnListByTableId(table_id).getMessage()
            columns_dest_list = [i["e_name"] for i in columns_dest]
            columns_diff = set(columns_src_list) - set(columns_dest_list)

            for j in columns_diff:
                args = {}
                args.setdefault("schema_name", db_schema)
                args.setdefault("table_name", db_table)
                args.setdefault("columnName", j)
                column_info = dao_db.getSynchronizeColumn(args, **db_src).getMessage()
                columnDict = {}
                columnDict["table_id"] = table_id
                e_name = j["COLUMN_NAME"]
                columnDict["e_name"] = e_name
                columnDict["type"] = j["COLUMN_TYPE"]
                remark = j["COLUMN_COMMENT"]
                columnDict["remark"] = remark
                if e_name[0:2] == "~~":
                    columnDict["discarded"] = 1
                else:
                    columnDict["discarded"] = 0
                logColumnName = "{}.{}".format(db_table, columnDict["e_name"])
                logColumnList.append(logColumnName)
                dao_db.addColumn(columnDict)

        dao_db.getDatabaseAllInfoById({"id": db_id})

        # 增加log信息
        return self.addDBLog(db_id, logTableList + logColumnList)

    @AdminDecoratorServer.execImplDecorator()
    def initSynchronizeTable(self, schema_name, table_name):
        # 多个表？不同数据库的表
        args = {}
        args.setdefault("schema_name", schema_name)
        args.setdefault("table_name", table_name)
        return self.DatabaseDaoInterface.initSynchronizeTable(args)

    @AdminDecoratorServer.execImplDecorator()
    def initSynchronizeColumn(self, schema_name, table_name, columnName):
        args = {}
        args.setdefault("schema_name", schema_name)
        args.setdefault("table_name", table_name)
        args.setdefault("columnName", columnName)
        return self.DatabaseDaoInterface.initSynchronizeColumn(args)

    @AdminDecoratorServer.execImplDecorator()
    def getSynchronizeDatabase(self, args, **kwargs):
        # args = {}
        # args.setdefault("schema_name", db_schema)
        return self.DatabaseDaoInterface.getSynchronizeDatabase(args, kwargs)

    @AdminDecoratorServer.execImplDecorator()
    def getSynchronizeTable(self, args, **kwargs):
        return self.DatabaseDaoInterface.getSynchronizeTable(args, kwargs)

    @AdminDecoratorServer.execImplDecorator()
    def getSynchronizeColumn(self, args, **kwargs):
        return self.DatabaseDaoInterface.getSynchronizeColumn(args, kwargs)

    @AdminDecoratorServer.execImplDecorator()
    def getSearchByTable(self, args):
        content = args
        args = {}
        args.setdefault("db_id", content["db_id"])
        args.setdefault("e_name", '%{}%'.format(content["content"]))
        return self.DatabaseDaoInterface.getSearchByTable(args)

    @AdminDecoratorServer.execImplDecorator()
    def getSearchByTableColumn(self, args):
        content = args
        search = content["content"].split('.')
        args = {}
        args.setdefault("db_id", content["db_id"])
        args.setdefault("tb_e_name", search[0])
        args.setdefault("col_e_name", '%{}%'.format(search[1]))
        return self.DatabaseDaoInterface.getSearchByTableColumn(args)

    @AdminDecoratorServer.execImplDecorator()
    def getSearchByColumn(self, args):
        content = args
        args = {}
        args.setdefault("db_id", content["db_id"])
        args.setdefault("e_name", '%{}%'.format(content["content"][1:]))
        return self.DatabaseDaoInterface.getSearchByColumn(args)

    @AdminDecoratorServer.execImplDecorator()
    def getSearchByColumnRemark(self, args):
        content = args
        args = {}
        args.setdefault("db_id", content["db_id"])
        args.setdefault("remark", '%{}%'.format((content["content"])[1:]))
        return self.DatabaseDaoInterface.getSearchByColumnRemark(args)

    @AdminDecoratorServer.execImplDecorator()
    def addDBLog(self, db_id, content, user_id=0, type=0):
        # todo 默认无用户
        args = {}
        args.setdefault("user_id", user_id)
        args.setdefault("db_id", db_id)
        if type == 0:
            content = [c for c in content]
            concat_content = "添加了{}".format("、".join(content))
        elif type == 1:
            concat_content = "更新了{}".format("、".join(content))

        args.setdefault("content", concat_content)
        return self.DatabaseDaoInterface.addDBLog(args)

    @AdminDecoratorServer.execImplDecorator()
    def getDBLogList(self, db_id):
        args = {}
        args.setdefault("db_id", db_id)
        return self.DatabaseDaoInterface.getDBLogList(args)

    @AdminDecoratorServer.execImplDecorator()
    def addColumnLink(self, args):
        return self.DatabaseDaoInterface.addColumnLink(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteColumnLink(self, args):
        return self.DatabaseDaoInterface.deleteColumnLink(args)

    @AdminDecoratorServer.execImplDecorator()
    def getLinkTableList(self, db_id):
        args = {}
        args.setdefault("db_id", db_id)
        return self.DatabaseDaoInterface.getLinkTableList(args)

    @AdminDecoratorServer.execImplDecorator()
    def getLinkColumnList(self, table_id):
        args = {}
        args.setdefault("table_id", table_id)
        return self.DatabaseDaoInterface.getLinkColumnList(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableListByTableName(self, content):
        args = {}
        args.setdefault("db_id", content["id"])
        args.setdefault("e_name", '%{}%'.format(content["content"]))
        return self.DatabaseDaoInterface.getTableListByTableName(args)

    @AdminDecoratorServer.execImplDecorator()
    def getColumnListByColName(self, content):
        args = {}
        args.setdefault("table_id", content["id"])
        args.setdefault("e_name", '%{}%'.format(content["content"]))
        return self.DatabaseDaoInterface.getColumnListByColName(args)

    @AdminDecoratorServer.execImplDecorator()
    def addTableRoute(self, args):
        return self.DatabaseDaoInterface.addTableRoute(args)

    @AdminDecoratorServer.execImplDecorator()
    def addDataNode(self, args):
        return self.DatabaseDaoInterface.addDataNode(args)

    @AdminDecoratorServer.execImplDecorator()
    def addDataRoute(self, args):
        return self.DatabaseDaoInterface.addDataRoute(args)

    @AdminDecoratorServer.execImplDecorator()
    def getTableRouteList(self, table_id):
        args = {}
        args.setdefault("table_id", table_id)
        result = self.DatabaseDaoInterface.getTableRouteList(args)
        route = result.getMessage()
        message = []
        route_group = itertools.groupby(route, key=lambda x: x["route_id"])
        for key, value in route_group:
            s = {}
            s.setdefault("key", key)
            s.setdefault("route", list(value))
            message.append(s)
        result.setMessage(message)
        return result

    @AdminDecoratorServer.execImplDecorator()
    def updateComment(self, args):
        result = DataResult()
        result.setSuccess(True)
        user_id = 0
        table_id = args["id"]
        db_id = args["db_id"]
        # 获取表信息
        table_info = self.getTableInfoById(table_id).getMessage()
        table_e_name = table_info[0]["e_name"]
        table_c_name = table_info[0]["c_name"]
        # 获取原库的表信息
        table_info_src = self.getTableComment(db_id, table_e_name).getMessage()
        table_c_name_src = table_info_src[0]["TABLE_COMMENT"]
        flag_table = False
        table_content = []
        # 对比表信息
        if table_c_name != table_c_name_src:
            flag_table = True
            content = "表{}的【中文名】从 [{}] 变成 [{}]".format(table_e_name, table_c_name, table_c_name_src)
            table_content.append(content)
        if flag_table:
            self.editTableCNameById(table_id, table_c_name_src)
            self.addDBLog(db_id, table_content, user_id, 1)
        # 对比字段信息
        c_args = {}
        c_args.setdefault("e_name", table_e_name)
        c_args.setdefault("db_id", db_id)
        # 获取表字段信息
        column_info = self.getColumnListByTableName(c_args).getMessage()
        # 获取原库的表字段信息
        db_src = self.getDBSrcInfo(db_id)
        cs_args = {}
        cs_args.setdefault("schema_name", db_src["db"])
        cs_args.setdefault("table_name", table_e_name)
        column_info_src = self.DatabaseDaoInterface.getSynchronizeTable(cs_args, **db_src).getMessage()
        column_info = [{"name": i["e_name"], "type": i["type"], "remark": i["remark"], "id": i["id"]} for i in
                       column_info]
        column_info_src = [{"name": i["COLUMN_NAME"], "type": i["COLUMN_TYPE"], "remark": i["COLUMN_COMMENT"]}
                           for i in column_info_src]
        column_info = sorted(column_info, key=lambda x: x["name"])
        column_info_src = sorted(column_info_src, key=lambda x: x["name"])
        flag_column = False
        column_content = []
        update_column_type = []
        update_column_remark = []
        if len(column_info) == len(column_info_src):
            flag_column = True
        else:
            result.setSuccess(False)
            result.setMessage("当前表的字段数和源库中不一致，请先同步表信息")
        if flag_column:
            for x, y in zip(column_info, column_info_src):
                one_flag = False
                if x["name"] == y["name"]:
                    one_flag = True
                if one_flag:
                    if x["type"] != y["type"]:
                        args_type = {}
                        args_type.setdefault("id", x["id"])
                        args_type.setdefault("val", y["type"])
                        update_column_type.append(args_type)
                        content = "字段{}.{}的【类型】从 [{}] 变成 [{}]".format(table_e_name,
                                                                      x["name"], x["type"], y["type"])
                        column_content.append(content)
                    if x["remark"] != y["remark"]:
                        args_remark = {}
                        args_remark.setdefault("id", x["id"])
                        args_remark.setdefault("val", y["remark"])
                        update_column_remark.append(args_remark)
                        content = "字段{}.{}的【备注】从 [{}] 变成 [{}]".format(table_e_name,
                                                                      x["name"], x["remark"], y["remark"])
                        column_content.append(content)
        if flag_column:
            self.editColumnTypeById(update_column_type, True)
            self.editColumnRemarkById(update_column_remark, True)
            if len(column_content) > 0:
                self.addDBLog(db_id, column_content, user_id, 1)

        return result

    @AdminDecoratorServer.execImplDecorator()
    def getTableComment(self, db_id, table_name):
        db_src = self.getDBSrcInfo(db_id)
        db_schema = db_src["db"]
        args = {}
        args.setdefault("schema_name", db_schema)
        args.setdefault("table_name", table_name)
        return self.DatabaseDaoInterface.getTableComment(args, **db_src)

    @AdminDecoratorServer.execImplDecorator()
    def editTableCNameById(self, id, table_c_name):
        args = {}
        args.setdefault("id", id)
        args.setdefault("c_name", table_c_name)
        return self.DatabaseDaoInterface.editTableCNameById(args)

    @AdminDecoratorServer.execImplDecorator()
    def editTableRemarkById(self, args):
        return self.DatabaseDaoInterface.editTableRemarkById(args)

    @AdminDecoratorServer.execImplDecorator()
    def getDBSrcInfo(self, db_id):
        db_info = self.getDatabaseAllInfoById(db_id).getMessage()
        db_src = {'host': db_info[0]["host"], 'user': db_info[0]["username"], 'passwd': db_info[0]["password"],
                  'db': db_info[0]["schema_name"], 'port': db_info[0]["port"]}
        return db_src

    @AdminDecoratorServer.execImplDecorator()
    def getViewLinks(self, id, link_type):
        result = DataResult()
        if int(link_type) == 1:
            table_id = id
            args = {}
            args.setdefault("table_id", table_id)
            tb_info = self.getTableInfoById(table_id).getMessage()
            type_name = tb_info[0]["e_name"]

            link_info = self.DatabaseDaoInterface.getViewLinks(args)
            infos = link_info.getMessage()
            links = []
            for i in infos:
                link = {}
                link.setdefault("source", i["src_tb_name"])
                link.setdefault("target", i["link_tb_name"])
                link.setdefault("value", "{} > {}".format(i["src_col_name"], i["link_col_name"]))
                links.append(link)

            datus = []
            table_info = self.DatabaseDaoInterface.getViewTableInfo(args)
            table_group = itertools.groupby(table_info.getMessage(), key=lambda x: x["name"])
            for key, group in table_group:
                data = {}
                group = list(group)
                db = group[0]["db_name"]
                link_type = group[0]["link_type"]
                data.setdefault("t_name", key)
                data.setdefault("db_name", db)
                data.setdefault("link_type", link_type)
                cols = [g['e_name'] for g in group]
                data.setdefault('info', cols)
                datus.append(data)

        elif int(link_type) == 2:
            group_id = id
            group_info = self.getTableGroupInfoById(group_id).getMessage()
            type_name = group_info[0]["name"]
            table_list = []
            tables = self.getViewTableByGroup(group_id).getMessage()
            tables = [t["table_id"] for t in tables]
            table_list.extend(tables)

            datus = []
            for level in range(1,10):
                if tables != []:
                    table_info = self.getLinkTable(tables, level)
                    logger.info(table_info)
                    tables = [t["dt.id"] for t in table_info]
                    table_list.extend(tables)

                    logger.info(tables)

                    table_group = itertools.groupby(table_info, key=lambda x: x["name"])
                    for key, group in table_group:
                        data = {}
                        group = list(group)
                        db = group[0]["db_name"]
                        link_type = group[0]["link_type"]
                        data.setdefault("t_name", key)
                        data.setdefault("db_name", db)
                        data.setdefault("link_type", link_type)
                        cols = [g['e_name'] for g in group]
                        data.setdefault('info', cols)
                        datus.append(data)

            link_info = self.getViewLinksByGroup(table_list)
            infos = link_info.getMessage()
            links = []
            for i in infos:
                link = {}
                link.setdefault("source", i["src_tb_name"])
                link.setdefault("target", i["link_tb_name"])
                link.setdefault("value", "{} > {}".format(i["src_col_name"], i["link_col_name"]))
                links.append(link)

        message = {}
        message.setdefault("links", links)
        message.setdefault("data", datus)
        message.setdefault("type_name", type_name)
        result.setMessage(message)
        result.setSuccess(True)
        return result

    def getLinkTable(self, table_id, link_level):
        if table_id != []:
            return self.getViewTableInfoByGroup(table_id, link_level).getMessage()
        else:
            return []

    def addLinkByMatchRule(self, args):
        result = DataResult()
        # 1是自定义匹配，2是驼峰全局匹配，3是_全局匹配
        db_id = args["db"]
        content = args["content"]
        match_type = args["type"]
        links = []
        link_args = {}
        link_args.setdefault("relation_type", 1)
        if match_type == 1:
            lists = [l.split("-") for l in content.split(",")]
            for l in lists:
                link = l[0].lower()
                src = l[1].lower()
                table_info = self.getIdColumnInfoByTableName(db_id, link).getMessage()
                link_args["link_column_id"] = table_info[0]["id"]
                link_args["link_table_id"] = table_info[0]["table_id"]

                info_links = self.addLinkByMatchRuleInsert(db_id, src, link_args)
                links.extend(info_links)

        elif match_type == 2 or match_type == 3:
            table_info = self.getIdColumnListByTableName(db_id).getMessage()
            for t in table_info:
                link_args["link_column_id"] = t["cl_id"]
                link_args["link_table_id"] = t["t_id"]
                link = t["t_name"]
                src = ""
                if match_type == 2:
                    src = "{}id".format(link)
                elif match_type == 3:
                    src = "{}_id".format(link)

                info_links = self.addLinkByMatchRuleInsert(db_id, src, link_args)
                links.extend(info_links)

        return self.DatabaseDaoInterface.addColumnLink(links, is_execute_many=True)

    def addLinkByMatchRuleInsert(self, db_id, src, link_args ):
        links = []
        column_info = self.getColumnInfoByEname(db_id, src).getMessage()
        for c in column_info:
            link_args_bk = deepcopy(link_args)
            link_args_bk["src_column_id"] = c["id"]
            link_args_bk["src_table_id"] = c["table_id"]
            links.append(link_args_bk)
        return links

    def getColumnInfoByEname(self, db_id, e_name):
        args = {}
        args.setdefault('e_name', e_name)
        args.setdefault('db_id', db_id)
        return self.DatabaseDaoInterface.getColumnInfoByEname(args)

    def getIdColumnInfoByTableName(self, db_id, e_name):
        args = {}
        args.setdefault('e_name', e_name)
        args.setdefault('db_id', db_id)
        return self.DatabaseDaoInterface.getIdColumnInfoByTableName(args)

    def getIdColumnListByTableName(self, db_id):
        args = {}
        args.setdefault('db_id', db_id)
        return self.DatabaseDaoInterface.getIdColumnListByTableName(args)

    def getViewTableByGroup(self, group_id):
        args = {}
        args.setdefault("group_id", group_id)
        return self.DatabaseDaoInterface.getViewTableByGroup(args)

    def getViewTableInfoByGroup(self, table_id, link_level):
        if link_level > 3:
            link_level = 3
        args = {}
        args.setdefault("table_ids", table_id)
        args.setdefault("link_type", link_level)
        return self.DatabaseDaoInterface.getViewTableInfoByGroup(args)

    def getViewLinksByGroup(self, table_id):
        args = {}
        args.setdefault("table_ids", table_id)
        return self.DatabaseDaoInterface.getViewLinksByGroup(args)