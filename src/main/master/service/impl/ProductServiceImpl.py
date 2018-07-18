# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.ProductDao import ProductDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('ProductServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"ProductServiceImpl.log")

class ProductService(object):

    def __init__(self):
        self.ProductDaoInterface = ProductDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addProduct(self,args):
        return self.ProductDaoInterface.addProduct(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteProduct(self,args):
        return self.ProductDaoInterface.deleteProduct(args)

    @AdminDecoratorServer.execImplDecorator()
    def getProductInfoById(self,productId):
        args={}
        args.setdefault("id",productId)
        return self.ProductDaoInterface.getProductInfoById(args)

    @AdminDecoratorServer.execImplDecorator()
    def getProductList(self):
        # todo businessUnit=2
        args = {}
        args.setdefault("businessUnit", 2)
        return self.ProductDaoInterface.getProductList(args)

    @AdminDecoratorServer.execImplDecorator()
    def editProduct(self, args):
        return self.ProductDaoInterface.editProduct(args)

