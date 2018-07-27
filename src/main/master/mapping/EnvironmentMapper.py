# -*- coding: utf-8 -*-

class EnvironmentSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addEnvironmentItemSQL="""
        insert into environment (env_name,create_userid,gmt_create) 
        values (%(env_name)s,%(userId)s,now())
        """
        deleteEnvironmentItemSQL="""
        delete from environment where id = %(envId)s
        """
        editEnvironmentItemSQL="""
        update environment set env_name=%(name)s,pre_url=%(url)s,data_template=%(template)s,db_name=%(dbname)s,
        db_hostname=%(dbhostname)s,db_port=%(dbport)s,db_username=%(dbusername)s,db_passwd=%(dbpasswd)s,auth_info=%(authInfo)s,headers=%(headers)s
        where id=%(envId)s
        """
        getEnvironmentInfoByIdSQL="""
        select * from environment where id = %(envId)s
        """
        getEnvironmentInfosSQL="""
        select * from environment
        """
        getEnvironmentInfosByUserIdSQL="""
        select * from environment where create_userid=%(userId)s
        """
        getEnvironmentInfoByNameSQL="""
        select * from environment where env_name=%(envName)s
        """

        #SET SQL FOR DAO
        self.data.setdefault("addEnvironmentItem",addEnvironmentItemSQL)
        self.data.setdefault("deleteEnvironmentItem",deleteEnvironmentItemSQL)
        self.data.setdefault("editEnvironmentItem",editEnvironmentItemSQL)
        self.data.setdefault("getEnvironmentInfoById",getEnvironmentInfoByIdSQL)
        self.data.setdefault("getEnvironmentInfos", getEnvironmentInfosSQL)
        self.data.setdefault("getEnvironmentInfosByUserId",getEnvironmentInfosByUserIdSQL)
        self.data.setdefault("getEnvironmentInfoByName",getEnvironmentInfoByNameSQL)
