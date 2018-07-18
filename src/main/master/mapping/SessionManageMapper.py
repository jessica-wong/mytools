# -*- coding: utf-8 -*-

#CREATE TABLE `session_manage` (
#`id` int(11) NOT NULL auto_increment,
#`user_id` int(11) NOT NULL,
#`session` varchar(255) NOT NULL,
#`domain` varchar(255) DEFAULT NULL,
#`gmt_create` datetime DEFAULT NULL,
#`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
#PRIMARY KEY(`id`)
#) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

class SessionManageSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addSessionSQL="""
        insert into session_manage (user_id,session,domain,gmt_create) values 
        (%(userId)s,%(session)s,%(domain)s,now())
        """
        getSessionInfoSQL="""
        select * from session_manage where user_id = %(userId)s and domain=%(domain)s
        """
        updateSessionSQL="""
        update session_manage set session=%(session)s where user_id = %(userId)s and domain=%(domain)s
        """
        #SET SQL FOR DAO
        self.data.setdefault("addSession",addSessionSQL)
        self.data.setdefault("getSessionInfo",getSessionInfoSQL)
        self.data.setdefault("updateSession",updateSessionSQL)

