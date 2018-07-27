# -*- coding: utf-8 -*-

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
        insert into case_result (instance_id,case_id,case_name,runtime,exe_status,
        exec_start,message,gmt_create) values (%(instanceId)s,%(caseId)s,%(caseName)s,
        %(runtime)s,%(exe_status)s,%(exec_start)s,%(message)s,now())
        """
        deleteCaseResultSQL="""
        delete from case_result where id = %(caseId)s
        """
        updateCaseResultSQL="""
        update case_result set runtime=%(runtime)s,status=%(status)s,exec_start=%(exec_start)s,
        remarks=%(remarks)s,message=%(message)s where case_id=%(caseId)s and instance_id= %(instanceId)s
        """
        getCaseResultInfoByCaseIdSQL="""
        select * from case_result where case_id = %(caseId)s
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
