# -*- coding: utf-8 -*-

#CREATE TABLE `caseresult` (
#`id` int(11) NOT NULL auto_increment,
#`instanceid` int(11) NOT NULL,
#`caseid` int(11) NOT NULL,
#`casename` varchar(255) NOT NULL,
#`runtime` int(11) DEFAULT NULL,
#`status` varchar(255) NOT NULL COMMENT 'wait,run,stop,fail,success,timeout,error,skip',
#`exec_start` datetime DEFAULT NULL,
#`exec_end` datetime DEFAULT NULL,
#`message` text DEFAULT NULL,
#`remarks` varchar(255) DEFAULT NULL,
#`gmt_create` datetime DEFAULT NULL,
#`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
#PRIMARY KEY(`id`)
#) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

class CaseResultSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addCaseResultSQL="""
        insert into caseresult (instanceid,caseid,casename,runtime,status,
        exec_start,exec_end,remarks,message,gmt_create) values (%(instanceid)s,%(caseid)s,%(casename)s,
        %(runtime)s,%(status)s,%(exec_start)s,%(exec_end)s,%(remarks)s,%(messaga)s,now())
        """
        deleteCaseResultSQL="""
        delete from caseresult where id = %(caseId)s
        """
        updateCaseResultSQL="""
        update caseresult set runtime=%(runtime)s,status=%(status)s,exec_start=%(exec_start)s,
        exec_end=%(exec_end)s,remarks=%(remarks)s,message=%(message)s where caseid=%(caseId)s
        and instanceid= %(instanceId)s
        """
        getCaseResultInfoByCaseIdSQL="""
        select * from testcase where projectid = %(projectId)s and type = %(type)s
        """
        getCaseResultInfosByConditionSQL="""
        select * from testcase where projectid = %(projectId)s and type = %(type)s
        """
        #SET SQL FOR DAO
        self.data.setdefault("addCaseResult",addCaseResultSQL)
        self.data.setdefault("deleteCaseResult",deleteCaseResultSQL)
        self.data.setdefault("updateCaseResult",updateCaseResultSQL)
        self.data.setdefault("getCaseResultInfoByCaseId",getCaseResultInfoByCaseIdSQL)
        self.data.setdefault("getCaseResultInfosByCondition", getCaseResultInfosByConditionSQL)
