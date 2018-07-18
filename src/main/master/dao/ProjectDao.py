# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.ProjectMapper import ProjectSQLMapper

#set log
logger = Log('ProjectDao')
logger.write_to_file(SystemConfig.logPathPrefix+"ProjectDao.log")

class ProjectDaoInterface:

    def addProject(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = ProjectSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def getProjectInfoByName(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = ProjectSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.read()

    def deleteProject(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ProjectSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getProjectInfoById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ProjectSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getProjectList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ProjectSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql,args)
        return daoOperate.read()

    def getProjectListLeader(self):
        logger.info(inspect.stack()[0][3])
        sql = ProjectSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql)
        return daoOperate.read()

    def editProject(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ProjectSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql,args)
        return daoOperate.write()

    def getProjectLogListData(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ProjectSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql,args)
        return daoOperate.read()

    def getProjectCount(self):
        logger.info(inspect.stack()[0][3])
        sql = ProjectSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql)
        return daoOperate.read()

    def getProjectListByApplicationId(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ProjectSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql,args)
        return daoOperate.read()