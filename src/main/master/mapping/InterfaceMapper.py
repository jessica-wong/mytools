# -*- coding: utf-8 -*-

#CREATE TABLE `interface` (
#`id` int(11) NOT NULL auto_increment,
#`name` varchar(255) NOT NULL,
#`url` varchar(255) NOT NULL,
#`create_userid` int(11) NOT NULL,
#`create_username` varchar(255) NOT NULL,
#`update_userid` int(11) NOT NULL,
#`update_username` varchar(255) NOT NULL,
#`describe` varchar(255) NOT NULL,
#`params` text DEFAULT NULL,
#`success_response` text DEFAULT NULL,
#`failure_response` text DEFAULT NULL,
#`method` tinyint(4) NOT NULL COMMENT '0: GET 1: POST 2.PUT 3. DELETE',
#`format` tinyint(4) NOT NULL COMMENT '0: form-data 1: json',
#`response_type` tinyint(4) default 0 COMMENT '0: json 1: view',
#`status` tinyint(4) default 0 COMMENT '0: enable 1: disable',
#`remarks` varchar(255) DEFAULT NULL,
#`projectid` int(11) NOT NULL,
#`groupid` int(11) NOT NULL,
#`gmt_create` datetime DEFAULT NULL,
#`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
#PRIMARY KEY(`id`)
#) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

class InterfaceSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addInterfaceItemSQL="""
        insert into interface (name,url,create_userid,interface_describe,params,success_response,failure_response,
        method,format,response_type,status,remarks,projectid,groupid,gmt_create,create_username) 
        values (%(name)s,%(url)s,%(create_userid)s,%(describe)s,%(params)s,%(success_response)s,%(failure_response)s,
        %(method)s,%(format)s,%(response_type)s,%(status)s,%(remarks)s,%(projectid)s,%(groupid)s,now(),%(create_username)s)
        """
        updateInterfaceItemSQL="""
        update interface set name=%(name)s,url=%(url)s,update_userid=%(userId)s,interface_describe=%(describe)s,
        params=%(params)s,success_response=%(success_response)s,failure_response=%(failure_response)s,method=%(method)s,
        format=%(format)s,response_type=%(response_type)s,status=%(status)s,remarks=%(remarks)s where id =%(interfaceId)s
        """
        deleteInterfaceItemSQL="""
        delete from interface where id = %(interfaceId)s
        """
        getInterfaceInfoByIdSQL="""
        select * from interface where id = %(interfaceId)s
        """
        enableInterfaceItemSQL="""
        update interface set status= %(status)s where id=%(interfaceId)s
        """
        disableInterfaceItemSQL="""
        update interface set status= 1 where id=%(interfaceId)s
        """
        getInterfaceInfosByProjectSQL="""
        select * from interface where projectid=%(projectId)s and groupid=%(groupId)s 
        order by id desc limit %(offset)s,%(limit)s
        """
        setInterfaceGroupSQL="""
        update interface set groupid=%(groupId)s where id = %(interfaceId)s
        """

        #SET SQL FOR DAO
        self.data.setdefault("addInterfaceItem",addInterfaceItemSQL)
        self.data.setdefault("deleteInterfaceItem",deleteInterfaceItemSQL)
        self.data.setdefault("getInterfaceInfoById",getInterfaceInfoByIdSQL)
        self.data.setdefault("updateInterfaceItem", updateInterfaceItemSQL)
        self.data.setdefault("enableInterfaceItem", enableInterfaceItemSQL)
        self.data.setdefault("disableInterfaceItem", disableInterfaceItemSQL)
        self.data.setdefault("getInterfaceInfosByProject", getInterfaceInfosByProjectSQL)
        self.data.setdefault("setInterfaceGroup",setInterfaceGroupSQL)