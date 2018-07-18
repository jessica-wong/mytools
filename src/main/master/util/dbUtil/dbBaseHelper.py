# -*- coding: utf-8 -*-
from src.main.master.util.dbUtil.dbBaseUtil import Connection
from src.main.master.entity.DataResult import DataResult
from src.main.master.util.logUtil.log import Log
from src.main.master.common.constants import SystemConfig
import traceback

#set log
logger = Log('dbBaseHelper')
logger.write_to_file(SystemConfig.logPathPrefix+"dbBaseHelper.log")

#本类只提供了base操作
class DbBaseHelper(object):

    def __init__(self,sql=None,args=None,is_execute_many=False):
        self.data = DataResult()
        self.sql=sql
        self.args =args
        self.is_execute_many=is_execute_many

    #针对select操作
    def read(self, **kwargs):
        db = Connection(autocommit=False, **kwargs)
        try:
            if self.args is not None and not isinstance(self.args,dict):
                logger.error("sql params [{0}] type is error,must be dict".format(self.args))
                self.data.setMessage("sql params type is error,must be dict")
                self.data.setSuccess(False)
                return self.data
            ret = db.read(self.sql,self.args)
            self.data.setMessage(list(ret))
            self.data.setSuccess(True)
            return self.data
        except Exception as e:
            logger.error("select sql:{0} args:{1} Exception:{2}".format(self.sql,self.args,traceback.format_exc()))
            self.data.setSuccess(False)
            self.data.setMessage(traceback.format_exc())
            self.data.setStatusCode(500)
            return self.data
        finally:
            db.close()

    # 针对update、insert、delete操作，is_execute_many=True 支持批量插入和更新
    def write(self):
        db = Connection(autocommit=False)
        try:
            if self.is_execute_many:
                if not isinstance(self.args,list):
                    logger.error("sql params [{0}] type is error,must be list".format(self.args))
                    self.data.setMessage("sql params type is error,must be list")
                    self.data.setSuccess(False)
                    return self.data
            elif self.args is not None and not isinstance(self.args,dict):
                logger.error("sql params [{0}] type is error,must be dict".format(self.args))
                self.data.setMessage("sql params type is error,must be dict")
                self.data.setSuccess(False)
                return self.data
            ret = db.write(self.sql,self.args,self.is_execute_many)
            db.commit()
            self.data.setMessage(ret)
            self.data.setSuccess(True)
            return self.data
        except Exception as e:
            logger.error("write sql:{0} args:{1} Exception:{2}".format(self.sql,self.args,traceback.format_exc()))
            self.data.setSuccess(False)
            self.data.setMessage(traceback.format_exc())
            self.data.setStatusCode(500)
            return self.data
        finally:
            db.close()

    def execReadOnlySQL(self,dbConfig,sql):
        db = Connection(autocommit=False,**dbConfig)
        try:
            ret = db.read(sql)
            return list(ret)
        except Exception as e:
            logger.error("execReadOnlySQL Exception:sql{0}  reason:{1}".format(sql,traceback.format_exc()))
            return []
        finally:
            db.close()
