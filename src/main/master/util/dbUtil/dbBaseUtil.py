# -*- coding: utf-8 -*-

import sys
import pymysql
import pymysql.cursors
from src.main.master.common.constants import DbConfig,SystemConfig
from src.main.master.util.logUtil.log import Log

#set log
logger = Log('dbBaseUtil')
logger.write_to_file(SystemConfig.logPathPrefix +"dbBaseUtil.log")

#set
dbinfo ={'host':DbConfig.host,'user':DbConfig.user,'passwd':DbConfig.passwd,'db':DbConfig.db,'port' :DbConfig.port}

class Connection(object):
    """
    General mysql read/write class
    example:
    dbinfo = {
          'host': '127.0.0.1',
          'user': 'root',
          'passwd': '123456',
          'db': 'testservice'
           }
    db = Connection(**dbinfo)

    """
    def __init__(self, autocommit = True,**kwargs):
        self.autocommit = autocommit
        if kwargs == None or len(kwargs) == 0:
          self.reconnect(**dbinfo)
        else:
          self.reconnect(**kwargs)

    def read(self, sql, args = None):
        c = self._conn.cursor()
        try:
            c.execute(sql, args)
            ret = c.fetchall()
            return ret
        finally:
            try:
                c.close()
            except:
                pass

    def write(self, sql, args = None, is_execute_many=False):
        c = self._conn.cursor()
        caller = sys._getframe(1).f_code.co_name
        logger.debug('in write:caller:%s\tsql:%s'%(caller, sql))
        try:
            if not is_execute_many:
                ret = c.execute(sql, args)
                # 增加返回的id
                # todo 考虑并发的情况
                ret = self._conn.insert_id()
            else:

                ret = c.executemany(sql, args)
                ret = self._conn.insert_id()
            if self.autocommit:
                self._conn.commit()
            return ret
        finally:
            try:
                c.close()
            except:
                pass

    def write_transaction(self, sql, args = None, is_execute_many=False):
        c = self._conn.cursor()
        caller = sys._getframe(1).f_code.co_name
        logger.debug('in write:caller:%s\tsql:%s'%(caller, sql))
        try:
            if not is_execute_many:
                ret = c.execute(sql, args)
                # 增加返回的id
                # todo 考虑并发的情况
                ret = self._conn.insert_id()
            else:
                ret = c.executemany(sql, args)
                ret = self._conn.insert_id()
            if self.autocommit:
                self._conn.commit()
            return ret
        except:
            self._conn.rollback()
        finally:
            try:
                c.close()
            except:
                pass

    def reconnect(self,**kwargs):
        self._conn = self._get_connection(**kwargs)

    def _get_connection(self,**kwargs):
        return pymysql.connect(cursorclass=pymysql.cursors.DictCursor, charset = 'utf8', **kwargs)

    def commit(self):
        if getattr(self, '_conn', None) is not None:
            self._conn.commit()

    def rollback(self):
        if getattr(self, '_conn', None) is not None:
            self._conn.rollback()

    def close(self):
        if getattr(self, '_conn', None) is not None:
            self._conn.close()
            self._conn = None