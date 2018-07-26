# -*- coding: utf-8 -*-


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
        insert into test_case (name,create_userid,case_describe,case_status,project_id,application_id,group_id,gmt_create) 
        values(%(name)s,%(userId)s,%(desc)s,%(status)s,%(projectId)s,%(applicationId)s,%(groupId)s,now())
        """
        newInsertTestCaseSQL = """
        SELECT LAST_INSERT_ID() AS id
        """
        addTestCaseContentSQL="""
        insert into case_content (case_id,ip_url,webapi_path,method,content_type,requests_params,headers,execute_step,step_name) 
        values (%(caseId)s,%(host)s,%(path)s,%(method)s,%(content_type)s,%(params)s,%(headers)s,%(execute_step)s,%(step_name)s)
        """
        addTestCaseAssertSQL="""
        insert into assert (casecontentid,actual,expect,assert_type) values (%(contentId)s,
        %(actual)s,%(expect)s,%(type)s)
        """
        deleteTestCaseSQL="""
        delete assert,case_content,test_case from assert right join case_content on case_content.id=assert.casecontentid 
        right join test_case on case_content.case_id=test_case.id
        where test_case.id = %(caseId)s
        """
        updateTestCaseSQL="""
        update test_case set name=%(name)s,update_userid=%(userId)s,case_describe=%(desc)s,case_status=%(status)s
        where id=%(caseId)s
        """
        updateTestCaseContentSQL="""
        update case_content set ip_url=%(host)s,webapi_path=%(path)s,method=%(method)s,content_type=%(content_type)s,
        requests_params=%(params)s,headers=%(headers)s,step_name=%(step_name)s where case_id=%(caseId)s and execute_step=%(execute_step)s
        """
        updateTestCaseAssertSQL="""
        update assert set actual=%(actual)s,expect=%(expect)s,assert_type=%(type)s 
        where casecontentid=(select id from case_content where case_id=%(caseId)s and execute_step=%(execute_step)s)
        """
        deleteContentAndAssertIdByCaseIdSQL="""
        delete assert,case_content from assert right join case_content on case_content.id=assert.casecontentid 
        where case_content.case_id=%(caseId)s
        """
        getCaseInfosByConditionSQL="""
        select * from testcase where projectid = %(projectId)s and groupid= %(groupId)s 
        order by id desc limit %(offset)s,%(limit)s 
        """
        getCaseInfosByIdSQL="""
        select * from test_case where id=%(caseId)s
        """
        getInitCaseInfoByIdsSQL="""
        select * from testcase where id in (%(caseIds)s) where name="init" limit 1
        """
        getCaseDetailInfoByIdSQL="""
        select test_case.*,case_content.id as contentId,case_content.step_name,case_content.execute_step,case_content.webapi_path,case_content.ip_url,case_content.method,
        case_content.content_type,case_content.requests_params,case_content.headers,assert.actual,assert.expect,assert.assert_type,assert.casecontentid 
        from test_case left join case_content on test_case.id = case_content.case_id 
        left join assert on assert.casecontentid = case_content.id where test_case.id = %(caseId)s
        """
        getTestCaseCountSQL="""
        select count(1) as testCaseCount from test_case
        """
        getCaseListSQL="""
        select * from test_case where application_id=%(applicationId)s and project_id=%(projectId)s
        """
        searchCaseByNameSQL="""
        select * from test_case where application_id=%(applicationId)s and project_id=%(projectId)s and name like %(searchValue)s
        """
        createTestCaseSQL="""
        insert into test_case (name,case_describe,case_status,project_id,application_id,gmt_create) 
        values(%(name)s,%(desc)s,0,%(projectId)s,%(applicationId)s,now())
        """
        createTestCaseContentSQL="""
        insert into case_content (case_id,webapi_path,method,content_type,requests_params,execute_step,step_name) 
        values (%(caseId)s,%(path)s,%(method)s,%(content_type)s,%(params)s,%(execute_step)s,%(step_name)s)
        """
        createTestCaseAssertSQL="""
        insert into assert (casecontentid,actual,expect,assert_type) values (%(contentId)s,
        %(actual)s,%(expect)s,%(type)s)
        """
        getCasePathForProjectSQL="""
        select * from test_case left join case_content on test_case.id=case_content.case_id 
        where test_case.project_id = 1 and test_case.application_id =1 and case_content.webapi_path=%(Path)s
        """
        getCaseIdsSQL="""
        select id as caseId from test_case where project_id=%(projectId)s and application_id=%(applicationId)s
        """

        #SET SQL FOR DAO
        self.data.setdefault("addTestCase",addTestCaseSQL)
        self.data.setdefault("newInsertTestCase", newInsertTestCaseSQL)
        self.data.setdefault("addTestCaseContent", addTestCaseContentSQL)
        self.data.setdefault("addTestCaseAssert", addTestCaseAssertSQL)
        self.data.setdefault("deleteTestCase",deleteTestCaseSQL)
        self.data.setdefault("updateTestCase",updateTestCaseSQL)
        self.data.setdefault("updateTestCaseContent", updateTestCaseContentSQL)
        self.data.setdefault("updateTestCaseAssert", updateTestCaseAssertSQL)
        self.data.setdefault("deleteContentAndAssertIdByCaseId", deleteContentAndAssertIdByCaseIdSQL)
        self.data.setdefault("getCaseInfosByCondition", getCaseInfosByConditionSQL)
        self.data.setdefault("getCaseInfosById", getCaseInfosByIdSQL)
        self.data.setdefault("getInitCaseInfoByIds", getInitCaseInfoByIdsSQL)
        self.data.setdefault("getCaseDetailInfoById",getCaseDetailInfoByIdSQL)
        self.data.setdefault("getTestCaseCount", getTestCaseCountSQL)
        self.data.setdefault("getCaseList", getCaseListSQL)
        self.data.setdefault("searchCaseByName",searchCaseByNameSQL)
        self.data.setdefault("createTestCase", createTestCaseSQL)
        self.data.setdefault("createTestCaseContent", createTestCaseContentSQL)
        self.data.setdefault("createTestCaseAssert", createTestCaseAssertSQL)
        self.data.setdefault("getCasePathForProject", getCasePathForProjectSQL)
        self.data.setdefault("getCaseIds", getCaseIdsSQL)