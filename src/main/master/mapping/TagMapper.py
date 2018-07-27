# -*- coding: utf-8 -*-

class TagSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addWebApiTagSQL="""
        insert into tag_associate (tag_id,api_id,project_id,application_id) values (%(tagId)s,%(apiId)s,%(projectId)s,%(applicationId)s)
        """
        getTagsForApiSQL="""
        select * from tag where tag_type=0
        """

        #SET SQL FOR DAO
        self.data.setdefault("addWebApiTag",addWebApiTagSQL)
        self.data.setdefault("getTagsForApi", getTagsForApiSQL)