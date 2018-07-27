# -*- coding: utf-8 -*-

class WebApiSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addWebApiSQL="""
        insert into webapi (ApplicationId,Method,OperationId,Path,Produces,ProjectId,Summary) 
        values (%(ApplicationId)s,%(Method)s,%(OperationId)s,%(Path)s,%(Produces)s,%(ProjectId)s,%(Summary)s)
        """
        updateWebApiSQL="""
        update webapi set Method=%(Method)s,OperationId=%(OperationId)s,Path=%(Path)s,Produces=%(Produces)s,
        Summary=%(Summary)s where ApplicationId = %(applicationId)s and ProjectId=%(projectId)s and id=%(webApiId)s
        """
        deleteWebApiSQL="""
        delete from webapi where id = %(webApiId)s
        """
        getWebApiForVersionSQL="""
        select * from webapi where ApplicationId = %(applicationId)s and ProjectId=%(projectId)s and OperarionId in (select Operation from webapi_diff where ApplicationId = %(applicationId)s and ProjectId=%(projectId)s)
        """
        getWebApiInfoByIdSQL="""
        select * from webapi where id=%(webApiId)s
        """
        getWebApiListSQL="""
        select w.*,wd.DiffType from webapi w left join webapi_diff wd on w.OperationId=wd.OperationId
        where w.ApplicationId = %(applicationId)s and w.ProjectId=%(projectId)s
        """
        getWebApiRequestSQL="""
        select * from webapi_parameter where WebApiId=%(Id)s and ParameterType=1
        """
        # getWebApiRequestQuerySQL="""
        # select * from webapi_parameter where WebApiId=%(Id)s and ParameterType=1 and `In`="query"
        # """
        getWebApiResponseSQL="""
        select * from webapi_parameter where WebApiId=%(Id)s and ParameterType=2
        """
        getWebApiInfoByPathSQL="""
        select w.*,wd.DiffType from webapi w left join webapi_diff wd on w.OperationId = wd.OperationId
        where w.ApplicationId = %(applicationId)s and w.ProjectId=%(projectId)s and w.Path=%(Path)s
        """
        getWebApiPathForProjectSQL="""
        select Path from webapi where ApplicationId = %(applicationId)s and ProjectId=%(projectId)s
        """
        getWebApiInfosForCaseSQL="""
        select * from webapi left join webapi_parameter on webapi.Id= webapi_parameter.webApiId
        where webapi.ApplicationId = %(applicationId)s and webapi.ProjectId=%(projectId)s 
        and webapi.Path=%(Path)s 
        """
        #SET SQL FOR DAO
        self.data.setdefault("addWebApi",addWebApiSQL)
        self.data.setdefault("deleteWebApi",deleteWebApiSQL)
        self.data.setdefault("getWebApiForVersion",getWebApiForVersionSQL)
        self.data.setdefault("updateWebApi", updateWebApiSQL)
        self.data.setdefault("getWebApiInfoById", getWebApiInfoByIdSQL)
        self.data.setdefault("getWebApiList", getWebApiListSQL)
        self.data.setdefault("getWebApiRequest", getWebApiRequestSQL)
        # self.data.setdefault("getWebApiRequestQuery", getWebApiRequestQuerySQL)
        self.data.setdefault("getWebApiResponse", getWebApiResponseSQL)
        self.data.setdefault("getWebApiInfoByPath", getWebApiInfoByPathSQL)
        self.data.setdefault("getWebApiPathForProject", getWebApiPathForProjectSQL)
        self.data.setdefault("getWebApiInfosForCase", getWebApiInfosForCaseSQL)