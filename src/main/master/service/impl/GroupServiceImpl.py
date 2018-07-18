# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.GroupDao import GroupDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('GroupServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"GroupServiceImpl.log")

class GroupService(object):

    def __init__(self):
        self.GroupDaoInterface = GroupDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addParentGroup(self,args):
        if "type" not in args:
            args.setdefault("type",0)
        logger.error("args={0}".format(args))
        dataResult = self.GroupDaoInterface.addParentGroup(args)
        return dataResult

    def addChildGroup(self, args):
        logger.error("args={0}".format(args))
        if 'ischild' not in args:
            args.setdefault("ischild",None)
        if 'parent_groupid' not in args:
            args.setdefault("parent_groupid", None)
        if "children" in args:
            args.pop("children")
        dataResult = self.GroupDaoInterface.addChildGroup(args)
        if dataResult.getSuccess():
            dataResult = self.GroupDaoInterface.getGroupInfoByName(args)
            if dataResult.getSuccess() and len(dataResult.getMessage())>0:
                dataResult.setMessage(dataResult.getMessage()[0])
            else:
                dataResult.setSuccess(False)
        return dataResult

    def editGroup(self,args):
        return self.GroupDaoInterface.editGroup(args)

    @AdminDecoratorServer.execImplDecorator()
    def getGroupInfoByProjectId(self,projectId,type=0):
        treeResult = DataResult()
        trees =[]
        args={}
        args.setdefault("projectId",projectId)
        args.setdefault("type", type)
        args.setdefault("parentGroupId",0)
        #先查根结点
        dataResult = self.GroupDaoInterface.getGroupInfoByParentGroupId(args)
        if dataResult.getSuccess():
            for item in dataResult.getMessage():
                data={}
                data["children"]=[]
                data["name"]=item["name"]
                data["expand"]=True
                data["parentGroupId"]=item["parent_groupid"]
                data["groupId"]=item["id"]
                #查找子节点
                args.pop("parentGroupId")
                args.setdefault("parentGroupId",item["id"])
                sonNodes = self.GroupDaoInterface.getGroupInfoByParentGroupId(args)
                if sonNodes.getSuccess():
                    for sonItem in sonNodes.getMessage():
                        sonData={}
                        sonData["children"] = []
                        sonData["name"] = sonItem["name"]
                        sonData["expand"] = True
                        sonData["parentGroupId"] = sonItem["parent_groupid"]
                        sonData["groupId"] = sonItem["id"]
                        data["children"].append(sonData)
                trees.append(data)
        treeResult.setMessage(trees)
        treeResult.setSuccess(True)
        return treeResult


    @AdminDecoratorServer.execImplDecorator()
    def deleteGroup(self,args):
        return self.GroupDaoInterface.deleteGroup(args)

    def getGroupInfoByParentGroupId(self,args):
        return self.GroupDaoInterface.getGroupInfoByParentGroupId(args)

    def getGroupByProjectId(self,projectId,type):
        treeResult = DataResult()
        trees =[]
        args={}
        args.setdefault("projectId",projectId)
        args.setdefault("type", type)
        args.setdefault("parentGroupId",0)
        #先查根结点
        dataResult = self.GroupDaoInterface.getGroupInfoByParentGroupId(args)
        if dataResult.getSuccess():
            for item in dataResult.getMessage():
                data={}
                data["children"]=[]
                data["title"]=item["name"]
                data["expand"]=True
                data["parentGroupId"]=item["parent_groupid"]
                data["groupId"]=item["id"]
                #查找子节点
                args.pop("parentGroupId")
                args.setdefault("parentGroupId",item["id"])
                sonNodes = self.GroupDaoInterface.getGroupInfoByParentGroupId(args)
                if sonNodes.getSuccess():
                    for sonItem in sonNodes.getMessage():
                        sonData={}
                        sonData["children"] = []
                        sonData["title"] = sonItem["name"]
                        sonData["expand"] = True
                        sonData["parentGroupId"] = sonItem["parent_groupid"]
                        sonData["groupId"] = sonItem["id"]
                        data["children"].append(sonData)
                trees.append(data)
        treeResult.setMessage(trees)
        treeResult.setSuccess(True)
        return treeResult