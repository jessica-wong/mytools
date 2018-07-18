# -*- coding: utf-8 -*-

#CREATE TABLE `taskmetaqinfo` (
#`id` int(11) NOT NULL auto_increment,
#`instanceid` int(11) NOT NULL,
#`status` varchar(255) NOT NULL COMMENT '0 wait 1 send 2 receive',
#`running_consumer` varchar(255) DEFAULT NULL,
#`msg_id` varchar(255) DEFAULT NULL COMMENT 'process id',
#`message` text DEFAULT NULL,
#`is_deleted` tinyint(4) DEFAULT 0,
#`gmt_create` datetime DEFAULT NULL,
#`gmt_modify` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
#PRIMARY KEY(`id`)
#) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

class TaskMetaqInfoSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addTaskInfoSQL="""
        insert into taskmetaqinfo (instanceid,message,gmt_create) values (%(instanceid)s,%(message)s,now())
        """
        deleteTaskInfoSQL="""
        update taskmetaqinfo set is_deleted =1  where id = %(taskId)s
        """
        updateTaskInfoSQL="""
        update taskmetaqinfo set status=%(status)s,running_consumer=%(consumer)s,msg_id=%(processId)s where id = %(taskId)s
        """
        getWaitingTaskInfosSQL="""
        select * from taskmetaqinfo where status=0 and is_deleted =0 order by gmt_create limit %(limit)s
        """
        updateTaskStatusSQL="""
        update taskmetaqinfo set status=%(status)s where id = %(taskId)s
        """
        #SET SQL FOR DAO
        self.data.setdefault("addTaskInfo",addTaskInfoSQL)
        self.data.setdefault("deleteTaskInfo",deleteTaskInfoSQL)
        self.data.setdefault("updateTaskInfo",updateTaskInfoSQL)
        self.data.setdefault("getWaitingTaskInfos", getWaitingTaskInfosSQL)
        self.data.setdefault("updateTaskStatus", updateTaskStatusSQL)

