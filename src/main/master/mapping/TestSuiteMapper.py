# -*- coding: utf-8 -*-
#CREATE TABLE `testsuite` (
#`id` int(11) NOT NULL auto_increment,
#`name` varchar(255) NOT NULL unique,
#`testcaseids` text DEFAULT NULL,
#`create_userid` int(11) NOT NULL,
#`create_username` varchar(255) NOT NULL,
#`update_userid` int(11) NOT NULL,
#`update_username` varchar(255) NOT NULL,
#`status` tinyint(4) default 0 COMMENT '0: enable 1: disable',
#`remarks` varchar(255) DEFAULT NULL,
#`envid` int(11) NOT NULL,
#`gmt_create` datetime DEFAULT NULL,
#`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
#PRIMARY KEY(`id`)
#) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

#ALTER TABLE `testsuite` ADD unique(`name`);

class TestSuiteSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addTestSuiteSQL="""
        insert into testsuite (name,testcaseids,create_userid,status,remarks,envid,projectid,gmt_create) 
        values (%(name)s,%(caseIds)s,%(userId)s,%(status)s,%(remarks)s,%(envId)s,%(projectId)s,now())
        """
        updateTestSuiteSQL="""
        update testsuite set name=%(name)s,update_userid=%(userId)s,testcaseids=%(caseIds)s,
        status=%(status)s,remarks=%(remarks)s,envid=%(envId)s,projectid=%(projectId)s where id=%(suiteId)s
        """
        deleteTestSuiteSQL="""
        delete from testsuite where id = %(suiteId)s
        """
        getSuiteInfoByIdSQL="""
        select * from testsuite where id = %(suiteId)s
        """
        getSuiteListSQL="""
        select * from testsuite
        """
        editTestSuiteNameSQL="""
        update testsuite set name=%(name)s where id=%(suiteId)s
        """

        #SET SQL FOR DAO
        self.data.setdefault("addTestSuite",addTestSuiteSQL)
        self.data.setdefault("updateTestSuite", updateTestSuiteSQL)
        self.data.setdefault("deleteTestSuite", deleteTestSuiteSQL)
        self.data.setdefault("getSuiteInfoById", getSuiteInfoByIdSQL)
        self.data.setdefault("getSuiteList",getSuiteListSQL)
        self.data.setdefault("editTestSuiteName", editTestSuiteNameSQL)
