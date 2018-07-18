# -*- coding: utf-8 -*-

# CREATE TABLE `business` (
# `id` TINYINT(4) NOT NULL auto_increment,
# `businessName` varchar(255) NOT NULL,
# PRIMARY KEY(`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
#
#
# CREATE TABLE `product` (
# `id` int(11) NOT NULL auto_increment,
# `productName` varchar(255) NOT NULL,
# `businessUnit` TINYINT(4) default 0 NOT NULL,
# PRIMARY KEY(`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

class ProductSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addProductSQL="""
        insert into product (productName,businessUnit) 
        values (%(productName)s,%(businessUnit)s)
        """

        deleteProductSQL="""
        delete from product where id = %(id)s
        """
        getProductInfoByIdSQL="""
        select * from product where id = %(id)s
        """
        getProductListSQL="""
        select * from product where businessUnit = %(businessUnit)s 
        """

        editProductSQL="""
        update product set name=%(productName)s,businessUnit=%(businessUnit)s where id=%(id)s
        """

        #SET SQL FOR DAO
        self.data.setdefault("addProduct",addProductSQL)
        self.data.setdefault("deleteProduct",deleteProductSQL)
        self.data.setdefault("getProductInfoById",getProductInfoByIdSQL)
        self.data.setdefault("getProductList", getProductListSQL)
        self.data.setdefault("editProduct", editProductSQL)

