# -*- coding: utf-8 -*-

class LoginSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        getUserInfoSQL="""
        select * from user where username=%(userName)s and passwd=%(passWord)s and status=0 limit 1
        """

        #SET SQL FOR DAO
        self.data.setdefault("getUserInfo",getUserInfoSQL)
