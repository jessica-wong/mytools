# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.TaskMetaqInfoMapper import TaskMetaqInfoSQLMapper

#set log
logger = Log('TaskMetaqInfoDao')
logger.write_to_file(SystemConfig.logPathPrefix+"TaskMetaqInfoDao.log")

class TaskMetaqInfoDaoInterface:

    def addTaskInfo(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = TaskMetaqInfoSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getWaitingTaskInfos(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = TaskMetaqInfoSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def updateTaskInfo(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TaskMetaqInfoSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def updateTaskStatus(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TaskMetaqInfoSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def deleteTaskInfo(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TaskMetaqInfoSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()