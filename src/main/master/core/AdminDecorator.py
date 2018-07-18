# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult

#set log
logger = Log('AdminDecorator')
logger.write_to_file(SystemConfig.logPathPrefix+"AdminDecorator.log")

class AdminDecoratorServer(object):

    def __init__(self):
        pass

    @staticmethod
    def execImplDecorator():
        def _deco(func):
            def __deco(*args,**kwargs):
                try:
                    return func(*args,**kwargs)
                except Exception as e:
                    dataResult = DataResult()
                    logger.error(traceback.format_exc())
                    dataResult.setMessage(traceback.format_exc())
                    dataResult.setSuccess(False)
                    dataResult.setStatusCode(500)
                    return dataResult
            return __deco
        return _deco

    @staticmethod
    def webInterceptorDecorator(adminIps):
        def _deco(func):
            def __deco(*args,**kwargs):
                dataResult = DataResult()
                try:
                    isAdmin = False
                    ips = adminIps.split(",")
                    #get remote ip of client
                    remote_ip = args[0].__dict__['request'].remote_ip
                    for ip in ips:
                        if remote_ip == ip:
                            isAdmin= True
                    if not isAdmin:
                        dataResult.setSuccess(False)
                        dataResult.setMessage("Request IP [{0}]without a white list，to be intercepted".format(remote_ip))
                        return dataResult
                    return func(*args,**kwargs)
                except Exception as e:
                    logger.error(traceback.format_exc())
                    dataResult.setMessage(traceback.format_exc())
                    dataResult.setSuccess(False)
                    dataResult.setStatusCode(500)
                    return dataResult
            return __deco
        return _deco

