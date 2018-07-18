# -*- coding: utf-8 -*-

#CREATE TABLE `cooperation` (
#`id` int(11) NOT NULL auto_increment,
#`name` varchar(255) NOT NULL unique,
#`url` varchar(255) NOT NULL,
#`datatemplate` longtext default NULL,
#`dbname` varchar(255) DEFAULT NULL,
#`dbhostname` varchar(255) DEFAULT NULL,
#`dbport` varchar(255) DEFAULT NULL,
#`dbusername` varchar(255) DEFAULT NULL,
#`dbpasswd` varchar(255) DEFAULT NULL,
#`create_userid` int(11) NOT NULL,
#`create_username` varchar(255) NOT NULL,
#`gmt_create` datetime DEFAULT NULL,
#`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
#PRIMARY KEY(`id`)
#) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

#ALTER TABLE `cooperation` ADD unique(`name`);

class EnvironmentSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addEnvironmentItemSQL="""
        insert into cooperation (name,url,create_userid,datatemplate,dbname,dbhostname,dbport,dbusername,dbpasswd,gmt_create) 
        values (%(name)s,%(url)s,%(userId)s,%(template)s,%(dbname)s,%(dbhostname)s,%(dbport)s,%(dbusername)s,%(dbpasswd)s,now())
        """
        deleteEnvironmentItemSQL="""
        delete from cooperation where id = %(envId)s
        """
        editEnvironmentItemSQL="""
        update cooperation set name=%(name)s,url=%(url)s,datatemplate=%(template)s,dbname=%(dbname)s,
        dbhostname=%(dbhostname)s,dbport=%(dbport)s,dbusername=%(dbusername)s,dbpasswd=%(dbpasswd)s 
        where id=%(envId)s
        """
        getEnvironmentInfoByIdSQL="""
        select * from cooperation where id = %(envId)s
        """
        getEnvironmentInfosSQL="""
        select * from cooperation
        """

        getEnvironmentInfosByUserIdSQL="""
        select * from cooperation where create_userid=%(userId)s
        """

        #SET SQL FOR DAO
        self.data.setdefault("addEnvironmentItem",addEnvironmentItemSQL)
        self.data.setdefault("deleteEnvironmentItem",deleteEnvironmentItemSQL)
        self.data.setdefault("editEnvironmentItem",editEnvironmentItemSQL)
        self.data.setdefault("getEnvironmentInfoById",getEnvironmentInfoByIdSQL)
        self.data.setdefault("getEnvironmentInfos", getEnvironmentInfosSQL)
        self.data.setdefault("getEnvironmentInfosByUserId",getEnvironmentInfosByUserIdSQL)

