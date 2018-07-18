# -*- coding: utf-8 -*-

import json
import traceback
import tornado.web
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.service.impl.ProductServiceImpl import ProductService
from src.main.master.util.jsonUtil.JsonUtil import CJsonEncoder
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('ProductController')
logger.write_to_file(SystemConfig.logPathPrefix+"ProductController.log")

class ProductHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(30)

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
                'getProductInfoById': lambda: self.getProductInfoById(),
                'getProductList':lambda :self.getProductList(),
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
                'addProduct' : lambda : self.addProduct(),
                'deleteProduct':lambda :self.deleteProduct(),
                'editProduct':lambda :self.editProduct(),
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
    def addProduct(self):
        logger.info(self.request.body)
        data = json.loads(self.request.body)
        #数据库该字段可为空,入参没有时,需要补充key,否则访问sql
        return ProductService().addProduct(data)

    def getProductInfoById(self):
        productId= self.get_argument("id")
        return ProductService().getProductInfoById(productId)

    def getProductList(self):
        # todo 后面传了bu的Id
        # businessUnit = self.get_argument("businessUnit")
        # return ProductService().getProductList(businessUnit)
        return ProductService().getProductList()

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def deleteProduct(self):
        return ProductService().deleteProduct(json.loads(self.request.body))

    @AdminDecoratorServer.webInterceptorDecorator(SystemConfig.adminHost)
    def editProduct(self):
        logger.info(self.request.body)
        return ProductService().editProduct(json.loads(self.request.body))
