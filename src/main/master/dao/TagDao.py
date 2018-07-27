# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.TagMapper import TagSQLMapper

#set log
logger = Log('TagDao')
logger.write_to_file(SystemConfig.logPathPrefix+"TagDao.log")

class TagDaoInterface:

    def addWebApiTag(self,args):
        logger.info(inspect.stack()[0][3])
        sql = TagSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getTagsForApi(self):
        logger.info(inspect.stack()[0][3])
        sql = TagSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql)
        return daoOperate.read()