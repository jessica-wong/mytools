# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.TaskMetaqInfoDao import TaskMetaqInfoDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('TaskServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"TaskServiceImpl.log")

class TaskService(object):

    def __init__(self):
        self.taskMetaqInfoDaoInterface = TaskMetaqInfoDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addTaskInfo(self,args):
        return self.taskMetaqInfoDaoInterface.addTaskInfo(args)

    @AdminDecoratorServer.execImplDecorator()
    def getWaitingTaskInfos(self):
        args={}
        args.setdefault("limit",SystemConfig.maxThreadSize)
        return self.taskMetaqInfoDaoInterface.getWaitingTaskInfos(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteTaskInfo(self,args):
        return self.taskMetaqInfoDaoInterface.deleteTaskInfo(args)

    @AdminDecoratorServer.execImplDecorator()
    def updateTaskInfo(self,args):
        return self.taskMetaqInfoDaoInterface.updateTaskInfo(args)

