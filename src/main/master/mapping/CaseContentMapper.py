# -*- coding: utf-8 -*-

#CREATE TABLE `casecontent` (
#`id` int(11) NOT NULL auto_increment,
#`step_name` varchar(255) NOT NULL,
#`caseid` int(11) NOT NULL,
#`step` int(11) NOT NULL,
#`url` varchar(255) DEFAULT NULL,
#`method` tinyint(4) DEFAULT NULL COMMENT '0: GET 1: POST 2.PUT 3. DELETE',
#`format` tinyint(4) DEFAULT NULL COMMENT '0: form-data 1: json',
#`request_params` varchar(255) DEFAULT NULL,
#`timeout` int(11) DEFAULT NULL,
#`type` tinyint(4) default 0 COMMENT '0: api 1: sql',
#`sqlcontent` varchar(255) DEFAULT NULL,
#PRIMARY KEY(`id`)
#) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

class CaseContentSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addCaseContentSQL="""
        insert into casecontent (step_name,caseid,step,interfaceid,url,method,
        format,request_params,timeout,type,sqlcontent) values (%(stepName)s,%(caseId)s,
        %(step)s,%(interfaceId)s,%(url)s,%(method)s,%(format)s,%(requestParams)s,%(timeout)s,
        %(type)s,%(sqlContent)s)
        """
        deleteTestContentByContentIdSQL="""
        delete from casecontent where id = %(contentId)s
        """
        deleteTestContentByCaseIdSQL="""
        delete from casecontent where caseid = %(caseId)s
        """
        updateTestContentSQL="""
        update casecontent set step_name=%(stepName)s,step=%(step)s,interfaceid=%(interfaceId)s,url=%(url)s,
        method=%(method)s,format=%(format)s,request_params=%(requestParams)s,timeout=%(timeout)s,type=%(type)s,
        sqlcontent=%(sqlContent)s where id = %(contentId)s
        """
        getContentInfosByCaseIdSQL="""
        select * from casecontent where caseid = %(caseId)s order by step 
        """
        getContentInfosByContentIdSQL="""
        select * from casecontent where id = %(contentId)s
        """
        #SET SQL FOR DAO
        self.data.setdefault("addCaseContent",addCaseContentSQL)
        self.data.setdefault("deleteTestContentByContentId",deleteTestContentByContentIdSQL)
        self.data.setdefault("deleteTestContentByCaseId",deleteTestContentByCaseIdSQL)
        self.data.setdefault("updateTestContent",updateTestContentSQL)
        self.data.setdefault("getContentInfosByCaseId",getContentInfosByCaseIdSQL)
        self.data.setdefault("getContentInfosByContentId", getContentInfosByContentIdSQL)

