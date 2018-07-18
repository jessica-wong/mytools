# -*- coding: utf-8 -*-

#CREATE TABLE `assert` (
#`id` int(11) NOT NULL auto_increment,
#`casecontentid` int(11) NOT NULL,
#`actual` varchar(255) NOT NULL,
#`expect` varchar(255) DEFAULT NULL,
#`assert_type` varchar(255) NOT NULL COMMENT '0: equal 1: not equal 2: contain 3:not contain ',
#PRIMARY KEY(`id`)
#) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

class AssertSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addAssertSQL="""
        insert into assert (casecontentid,actual,expect,assert_type,sqlcontent) 
        values (%(caseContentId)s,%(actual)s,%(expect)s,%(assertType)s,%(sqlContent)s)
        """
        deleteAssertSQL="""
        delete from assert where id = %(assertId)s
        """
        updateAssertSQL="""
        update assert set actual=%(actual)s,expect=%(expect)s,assert_type=%(assertType)s,
        sqlcontent=%(sqlContent)s where id =%(assertId)s
        """
        getAssertInfosByContentIdSQL="""
        select * from assert where casecontentid = %(contentId)s
        """
        getAssertInfoByIdSQL="""
        select * from assert where id = %(assertId)s
        """
        deleteAssertByContentIdSQL = """
        delete from assert where casecontentid = %(contentId)s
        """
        #SET SQL FOR DAO
        self.data.setdefault("addAssert",addAssertSQL)
        self.data.setdefault("deleteAssert",deleteAssertSQL)
        self.data.setdefault("updateAssert",updateAssertSQL)
        self.data.setdefault("getAssertInfosByContentId",getAssertInfosByContentIdSQL)
        self.data.setdefault("getAssertInfoById", getAssertInfoByIdSQL)
        self.data.setdefault("deleteAssertByContentId", deleteAssertByContentIdSQL)