# -*- coding: utf-8 -*-

# CREATE TABLE `application` (
# `id` int(11) NOT NULL auto_increment,
# `name` varchar(255) NOT NULL unique,
# `application_describe` varchar(255) DEFAULT NULL,
# `create_username` varchar(255) NOT NULL,
# `remarks` varchar(255) DEFAULT NULL,
# `gmt_create` datetime DEFAULT NULL,
# `gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
# PRIMARY KEY(`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
# ALTER TABLE `application` ADD unique(`name`);
#
# CREATE TABLE `application_version` (
# `id` int(11) NOT NULL auto_increment,
# `application_id` int(11) NOT NULL,
# `project_id` int(11) NOT NULL,
# `department_id` int(11) NOT NULL,
# `create_userid` int(11) NOT NULL,
# `create_username` varchar(255) NOT NULL,
# `remarks` varchar(255) DEFAULT NULL,
# `gmt_create` datetime DEFAULT NULL,
# `gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
# PRIMARY KEY(`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

class ApplicationSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addApplicationSQL="""
        insert into application (name,application_describe,department_id,gmt_create) values (%(applicationName)s,%(applicationDescribe)s,%(departmentId)s,now())
        """
        addApplicationVersionSQL="""
        insert into application_version (application_id,project_id,department_id,gmt_create) values (%(applicationId)s,%(projectId)s,%(departmentId)s,now())
        """
        getApplicationListSQL="""
        select application.* from application left join user on application.department_id=user.department_id where user.id=%(userId)s
        """
        getApplicationListLeaderSQL="""
        select * from application
        """

        getApplicationByProjectIdSQL="""
        select application.name,application_version.application_id,version_config.git_url,version_config.swagger_url,version_config.test_url 
        from application inner join application_version on 
        application.id=application_version.application_id
        left join version_config on 
        application_version.application_id=version_config.application_id
        where application_version.project_id=%(projectId)s
        """
        getInterfaceCountByApplicationVersionSQL="""
        select count(1) from interface where projectid=%(projectId)s and application_id=%(applicationId)s
        """
        deleteApplicationVersionSQL="""
        delete from application_version where project_id=%(projectId)s and application_id=%(applicationId)s
        """
        addApplicationVersionConfigSQL="""
        insert into version_config (application_id,project_id,git_url,swagger_url,test_url,gmt_create) values (%(application_id)s,%(project_id)s,%(git_url)s,%(swagger_url)s,%(test_url)s,now())
        """
        editVersionConfigSQL="""
        update version_config set git_url=%(git_url)s,swagger_url=%(swagger_url)s,test_url=%(test_url)s where id=%(id)s
        """
        getVersionConfigSQL="""
        select * from version_config where project_id=%(projectId)s and application_id=%(applicationId)s
        """
        getApplicationCountByProjectSQL="""
        select count(1) as count from application_version where project_id=%(projectId)s
        """
        getApplicationCountSQL="""
        select count(1) as applicationCount from application
        """
        getApplicationByIdSQL="""
        select * from application where id=%(Id)s
        """
        editApplicationSQL="""
        update application set application_describe=%(applicationDescribe)s, 
        name=%(applicationName)s,department_id=%(departmentId)s where id=%(id)s
        """
        deleteApplicationSQL="""
        delete from application where id=%(id)s
        """

        #SET SQL FOR DAO
        self.data.setdefault("addApplication",addApplicationSQL)
        self.data.setdefault("addApplicationVersion", addApplicationVersionSQL)
        self.data.setdefault("getApplicationList", getApplicationListSQL)
        self.data.setdefault("getApplicationListLeader", getApplicationListLeaderSQL)
        self.data.setdefault("getApplicationByProjectId", getApplicationByProjectIdSQL)
        self.data.setdefault("getInterfaceCountByApplicationVersion", getInterfaceCountByApplicationVersionSQL)
        self.data.setdefault("deleteApplicationVersion",deleteApplicationVersionSQL)
        self.data.setdefault("addApplicationVersionConfig", addApplicationVersionConfigSQL)
        self.data.setdefault("editVersionConfig", editVersionConfigSQL)
        self.data.setdefault("getVersionConfig", getVersionConfigSQL)
        self.data.setdefault("getApplicationCountByProject", getApplicationCountByProjectSQL)
        self.data.setdefault("getApplicationCount", getApplicationCountSQL)
        self.data.setdefault("getApplicationById", getApplicationByIdSQL)
        self.data.setdefault("editApplication", editApplicationSQL)
        self.data.setdefault("deleteApplication", deleteApplicationSQL)