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
        insert into testcaseinstance (create_userid,create_username,suite_name,suite_id,
        status,trigger_type,gmt_create) 
        values 
        (%(userId)s,%(userName)s,%(suiteName)s,%(suiteId)s,%(status)s,%(trigger_type)s,now())
        """
        updateTestInstanceSQL="""
        update testcaseinstance set build_start=%(build_start)s,build_end=%(build_end)s,
        status=%(status)s where id=%(instanceId)s
        """
        getTestInstanceInfoByIdSQL="""
        select * from testcaseinstance where id = %(instanceId)s
        """
        #SET SQL FOR DAO
        self.data.setdefault("addTestInstance",addTestInstanceSQL)
        self.data.setdefault("updateTestInstance", updateTestInstanceSQL)
        self.data.setdefault("getTestInstanceInfoById", getTestInstanceInfoByIdSQL)
