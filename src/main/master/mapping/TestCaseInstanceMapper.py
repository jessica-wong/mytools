# -*- coding: utf-8 -*-
#CREATE TABLE `testcaseinstance` (
#`id` int(11) NOT NULL auto_increment,
#`create_userid` int(11) NOT NULL,
#`create_username` varchar(255) NOT NULL,
#`suite_name` varchar(255) NOT NULL,
#`suite_id` int(11) NOT NULL,
#`status` varchar(255) NOT NULL COMMENT 'wait,run,stop,fail,success,timeout,error',
#`build_start` datetime DEFAULT NULL,
#`build_end` datetime DEFAULT NULL,
#`trigger_type` tinyint(4) default 0 COMMENT '0: manual 1: ci 2:crontab',
#`gmt_create` datetime DEFAULT NULL,
#`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
#PRIMARY KEY(`id`)
#) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

class TestInstanceSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addTestInstanceSQL="""
        insert into testcaseinstance (create_userid,env_name,create_username,project_id,application_id,suite_name,suite_id,
        status,trigger_type,build_start,gmt_create) 
        values 
        (%(userId)s,%(envName)s,%(userName)s,%(projectId)s,%(applicationId)s,%(suiteName)s,%(suiteId)s,%(status)s,%(triggerType)s,now(),now())
        """
        updateTestInstanceSQL="""
        update testcaseinstance set build_start=%(build_start)s,build_end=%(build_end)s,
        status=%(status)s where id=%(instanceId)s
        """
        getTestInstanceInfoByIdSQL="""
        select testcaseinstance.*, application.name as application_name,project.name as project_name from testcaseinstance left join project on 
        project.id =testcaseinstance.project_id left join application on application.id=testcaseinstance.application_id where testcaseinstance.id =%(instanceId)s
        """
        getPengdingInstanceInfosSQL="""
        select id as instanceId,env_name as envName,project_id as projectId,application_id as applicationId from testcaseinstance where status = 0 limit 0,%(limit)s 
        """
        updateTestInstanceStatusSQL="""
        update testcaseinstance set status=%(status)s,build_end=now() where id=%(instanceId)s
        """
        getTaskInstanceInfosSQL="""
        select testcaseinstance.*, application.name as application_name,project.name as project_name from testcaseinstance left join project on 
        project.id =testcaseinstance.project_id left join application on application.id=testcaseinstance.application_id order by testcaseinstance.id desc
        """
        #SET SQL FOR DAO
        self.data.setdefault("addTestInstance",addTestInstanceSQL)
        self.data.setdefault("updateTestInstance", updateTestInstanceSQL)
        self.data.setdefault("getTestInstanceInfoById", getTestInstanceInfoByIdSQL)
        self.data.setdefault("getPengdingInstanceInfos", getPengdingInstanceInfosSQL)
        self.data.setdefault("updateTestInstanceStatus", updateTestInstanceStatusSQL)
        self.data.setdefault("getTaskInstanceInfos", getTaskInstanceInfosSQL)
