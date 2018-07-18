# -*- coding: utf-8 -*-

#CREATE TABLE `testcase` (
#`id` int(11) NOT NULL auto_increment,
#`name` varchar(255) NOT NULL,
#`create_userid` int(11) NOT NULL,
#`create_username` varchar(255) NOT NULL,
#`update_userid` int(11) NOT NULL,
#`update_username` varchar(255) NOT NULL,
#`describe` varchar(255) NOT NULL,
#`status` tinyint(4) default 0 COMMENT '0: enable 1: disable',
#`remarks` varchar(255) DEFAULT NULL,
#`projectid` int(11) NOT NULL,
#`groupid` int(11) NOT NULL,
#`envid` int(11) DEFAULT NULL,
#`gmt_create` datetime DEFAULT NULL,
#`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
#PRIMARY KEY(`id`)
#) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

class TestCaseSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addTestCaseSQL="""
        insert into testcase (name,create_userid,case_describe,status,remarks,projectid,groupid,envid,gmt_create) 
        values(%(name)s,%(userId)s,%(describe)s,%(status)s,%(remarks)s,%(projectId)s,%(groupId)s,%(envId)s,now())
        """
        deleteTestCaseSQL="""
        delete from testcase where id = %(caseId)s
        """
        updateTestCaseSQL="""
        update testcase set name=%(name)s,update_userid=%(userId)s,case_describe=%(describe)s,status=%(status)s,
        remarks=%(remarks)s,envid=%(envid)s where id=%(caseId)s
        """
        getCaseInfosByConditionSQL="""
        select * from testcase where projectid = %(projectId)s and groupid= %(groupId)s 
        order by id desc limit %(offset)s,%(limit)s 
        """
        getCaseInfosByIdSQL="""
        select * from testcase where id=%(caseId)s
        """
        getInitCaseInfoByIdsSQL="""
        select * from testcase where id in (%(caseIds)s) where name="init" limit 1
        """
        getCaseDetailInfoByIdSQL="""
        select testcase.*,casecontent.id as contentId,casecontent.step_name,casecontent.step,casecontent.interfaceid,casecontent.url,casecontent.method,
        casecontent.format,casecontent.request_params,casecontent.type,casecontent.sqlcontent,casecontent.response_type,
        assert.actual,assert.expect,assert.assert_type,assert.casecontentid from testcase left join casecontent on testcase.id = casecontent.caseid 
        left join assert on assert.casecontentid = casecontent.id where testcase.id = %(caseId)s
        """
        getTestCaseCountSQL="""
        select count(1) as testCaseCount from testcase
        """
        getCaseListSQL="""
        select * from test_case where application_id=%(applicationId)s and project_id=%(projectId)s
        """

        #SET SQL FOR DAO
        self.data.setdefault("addTestCase",addTestCaseSQL)
        self.data.setdefault("deleteTestCase",deleteTestCaseSQL)
        self.data.setdefault("updateTestCase",updateTestCaseSQL)
        self.data.setdefault("getCaseInfosByCondition", getCaseInfosByConditionSQL)
        self.data.setdefault("getCaseInfosById", getCaseInfosByIdSQL)
        self.data.setdefault("getInitCaseInfoByIds", getInitCaseInfoByIdsSQL)
        self.data.setdefault("getCaseDetailInfoById",getCaseDetailInfoByIdSQL)
        self.data.setdefault("getTestCaseCount", getTestCaseCountSQL)
        self.data.setdefault("getCaseList", getCaseListSQL)
