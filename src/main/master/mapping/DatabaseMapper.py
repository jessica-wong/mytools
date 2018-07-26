# -*- coding: utf-8 -*-

# todo 注意关键字重名，如database,schema
# create table column_link
# (
# 	id int auto_increment
# 		primary key,
# 	src_column_id int default '0' not null comment '数据源字段Id',
# 	src_table_id int default '0' not null comment '数据源表Id',
# 	relation_type tinyint not null comment '关系类型: 1外键关系, 2数据关系',
# 	link_column_id int default '0' not null comment '关联字段Id',
# 	link_table_id int default '0' not null comment '关联表Id'
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
# comment '字段关系表'
# ;
#
# create table db_column
# (
# 	id int auto_increment
# 		primary key,
# 	table_id int default '0' not null comment '关联表Id',
# 	e_name varchar(255) not null comment '字段英文名',
# 	type varchar(32) not null comment '字段数据类型',
# 	remark varchar(1024) not null comment '字段备注',
# 	discarded tinyint not null comment '字段废弃: 0未废弃, 1废弃',
# 	hide tinyint default '0' null comment '字段在外联关系视图中是否可见: 0不可见 1可见',
#   unlink tinyint default '0' null comment '字段在外联关系视图中是否显示关联: 0关联 1不关联',
# 	gmt_create datetime null comment '创建时间',
# 	gmt_modify timestamp default CURRENT_TIMESTAMP not null comment '修改时间'
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
# comment '字段表'
# ;
#
# create table db_log
# (
# 	id int auto_increment
# 		primary key,
# 	db_id int default '0' not null comment '关联数据库Id',
# 	content text not null comment '操作内容',
# 	user_id int default '0' not null comment '操作人',
# 	gmt_create datetime null comment '操作时间'
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
# comment '数据库日志表'
# ;
#
# create table db_manage
# (
# 	id int auto_increment
# 		primary key,
# 	name varchar(255) not null comment '自定义连接名',
# 	host varchar(255) not null comment '主机名',
# 	port int(4) default '0' not null comment '端口号',
# 	username varchar(32) not null comment '连接用户名',
# 	password varchar(128) not null comment '连接密码',
# 	schema_name varchar(32) not null comment '实例名',
# 	business_unit tinyint default '0' not null comment '关联事业线Id',
# 	product_unit tinyint default '0' not null comment '关联产品Id',
# 	match_rule varchar(255) null comment '自动生成关联关系规则，用,隔开'
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
# comment '数据库表'
# ;
#
# create table db_table
# (
# 	id int auto_increment
# 		primary key,
# 	db_id int default '0' not null comment '关联数据库Id',
# 	c_name varchar(255) not null comment '表中文名',
# 	e_name varchar(255) not null comment '表英文名',
# 	remark varchar(1024) not null comment '表备注',
# 	discarded tinyint not null comment '表废弃: 0未废弃, 1废弃',
# 	gmt_create datetime null comment '创建时间',
# 	gmt_modify timestamp default CURRENT_TIMESTAMP not null comment '修改时间'
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
# comment '表信息表'
# ;
#
# create table table_group
# (
# 	id int auto_increment
# 		primary key,
# 	db_id int default '0' not null comment '关联数据库Id',
# 	name varchar(64) not null comment '分组名',
# 	define tinyint default '0' not null comment '自定义: 0不是, 是',
# 	sort tinyint default '0' null comment '排序'
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
# comment '分组表'
# ;
#
# create table table_group_relation
# (
# 	id int auto_increment
# 		primary key,
# 	table_id int default '0' not null comment '关联表Id',
# 	group_id int default '0' not null comment '关联分组Id'
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
# comment '表-分组关系表'
# ;

# alter  table  column_link add unique index link_unique_index(src_column_id,src_table_id,link_column_id,link_table_id,relation_type);


class DatabaseSQLMapper:

    def __init__(self):
        self.data={}
        self.__setSQL()

    def getSQL(self,key):
        return self.data.get(key)

    #define: function name=sql string
    #为了安全性，设置为私有方法
    def __setSQL(self):
        #WRITE SQL FOR API
        addDatabaseSQL="""
        insert into db_manage (name,host,port,username,password,schema_name,business_unit,product_unit) 
        values (%(name)s,%(host)s,%(port)s,%(username)s,%(password)s,%(schema_name)s,%(business_unit)s,%(product_unit)s);
        """

        deleteDatabaseSQL="""
        delete from db_manage where id = %(id)s;
        """

        getDatabaseInfoByIdSQL = """
        select id,name,host,port,username,schema_name,business_unit,product_unit from db_manage where id = %(id)s;
        """

        getDatabaseAllInfoByIdSQL = """
        select * from db_manage where id = %(id)s;
        """

        getDatabasePwdByIdSQL = """
        select id,password from db_manage where id = %(id)s;
        """

        getDatabaseListSQL = """
        select id,name,host,port,username,schema_name,business_unit,product_unit from db_manage where business_unit = %(business_unit)s;
        """

        editDatabaseSQL = """
        update db_manage set name=%(name)s,host=%(host)s,port=%(port)s,username=%(username)s,schema_name=%(schema_name)s,
        business_unit=%(business_unit)s,product_unit=%(product_unit)s,match_rule=%(match_rule)s where id=%(id)s;
        """

        editDatabasePwdByIdSQL = """
        update db_manage set password=%(password)s where id=%(id)s;
        """

        addTableGroupSQL = """
        insert into table_group (db_id,name,define,sort) 
        values (%(db_id)s,%(name)s,%(define)s,%(sort)s);
        """

        deleteTableGroupSQL = """
        delete from table_group where id = %(id)s;
        """

        getTableGroupInfoByIdSQL = """
        select * from table_group where id = %(id)s;
        """

        getTableGroupInfoByNameSQL = """
        select * from table_group where db_id = %(db_id)s and name = %(name)s;
        """

        getTableGroupListSQL = """
        select * from table_group where db_id = %(db_id)s order by sort;
        """

        editTableGroupSQL = """
        update table_group set db_id=%(db_id)s,name=%(name)s,sort=%(sort)s where id=%(id)s;
        """

        addTableGroupRelationSQL = """
        insert into table_group_relation (table_id,group_id) 
        values (%(table_id)s,%(group_id)s);
        """

        deleteTableGroupRelationSQL = """
        delete from table_group_relation where id = %(id)s;
        """

        getTableGroupRelationListSQL = """
        select tgr.*,tg.*,t.e_name,t.c_name,tg.id 'tg_id' from table_group_relation tgr join table_group tg 
         on tgr.group_id = tg.id join db_table t on t.id = tgr.table_id
         where tg.db_id = %(db_id)s order by tg.sort,t.id;
        """

        updateTableGroupRelationSQL = """
        update table_group_relation set group_id=%(group_id)s where find_in_set(id,%(ids)s) ;
        """

        updateTableGroupRelationByGroupIdSQL = """
        update table_group_relation set group_id=%(dest_group_id)s where group_id=%(src_group_id)s ;
        """

        deleteTableGroupByDBSQL = """
        DELETE FROM table_group where db_id = %(id)s; 
        """

        deleteTableGroupRelationByDBSQL = """
        DELETE FROM table_group_relation where table_id in (SELECT id from db_table where db_id = %(id)s); 
        """

        addTableSQL = """
        insert into db_table (db_id,c_name,e_name,remark,discarded,gmt_create,gmt_modify) 
        values (%(db_id)s,%(c_name)s,%(e_name)s,%(remark)s,%(discarded)s,now(),now());
        """

        deleteTableSQL = """
        delete from db_table where id = %(id)s;
        """

        getTableInfoByIdSQL = """
        select * from db_table where id = %(id)s;
        """

        getTableInfoByNameSQL = """
        select * from db_table where db_id = %(db_id)s and e_name = %(e_name)s;
        """

        getTableListSQL = """
        select * from db_table where db_id = %(db_id)s;
        """

        editTableSQL = """
        update db_table set db_id=%(db_id)s,c_name=%(c_name)s,e_name=%(e_name)s,remark=%(remark)s,
        discarded=%(discarded)s,gmt_modify=%(gmt_modify)s where id=%(id)s;
        """

        editTableByNameSQL = """
        update db_table set c_name=%(c_name)s,remark=%(remark)s,
        gmt_modify=now() where db_id=%(db_id)s and e_name=%(e_name)s;
        """

        editTableCNameByIdSQL = """
        update db_table set c_name=%(c_name)s,
        gmt_modify=now() where id=%(id)s;
        """
        editTableRemarkByIdSQL = """
        update db_table set remark=%(remark)s,
        gmt_modify=now() where id=%(id)s;
        """

        discardTableByNameSQL = """
        update db_table set discarded=1,
        gmt_modify=now() where db_id=%(db_id)s and e_name=%(e_name)s;
        """

        addColumnSQL = """
        insert into db_column (table_id,e_name,type,remark,discarded,gmt_create,gmt_modify) 
        values (%(table_id)s,%(e_name)s,%(type)s,%(remark)s,%(discarded)s,now(),now());
        """

        deleteColumnSQL = """
        delete from db_column where id = %(id)s;
        """

        getColumnInfoByIdSQL = """
        select * from db_column where id = %(id)s;
        """

        getColumnInfoByEnameSQL = """
        select dc.* from db_column dc 
        join db_table dt on dt.id = dc.table_id 
        where dc.e_name=%(e_name)s and dt.db_id=%(db_id)s;
        """

        getIdColumnInfoByTableNameSQL = """
        select dc.* from db_column dc 
        join db_table dt on dt.id = dc.table_id 
        where dt.e_name=%(e_name)s and dt.db_id=%(db_id)s and dc.e_name='id';
        """

        getIdColumnListByTableNameSQL = """
        select dc.id 'cl_id', dt.id 't_id', dc.e_name 'cl_name', dt.e_name 't_name' from db_column dc 
        join db_table dt on dt.id = dc.table_id 
        where dt.db_id=%(db_id)s and dc.e_name='id';
        """

        # todo 要改， 在service里做处理
        getColumnListByTableIdSQL = """
          select dc.*,cl.id 'cl_id',cl.link_table_id 'tb_id',dm.name 'db_name',dt.e_name 'tb_name',dc2.e_name 'col_name',dm.id 'db_id' from db_column dc
          left join column_link cl on cl.src_column_id = dc.id
          left join db_column dc2 on dc2.id = cl.link_column_id
          left join db_table dt on dt.id = cl.link_table_id
          left join db_manage dm on dm.id = dt.db_id where dc.table_id = %(table_id)s
        UNION
          select dc.*,cl.id 'cl_id',cl.src_table_id 'tb_id',dm.name 'db_name',dt.e_name 'tb_name',dc2.e_name 'col_name',dm.id 'db_id' from db_column dc
          left join column_link cl on cl.link_column_id = dc.id
          left join db_column dc2 on dc2.id = cl.src_column_id
          left join db_table dt on dt.id = cl.src_table_id
          left join db_manage dm on dm.id = dt.db_id where dc.table_id = %(table_id)s;
        """

        getColumnListByTableNameSQL = """
        select dc.* from db_column dc join db_table dt on dc.table_id = dt.id 
        where dt.e_name=%(e_name)s and dt.db_id=%(db_id)s;
        """

        editColumnSQL = """
        update db_column set table_id=%(table_id)s,e_name=%(e_name)s,type=%(type)s, 
        remark=%(remark)s,discarded=%(discarded)s,gmt_modify=now() where id=%(id)s;
        """

        editColumnRemarkByIdSQL = """
        update db_column set remark=%(val)s, gmt_modify=now() where id=%(id)s;
        """

        editColumnTypeByIdSQL = """
        update db_column set type=%(val)s, gmt_modify=now() where id=%(id)s;
        """

        editColumnDiscardByIdSQL = """
        update db_column set discarded=%(val)s, gmt_modify=now() where id=%(id)s;
        """

        editColumnHideByIdSQL = """
        update db_column set hide=%(val)s where id=%(id)s;
        """

        editColumnUnlinkByIdSQL = """
        update db_column set unlink=%(val)s where id=%(id)s;
        """

        isInitSynchronizeSQL = """
        SELECT count(*) as tableCount from db_table WHERE db_id = %(db_id)s;
        """

        getSynchronizeDatabaseSQL = """
        SELECT TABLE_NAME,TABLE_COMMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %(schema_name)s;
        """

        getSynchronizeTableSQL = """
        SELECT COLUMN_NAME,COLUMN_TYPE, COLUMN_COMMENT from information_schema.columns 
        where TABLE_SCHEMA = %(schema_name)s and TABLE_NAME= %(table_name)s;
        """

        getSynchronizeColumnSQL = """
        SELECT COLUMN_NAME, COLUMN_TYPE, COLUMN_COMMENT from information_schema.columns 
        where TABLE_SCHEMA = %(schema_name)s and TABLE_NAME = %(table_name)s and COLUMN_NAME = %(columnName)s;
        """

        getTableCommentSQL = """
        SELECT TABLE_NAME,TABLE_COMMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %(schema_name)s
         and TABLE_NAME = %(table_name)s;
        """

        addTableRouteSQL = """
        values (%(route_id)s,%(node_id)s,%(node_order)s);
        """

        addDataNodeSQL = """
        insert into data_node (data_module,data_operation) 
        values (%(data_module)s,%(data_operation)s);
        """

        addDataRouteSQL = """
        insert into data_route (table_id) values (%(table_id)s);
        """

        getTableRouteListSQL = """
        SELECT * FROM data_route dr JOIN table_route tr on tr.route_id = dr.id
        JOIN data_node dn on dn.id = tr.node_id WHERE dr.table_id = %(table_id)s
        order by tr.route_id,tr.node_order;
        """

        getSearchByTableSQL = """
        SELECT t.id as uid, t.id,t.e_name from db_table t join db_column c on t.id = c.table_id where db_id=%(db_id)s 
         and t.e_name like %(e_name)s GROUP BY t.id;
        """

        # todo 待改
        getSearchByTableColumnSQL = """
        SELECT c.id as uid, t.id,concat(t.e_name,'.',c.e_name) as e_name from db_table t join db_column c on t.id = c.table_id 
         where db_id=%(db_id)s and t.e_name = %(tb_e_name)s and c.e_name like %(col_e_name)s;
        """

        # todo 待改
        getSearchByColumnSQL = """
        SELECT c.id as uid, t.id,concat(t.e_name,'.',c.e_name) as e_name from db_table t join db_column c on t.id = c.table_id 
         where db_id=%(db_id)s and c.e_name like %(e_name)s;
        """

        # todo 待改
        getSearchByColumnRemarkSQL = """
        SELECT c.id as uid, t.id,concat(t.e_name,'.',c.e_name,'  #',left(c.remark,15),'...') as e_name from db_table t join db_column c on t.id = c.table_id 
         where db_id=%(db_id)s and c.remark like %(remark)s;
        """

        addDBLogSQL = """
        insert into db_log (db_id,content,user_id,gmt_create) 
        values (%(db_id)s,%(content)s,%(user_id)s,now());
        """

        # todo 待改
        getDBLogListSQL = """
        select concat(if(username is NULL,"自动",username),"在",dl.gmt_create,content) as content from db_log dl
          left join user u on u.id = dl.user_id
          where db_id = %(db_id)s order by dl.gmt_create desc;
        """

        addColumnLinkSQL = """
        insert ignore into column_link (src_column_id,src_table_id,relation_type,link_column_id,link_table_id) 
        values (%(src_column_id)s,%(src_table_id)s,%(relation_type)s,%(link_column_id)s,%(link_table_id)s);
        """

        deleteColumnLinkSQL = """
        delete from column_link where id=%(id)s;
        """

        # todo 新库是子表，不要显示
        getLinkDBListSQL = """

        """

        getLinkTableListSQL = """
        SELECT distinct dt.id, dt.e_name from column_link cl join db_table dt on dt.id = cl.link_table_id 
        and dt.db_id = %(db_id)s;
        """

        getLinkColumnListSQL = """
        SELECT distinct dc.id, dc.e_name from column_link cl join db_column dc on dc.id = cl.link_column_id 
        and dc.table_id = %(table_id)s;
        """

        getTableListByTableNameSQL = """
        SELECT dt.id, dt.e_name from db_table dt where
        dt.db_id = %(db_id)s and dt.e_name like %(e_name)s;
        """

        getColumnListByColNameSQL = """
        SELECT dc.id, dc.e_name from db_column dc where
        dc.table_id = %(table_id)s and dc.e_name like %(e_name)s;
        """

        deleteColumnSQL = """
        DELETE FROM db_column where table_id in (SELECT id from db_table where db_id = %(id)s); 
        """

        deleteTableSQL = """
        DELETE FROM db_table where db_id = %(id)s; 
        """

        getViewLinksSQL = """
        select sc.e_name 'src_col_name',st.e_name 'src_tb_name',lc.e_name 'link_col_name',lt.e_name 'link_tb_name' from column_link cl
            join db_column sc on sc.id = cl.src_column_id and sc.unlink = 0 and sc.discarded = 0 
            join db_table st on st.id = cl.src_table_id and st.discarded = 0 
            join db_column lc on lc.id = cl.link_column_id and lc.unlink = 0 and lc.discarded = 0
            join db_table lt on lt.id = cl.link_table_id and lt.discarded = 0
         where src_table_id = %(table_id)s and relation_type = 1
        union
        select sc.e_name 'src_col_name',st.e_name 'src_tb_name',lc.e_name 'link_col_name',lt.e_name 'link_tb_name' from column_link cl
            join db_column sc on sc.id = cl.src_column_id and sc.unlink = 0 and sc.discarded = 0 
            join db_table st on st.id = cl.src_table_id and st.discarded = 0 
            join db_column lc on lc.id = cl.link_column_id and lc.unlink = 0 and lc.discarded = 0 
            join db_table lt on lt.id = cl.link_table_id and lt.discarded = 0 
          where relation_type = 1 and src_table_id in
            (select link_table_id from column_link where src_table_id = %(table_id)s and relation_type = 1)
        ;
        """

        getViewTableInfoSQL = """
        select DISTINCT(dc.id),dt.id, dt.e_name 'name', dc.e_name, dc.type, t.link_type, dm.name 'db_name',dc.hide, dc.unlink from
            (select src_table_id 'table_id', 0  'link_type' from column_link where src_table_id = %(table_id)s and relation_type = 1
        UNION
            select link_table_id 'table_id', 1  'link_type' from column_link cl
                join db_column dc on dc.id = cl.src_column_id and dc.unlink = 0 where src_table_id = %(table_id)s and relation_type = 1
        UNION
        select link_table_id 'table_id', 2 'link_type' from column_link
        where relation_type = 1 and src_table_id in
            (select link_table_id from column_link cl join db_column dc on dc.id = cl.src_column_id and dc.unlink = 0
                 where src_table_id = %(table_id)s and relation_type = 1)) as t
          join db_column dc on dc.table_id = t.table_id and dc.discarded = 0
          join db_table dt on dt.id = dc.table_id and dt.discarded = 0 
          join db_manage dm on dm.id = dt.db_id where dc.hide = 0 order by dt.id,dc.id;

        """

        getViewTableByGroupSQL = """
        select table_id from table_group_relation tgr where tgr.group_id = %(group_id)s;
        """

        getViewTableInfoByGroupSQL = """
        select DISTINCT(dc.id),dt.id, dt.e_name 'name', dc.e_name, dc.type, %(link_type)s 'link_type', dm.name 'db_name',dc.hide, dc.unlink  
          from db_column dc 
          join db_table dt on dt.id = dc.table_id  and dt.discarded = 0 and dc.unlink = 0 and dc.discarded = 0
          join db_manage dm on dm.id = dt.db_id where dc.hide = 0 
          and dt.id in %(table_ids)s  order by dt.id,dc.id;
        """

        getViewLinksByGroupSQL = """
        select link_table_id,sc.e_name 'src_col_name',st.e_name 'src_tb_name',lc.e_name 'link_col_name',lt.e_name 'link_tb_name' from column_link cl
            join db_column sc on sc.id = cl.src_column_id and sc.unlink = 0 and sc.discarded = 0
            join db_table st on st.id = cl.src_table_id and st.discarded = 0
            join db_column lc on lc.id = cl.link_column_id and lc.unlink = 0 and lc.discarded = 0
            join db_table lt on lt.id = cl.link_table_id and lt.discarded = 0
         where src_table_id in %(table_ids)s and relation_type = 1
        """

        #SET SQL FOR DAO
        self.data.setdefault("addDatabase", addDatabaseSQL)
        self.data.setdefault("deleteDatabase", deleteDatabaseSQL)
        self.data.setdefault("getDatabaseInfoById", getDatabaseInfoByIdSQL)
        self.data.setdefault("getDatabaseAllInfoById", getDatabaseAllInfoByIdSQL)
        self.data.setdefault("getDatabasePwdById", getDatabasePwdByIdSQL)
        self.data.setdefault("getDatabaseList", getDatabaseListSQL)
        self.data.setdefault("editDatabase", editDatabaseSQL)
        self.data.setdefault("editDatabasePwdById", editDatabasePwdByIdSQL)

        self.data.setdefault("addTableGroup", addTableGroupSQL)
        self.data.setdefault("deleteTableGroup", deleteTableGroupSQL)
        self.data.setdefault("getTableGroupInfoById", getTableGroupInfoByIdSQL)
        self.data.setdefault("getTableGroupInfoByName", getTableGroupInfoByNameSQL)
        self.data.setdefault("getTableGroupList", getTableGroupListSQL)
        self.data.setdefault("editTableGroup", editTableGroupSQL)

        self.data.setdefault("addTableGroupRelation", addTableGroupRelationSQL)
        self.data.setdefault("deleteTableGroupRelation", deleteTableGroupRelationSQL)
        self.data.setdefault("getTableGroupRelationList", getTableGroupRelationListSQL)
        self.data.setdefault("updateTableGroupRelation", updateTableGroupRelationSQL)
        self.data.setdefault("updateTableGroupRelationByGroupId", updateTableGroupRelationByGroupIdSQL)

        self.data.setdefault("deleteTableGroupByDB", deleteTableGroupByDBSQL)
        self.data.setdefault("deleteTableGroupRelationByDB", deleteTableGroupRelationByDBSQL)

        self.data.setdefault("addTable", addTableSQL)
        self.data.setdefault("deleteTable", deleteTableSQL)
        self.data.setdefault("getTableInfoById", getTableInfoByIdSQL)
        self.data.setdefault("getTableInfoByName", getTableInfoByNameSQL)
        self.data.setdefault("getTableList", getTableListSQL)
        self.data.setdefault("editTable", editTableSQL)
        self.data.setdefault("editTableByName", editTableByNameSQL)
        self.data.setdefault("editTableCNameById", editTableCNameByIdSQL)
        self.data.setdefault("editTableRemarkById", editTableRemarkByIdSQL)
        self.data.setdefault("discardTableByName", discardTableByNameSQL)

        self.data.setdefault("addColumn", addColumnSQL)
        self.data.setdefault("deleteColumn", deleteColumnSQL)
        self.data.setdefault("getColumnInfoById", getColumnInfoByIdSQL)
        self.data.setdefault("getColumnInfoByEname", getColumnInfoByEnameSQL)
        self.data.setdefault("getIdColumnInfoByTableName", getIdColumnInfoByTableNameSQL)
        self.data.setdefault("getIdColumnListByTableName", getIdColumnListByTableNameSQL)
        self.data.setdefault("getColumnListByTableId", getColumnListByTableIdSQL)
        self.data.setdefault("getColumnListByTableName", getColumnListByTableNameSQL)
        self.data.setdefault("editColumn", editColumnSQL)
        self.data.setdefault("editColumnRemarkById", editColumnRemarkByIdSQL)
        self.data.setdefault("editColumnTypeById", editColumnTypeByIdSQL)
        self.data.setdefault("editColumnDiscardById", editColumnDiscardByIdSQL)
        self.data.setdefault("editColumnHideById", editColumnHideByIdSQL)
        self.data.setdefault("editColumnUnlinkById", editColumnUnlinkByIdSQL)

        self.data.setdefault("isInitSynchronize", isInitSynchronizeSQL)
        self.data.setdefault("getSynchronizeDatabase", getSynchronizeDatabaseSQL)
        self.data.setdefault("getSynchronizeTable", getSynchronizeTableSQL)
        self.data.setdefault("getSynchronizeColumn", getSynchronizeColumnSQL)
        self.data.setdefault("getTableComment", getTableCommentSQL)

        self.data.setdefault("getSearchByTable", getSearchByTableSQL)
        self.data.setdefault("getSearchByTableColumn", getSearchByTableColumnSQL)
        self.data.setdefault("getSearchByColumn", getSearchByColumnSQL)
        self.data.setdefault("getSearchByColumnRemark", getSearchByColumnRemarkSQL)

        self.data.setdefault("addDBLog", addDBLogSQL)
        self.data.setdefault("getDBLogList", getDBLogListSQL)

        self.data.setdefault("addColumnLink", addColumnLinkSQL)
        self.data.setdefault("deleteColumnLink", deleteColumnLinkSQL)
        self.data.setdefault("getLinkTableList", getLinkTableListSQL)
        self.data.setdefault("getLinkColumnList", getLinkColumnListSQL)
        self.data.setdefault("getTableListByTableName", getTableListByTableNameSQL)
        self.data.setdefault("getColumnListByColName", getColumnListByColNameSQL)

        self.data.setdefault("addTableRoute", addTableRouteSQL)
        self.data.setdefault("addDataNode", addDataNodeSQL)
        self.data.setdefault("addDataRoute", addDataRouteSQL)
        self.data.setdefault("getTableRouteList", getTableRouteListSQL)

        self.data.setdefault("deleteColumn", deleteColumnSQL)
        self.data.setdefault("deleteTable", deleteTableSQL)

        self.data.setdefault("getViewLinks", getViewLinksSQL)
        self.data.setdefault("getViewTableInfo", getViewTableInfoSQL)
        self.data.setdefault("getViewLinksByGroup", getViewLinksByGroupSQL)
        self.data.setdefault("getViewTableInfoByGroup", getViewTableInfoByGroupSQL)
        self.data.setdefault("getViewTableByGroup", getViewTableByGroupSQL)


