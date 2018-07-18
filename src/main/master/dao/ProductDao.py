# -*- coding: utf-8 -*-

import inspect
from src.main.master.util.dbUtil.dbBaseHelper import DbBaseHelper
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
from src.main.master.mapping.ProductMapper import ProductSQLMapper

#set log
logger = Log('ProductDao')
logger.write_to_file(SystemConfig.logPathPrefix+"ProductDao.log")

class ProductDaoInterface:

    def addProduct(self,args):
        #实例化
        logger.info(inspect.stack()[0][3])
        sql = ProductSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate =DbBaseHelper(sql,args)
        return daoOperate.write()

    def deleteProduct(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ProductSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()

    def getProductInfoById(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ProductSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def getProductList(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ProductSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.read()

    def editProduct(self,args):
        logger.info(inspect.stack()[0][3])
        sql = ProductSQLMapper().getSQL(inspect.stack()[0][3])
        daoOperate = DbBaseHelper(sql, args)
        return daoOperate.write()