<style lang="less">
@import "../../styles/common.less";
@import "./components/table.less";
@import "./cooperation-dbdoc-list.less";
</style>

<template>
    <div>
        <Row>
            <!-- <Card> -->
            <Col span="16">
                <div class="margin-top-10">
                    <Select v-model="searchInput" placeholder="搜索表名(user) / 表字段(user.id) / 字段(.id) / 字段备注(#内容)" 
                     filterable remote :remote-method="remoteSearch" :loading="selectIsLoading" clearable @on-change="selectChange">
                        <Option v-for="item in searchList" :value="item.id" :key="item.uid">{{item.e_name}}</Option>
                    </Select>
                </div>
                <div class="margin-top-10">
                    <div style="font-size:25px">  {{tableDataModel.e_name}}（{{tableDataModel.c_name}}）
                        <!-- <Button type="success" @click="setCloumnLink"  size="small" >增加外键/数据关系</Button> -->
                        <Button type="success" @click="setCloumnLink"  size="small" >增加外键关系</Button>
                        <Button type="warning" @click="updateCommentNet"  size="small" >更新表信息</Button>
                        <Button type="primary" size="small" @click="exportData(1, tableDataModel.e_name)"><Icon type="ios-download-outline"></Icon> 导出</Button>
                        <Button type="error" size="small" @click="lookLinks">外联关系</Button>
                    </div>
                </div>
                <div class="margin-top-10">
                <!-- <Collapse v-model="collapseStatus" accordion >
                  <Panel name="1">
                      数据流
                      <div slot="content">
                        <Timeline v-for="item in routeList">
                            <TimelineItem v-for="r in item.route"  color="green">
                              <p class="time">{{r.data_operation}}</p>
                              <p class="content">{{r.data_module}}</p>
                            </TimelineItem>
                        </Timeline>
                      </div>
                  </Panel>
                  <Panel name="2">
                      外键/数据关系
                      <div slot="content">
                        <p>tree：http://echarts.baidu.com/examples/editor.html?c=tree-legend</p>
                        <p>sandkey:http://echarts.baidu.com/examples/editor.html?c=sankey-energy</p>
                      </div>
                  </Panel> 
                </Collapse> -->
                </div>
                <div class="margin-top-10">    
                    <Input v-model="tableDataModel.remark" type="textarea" :autosize="{minRows: 2, maxRows: 5}" 
                    placeholder="备注" @on-blur="editTableRemarkByIdNet"></Input>
                </div>
                
                <div class="edittable-table-height-con margin-top-10">
                    <can-edit-table border :columns-list="listColumn" v-model="listData"
                    :hover-show="true" :edit-incell="true"  @on-cell-switch="editColumnStatusById"
                    @on-cell-link="handleLinkGo" @on-link-del="deleteColumnLinkNet"
                    :ref="'table1'"></can-edit-table>
                </div>
                
            </Col>
            <Col span="8" class="padding-left-10">
                <div class="">
                    <Card>
                        <p slot="title">
                            <Icon type="navicon-round"></Icon>
                            【{{groupRelation.db_name}}】文档目录
                        </p>
                        <Tree ref="tree" :data="groupRelation.group_info" @on-select-change="getTreeTableInfo"></Tree>
                    </Card>
                </div>
                
            </Col>
        <!-- </Card> -->
        </Row>
    <!-- <Modal v-model="setLinkModal" title="增加外键/数据关系" @on-ok="addColumnLink"> -->
    <Modal v-model="setLinkModal" title="增加外键关系" @on-ok="addColumnLink">
        <!-- todo 枚举值先写死了 -->
        <div class="margin-top-10">
          关系类型
          <Select v-model="selectLinkType" style="width:200px">
              <Option :value="1" :key="1">外键关系</Option>
              <!-- <Option :value="2" :key="2">数据关系</Option> -->
          </Select>
        </div>
        <div class="margin-top-10">
          源字段
          <Select v-model="selectSrcColumn" style="width:200px">
              <Option v-for="item in listData" :value="item.id" :key="item.id">{{ item.e_name }}</Option>
          </Select>
        </div>
        <div class="margin-top-10">
          关系库
          <Select v-model="selectLinkDB" style="width:200px" @on-change="selectLinkDBChange">
              <Option v-for="item in linkDBList" :value="item.id" :key="item.id">{{ item.name }}</Option>
          </Select>
        </div>
        <div class="margin-top-10">
            <!-- 默认选取已经产生关联的，否则选取条件下的，支持跨库 -->
            关系表
          <Select v-model="selectLinkTable" style="width:200px" @on-change="selectLinkTableChange" 
           filterable remote :remote-method="remoteLinkTableSearchNet" :loading="selectIsLoading">
              <Option v-for="item in linkTableList" :value="item.id" :key="item.id">{{ item.e_name }}</Option>
          </Select>
        </div>
        <div class="margin-top-10">
            <!-- 默认选取已经产生关联的，否则选取条件下的，支持跨库 -->
          关系字段
          <Select v-model="selectLinkColumn" style="width:200px" @on-change="selectLinkColumnChange" 
           filterable remote :remote-method="remoteLinkColumnSearchNet" :loading="selectIsLoading">
              <Option v-for="item in linkColumnList" :value="item.id" :key="item.id">{{ item.e_name }}</Option>
          </Select>
        </div>
    </Modal>
    </div>
</template>

<script>
import canEditTable from "./components/canEditTableChange.vue";
import axios from "axios";
export default {
    name: "cooperation-dbdoc-list",
    components: {
        canEditTable
    },
    data() {
        return {
            tableId: 0,
            selectSrcColumn: "",
            selectLinkType: 1,
            linkDBList: [],
            selectLinkDB: "",
            linkTableList: [],
            selectLinkTable: "",
            linkColumnList: [],
            selectLinkColumn: "",
            setLinkModal: false,
            collapseStatus: "",
            selectIsLoading: false,
            listColumn: [
                {
                    title: "字段",
                    width: 150,
                    key: "e_name"
                },
                {
                    title: "备注",
                    key: "remark",
                    editable: false
                },
                {
                    // title: "外键/数据关系",
                    title: "外键关系",
                    width: 280,
                    key: "links",
                    showlink: true
                },
                {
                    title: "类型",
                    width: 100,
                    key: "type"
                },
                {
                    title: "废弃",
                    width: 70,
                    key: "discarded",
                    switchbutton: true
                },
                {
                    title: "隐藏",
                    width: 70,
                    key: "hide",
                    switchbutton: true
                },
                {
                    title: "取关",
                    width: 70,
                    key: "unlink",
                    switchbutton: true
                },
            ],
            listData: [],
            tableDataModel: {
                id: 0,
                e_name: "",
                c_name: "",
                type: "",
                remark: "",
                discarded: 0,
                hide: 0,
                unlink: 0,
            },
            groupRelation: {
                db_name: "",
                group_info: [],
            },
            dbId: 0,
            searchInput: "",
            searchList: [],
            columnLinkModel: {
            　  src_column_id: 0,
            　  src_table_id: 0,
            　  relation_type: 0,
            　  link_column_id: 0,
            　  link_table_id: 0,
            },
            routeList: [],
        }
    },
    methods: {
        initColumnDataModel() {
            this.tableDataModel = {
                id: 0,
                e_name: "",
                c_name: "",
                type: "",
                remark: "",
                discarded: 0,
                hide: 0,
                unlink: 0,
            }
        },
        initColumnLinkModel() {
            this.columnLinkModel = {
                src_column_id: 0,
                src_table_id: 0,
                relation_type: 0,
                link_column_id: 0,
                link_table_id: 0,
            }
            this.selectLinkTable = ""
            this.selectLinkColumn = ""
            this.selectLinkDB = ""
            this.selectSrcColumn = ""
            this.selectLinkType = ""
        },
        getData() {
            this.dbId = this.$route.query.id
            this.isSearch=0
            this.getTableGroupRelationListInitNet(this.dbId)
        },
        getTableGroupRelationListInitNet(db_id) {
            axios.get("/v1/database/getTableGroupRelationList", {
                params: { id: db_id }
            }).then(res => {
                if (res.data.success) {
                    this.groupRelation = res.data.message
                    if(this.tableId == 0) {
                        let tableId = this.groupRelation.group_info[0].children[0].table_id
                        this.tableId = tableId
                    }
                    // 更新表信息
                    this.initTableinfo(this.tableId)
                } else {
                    this.$Message.error("获取表分组关系列表失败")
                }
            })
        },
        getTableGroupRelationListNet(db_id) {
            let table_id = this.tableId
            axios.get("/v1/database/getTableGroupRelationList", {
                params: { id: db_id }
            }).then(res => {
                if (res.data.success) {
                    this.groupRelation = res.data.message
                    this.initTableinfo(table_id)
                } else {
                    this.$Message.error("获取表分组关系列表失败")
                }
            })
        },
        initTableinfo(table_id) {
            this.getColumnListByTableIdNet(table_id)
            this.getTableInfoByIdNet(table_id)
            this.changeTreeSelected(table_id)
        },
        getTreeTableInfo(selectedArray) {
            let isHasChildren = selectedArray[0].children
            // todo 根节点不要选中且没有事件
            if (Array.isArray(isHasChildren)) {
                let groupId = selectedArray[0].id
                this.$router.push({path:"/cooperation/cooperation-dbdoc-link",query:{id:groupId, type:2}})
            } else {
                let tableId = selectedArray[0].table_id
                this.tableId = tableId
                this.getColumnListByTableIdNet(tableId)
                this.getTableInfoByIdNet(tableId)
            }
        },
        getColumnListByTableIdNet(tableId) {
            this.tableId = tableId
            axios.get("/v1/database/getColumnListByTableId", {
                params: { id: tableId}
            }).then(res => {
                if (res.data.success) {
                    this.listData = res.data.message
                    // debugger
                    // console.log(this.listData)
                } else {
                    this.$Message.error("获取表的字段信息失败")
                }
            })
        },
        getTableInfoByIdNet(tableId) {
            axios.get("/v1/database/getTableInfoById", {
                params: { id: tableId}
            }).then(res => {
                if (res.data.success) {
                    this.tableDataModel = res.data.message[0]
                } else {
                    this.$Message.error("获取表信息失败")
                }
            })
        },
        handleLinkGo(val, index, key, info) {
            this.dbId = info.db
            this.tableId = info.key
            this.getTableGroupRelationListNet(this.dbId)
        },
        deleteColumnLinkNet(val, index, key, info) {
            axios.post("/v1/database/deleteColumnLink", {
                id: info.cl
            })
            .then(res => {
                if (res.data.success) {
                    this.getColumnListByTableIdNet(this.tableId)
                    this.$Message.success("删除外联关系成功")
                } else {
                    this.$Message.error("删除外联关系失败")
                }
            })

        },
        editColumnStatusById(val, index, key) {
            let id = parseInt(val[index]["id"])
            let value = val[index][key]
            if(value == 1) {
                value = 0
            } else if(value == 0) {
                value = 1
            }

            if(key == "discarded") {
                this.editColumnDiscardByIdNet(value, id, key)
            } else if(key == "hide") {
                this.editColumnHideByIdNet(value, id, key)
            } else if(key == "unlink") {
                this.editColumnUnlinkByIdNet(value, id, key)
            }
        },
        editColumnDiscardByIdNet(val, id, key) {
            axios.post("/v1/database/editColumnDiscardById", {
                id: id, key: key, val: val
            })
            .then(res => {
                if (res.data.success) {
                    this.$Message.success("编辑字段废弃状态成功")
                } else {
                    this.$Message.error("编辑字段废弃状态失败")
                }
            })
        },
        editColumnHideByIdNet(val, id, key) {
            axios.post("/v1/database/editColumnHideById", {
                id: id, key: key, val: val
            })
            .then(res => {
                if (res.data.success) {
                    this.$Message.success("编辑字段隐藏状态成功")
                } else {
                    this.$Message.error("编辑字段隐藏状态失败")
                }
            })
        },
        editColumnUnlinkByIdNet(val, id, key) {
            axios.post("/v1/database/editColumnUnlinkById", {
                id: id, key: key, val: val
            })
            .then(res => {
                if (res.data.success) {
                    this.$Message.success("编辑字段取关状态成功")
                } else {
                    this.$Message.error("编辑字段取关状态失败")
                }
            })
        },
        remoteSearch(query) {
            // if(this.isSearch%3!=0){
            //   return
            // }

            let content = { db_id: this.dbId, content: query }

            var cindex = query.indexOf("#")
            if(cindex == 0) {
                this.getSearchListNet(3, content)
            } else {
            let index = query.indexOf(".")
                if(content != "") {
                    if (index > 0) {
                    // table.column
                    this.getSearchListNet(0, content)
                    } else if (index == -1) {
                    // table
                    this.getSearchListNet(1, content)
                    } else if (index == 0) {
                    // .column
                    this.getSearchListNet(2, content)
                    }
                }
            }
        },
        getSearchListNet(searchType, content) {
            if (searchType == 0) {
                // table.column
                this.selectIsLoading = true
                axios.post("/v1/database/getSearchByTableColumn", content).then(res => {
                    if (res.data.success) {
                        this.searchList = res.data.message
                        this.selectIsLoading = false
                    } else {
                        this.$Message.error("根据[表名.字段名]搜索失败")
                    }
                })
            } else if (searchType == 1) {
                // table
                this.selectIsLoading = true
                axios.post("/v1/database/getSearchByTable", content).then(res => {
                if (res.data.success) {
                    this.searchList = res.data.message
                    this.selectIsLoading = false
                } else {
                    this.$Message.error("根据[表名]搜索失败")
                }
            })
            } else if (searchType == 2) {
                // .column
                this.selectIsLoading = true
                axios.post("/v1/database/getSearchByColumn", content).then(res => {
                    if (res.data.success) {
                        this.searchList = res.data.message
                        this.selectIsLoading = false
                    } else {
                        this.$Message.error("根据[.字段名]搜索失败")
                    }
                })
            } else if (searchType == 3) {
                // #字段备注
                this.selectIsLoading = true
                axios.post("/v1/database/getSearchByColumnRemark", content).then(res => {
                if (res.data.success) {
                    this.searchList = res.data.message
                    this.selectIsLoading = false
                } else {
                    this.$Message.error("根据[备注]搜索失败")
                }
            })
        }
        },
        selectChange(val) {
            var id = val
            if(id > 0) {
                this.getColumnListByTableIdNet(id)
                this.getTableInfoByIdNet(id)
                this.changeTreeSelected(id)
                this.tableId = id
            }
            
        },
        changeTreeSelected(id) {
            // $set赋值
            this.groupRelation.group_info.forEach(grops =>{
                grops.children.forEach(item =>{
                    if(item.table_id==id){
                        this.$set(item,'selected',true)
                    }else{
                        this.$set(item,'selected',false)
                    }
                })
            })
        },
        addColumnLink() {
            this.setLinkModal = false
            this.columnLinkModel.relation_type = this.selectLinkType
            this.columnLinkModel.link_table_id = this.selectLinkTable
            this.columnLinkModel.link_column_id = this.selectLinkColumn
            this.columnLinkModel.src_column_id = this.selectSrcColumn
            this.columnLinkModel.src_table_id = this.tableId
            this.addColumnLinkNet()
        },
        addColumnLinkNet() {
            // let db_id = this.selectLinkDB
            // let tableId = this.selectLinkTable
            axios.post("/v1/database/addColumnLink",
                this.columnLinkModel
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("添加字段关系成功")
                    // 为什么this.selectLinkDB没用 作用域不一样
                    // this.getTableGroupRelationListNet(db_id)
                    this.getColumnListByTableIdNet(this.tableId)
                }else{
                    this.$Message.error(res.data.message)
                }
            })
            this.initColumnLinkModel()
        },
        setCloumnLink() {
            this.setLinkModal = true
            this.getDatabaseListNet()
        },
        getDatabaseListNet(buId=2) {
            // todo id写死了
            axios.get("/v1/database/getDatabaseList",
                {"params":{"id": buId}}
            ).then((res)=>{
                if(res.data.success){
                    this.linkDBList = res.data.message
                }else{
                    this.$Message.error("获取数据库列表失败")
                }
            })
        },
        getLinkTableListNet(id) {
            axios.get("/v1/database/getLinkTableList",
                {"params":{"id": id}}
            ).then((res)=>{
                if(res.data.success){
                    this.linkTableList = res.data.message
                }else{
                    this.$Message.error("获取曾经关联过的表失败")
                }
            })
        },
        getLinkColumnListNet(id) {
            return axios.get("/v1/database/getLinkColumnList",
                {"params":{"id": id}}
            ).then((res)=>{
                if(res.data.success){
                    this.linkColumnList = res.data.message
                }else{
                    this.$Message.error("获取曾经关联过的字段失败")
                }
            })
        },
        selectLinkDBChange(val) {
            // todo selectLinkTable?
            if(val != undefined) {
                this.getLinkTableListNet(val)
                this.selectLinkTable = ""
                this.selectLinkColumn = ""   
            }
        },
        selectLinkTableChange(val) {
            if(val != undefined) {
                this.getLinkColumnListNet(val)
                this.selectLinkColumn = ""
            }
        },
        selectLinkColumnChange() {
            
        },
        remoteLinkTableSearchNet(query) {
            this.selectIsLoading = true
            axios.post("/v1/database/getTableListByTableName", {
                id: this.selectLinkDB, content: query
            }).then(res => {
                if (res.data.success) {
                    this.linkTableList = res.data.message
                    this.selectIsLoading = false
                } else {
                    this.$Message.error("获取关联表失败")
                }
            })
        },
        remoteLinkColumnSearchNet(query) {
            this.selectIsLoading = true
            axios.post("/v1/database/getColumnListByColName", {
                id: this.selectLinkTable, content: query
            }).then(res => {
                if (res.data.success) {
                    this.linkColumnList = res.data.message
                    this.selectIsLoading = false
                } else {
                    this.$Message.error("获取关联字段失败")
                }
            })
        },
        updateCommentNet() {
            axios.post("/v1/database/updateComment", {
                id: this.tableId, db_id: this.dbId
            }).then(res => {
                if (res.data.success) {
                    this.getTableGroupRelationListNet(this.dbId)
                    this.$Message.success("更新表信息成功")
                } else {
                    this.$Message.error(res.data.message)
                }
            })
        },
        editTableRemarkByIdNet() {
            axios.post("/v1/database/editTableRemarkById", {
                id: this.tableId, remark: this.tableDataModel.remark
            }).then(res => {
                if (res.data.success) {
                    this.$Message.success("编辑表备注成功")
                    // this.getTableGroupRelationListNet(this.dbId)
                    this.getTableInfoByIdNet(this.tableId)
                } else {
                    this.$Message.error(res.data.message)
                }
            })
        },
        exportData (type, file_name) {
            if (type === 1) {
                this.$refs.table1.$children[0].exportCsv({
                    file_name: file_name,
                    // columns: this.listColumn.filter((col, index) => index = 1),
                })
            } 
            // else if (type === 2) {
            //     this.$refs.table.exportCsv({
            //         file_name: 'Sorting and filtering data',
            //         original: false
            //     })
            // } else if (type === 3) {
            //     this.$refs.table.exportCsv({
            //         file_name: 'Custom data',
            //         columns: this.columns8.filter((col, index) => index < 4),
            //         data: this.data7.filter((data, index) => index < 4)
            //     })
            // }
        },
        lookLinks() {
            this.$router.push({path:"/cooperation/cooperation-dbdoc-link",query:{id:this.tableId, type:1}})
        },
    },
    // created() {
    //     this.getData()
    // },
    // watch: {
    //     '$route': function (route) {
    //         console.log(1)
    //         // let query = route.query
    //         // this.page = query.page
    //         this.getData()
    //         console.log(2)
    //     },
    // },
    beforeRouteEnter(to, from, next) {
        next(vm => {
            vm.getData()
        })
    },
}
</script>
