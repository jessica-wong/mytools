# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.TagDao import TagDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('TagServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"TagServiceImpl.log")

class TagService(object):

    def __init__(self):
        self.TagDaoInterface = TagDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addWebApiTag(self,args):

        return self.TagDaoInterface.addWebApiTag(args)

    def getTagsForApi(self):
        return self.TagDaoInterface.getTagsForApi()