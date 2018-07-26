<style lang="less">
    @import '../../styles/common.less';
    @import './components/table.less';
</style>

<template>
    <div>
        <Row>
            <Tabs @on-click="getData">
                <TabPane label="数据库详情">
                    <Col span="12">
                        <!-- todo card高度 -->
                        <Card class="margin-right-10">
                            <p slot="title">
                                <Icon type="grid" class="margin-right-10"></Icon>数据库信息
                            </p>
                            <p class="margin-bottom-10">连接名：
                                <label v-if="editIsHide">{{databaseDataModel.name}}</label>
                                <Input v-if="!editIsHide" v-model="databaseDataModel.name" style="width: 300px" ></Input>
                            </p>
                            <p class="margin-bottom-10">主机名：
                                <label v-if="editIsHide">{{databaseDataModel.host}}</label>
                                <Input v-if="!editIsHide" v-model="databaseDataModel.host" style="width: 300px" ></Input>
                            </p>
                            <p class="margin-bottom-10">端口：
                                <label v-if="editIsHide">{{databaseDataModel.port}}</label>
                                <Input v-if="!editIsHide" v-model="databaseDataModel.port" style="width: 300px" ></Input>
                            </p>
                            <p class="margin-bottom-10">用户名：
                                <label v-if="editIsHide">{{databaseDataModel.username}}</label>
                                <Input v-if="!editIsHide" v-model="databaseDataModel.username" style="width: 300px" ></Input>
                            </p>
                            <p class="margin-bottom-10">实例名：
                                <label v-if="editIsHide">{{databaseDataModel.schema_name}}</label>
                                <Input v-if="!editIsHide" v-model="databaseDataModel.schema_name" style="width: 300px" ></Input>
                            </p>
                            <p class="margin-bottom-10">BU：
                                <Select  v-if="editIsHide" disabled v-model="databaseDataModel.business_unit" style="width:300px">
                                        <Option :value="1" :key="1">NBU</Option>
                                    <Option :value="2" :key="2">TBU</Option>
                                    <Option :value="3" :key="3">IBU</Option>
                                </Select>
                                <Select  v-if="!editIsHide" v-model="databaseDataModel.business_unit" style="width:300px">
                                    <Option :value="1" :key="1">NBU</Option>
                                    <Option :value="2" :key="2">TBU</Option>
                                    <Option :value="3" :key="3">IBU</Option>
                                </Select>
                            </p>
                            <p style="text-align:right">
                                <i-button v-if="editIsHide" type="info" @click="addPwdShow" size="small" class="margin-left-10">查看/修改密码</i-button>        
                                <i-button v-if="!editIsHide" type="primary" @click="editDatabaseByIdNet" size="small">确定</i-button>
                                <i-button v-if="editIsHide" type="info" @click="changeEditShow" class="margin-left-10" size="small">编辑</i-button>
                            </p>
                        </Card>
                        <Card class="margin-right-10 margin-top-20">
                            <p slot="title">
                                <Icon type="grid" class="margin-right-10"></Icon>匹配规则 (没有符合命名规范 或者 对应关系不是唯一意义的字段 不建议使用)
                            </p>
                            <p class="margin-bottom-10">
                                规则匹配: <br />
                                <Input v-model="matchRule" placeholder="格式如：org-orgId,user-user_id" style="width: 300px" ></Input>
                                <i-button type="primary" @click="addLinkByMatchRule(1)" size="small">输入匹配</i-button><br /><br />
                                全局匹配：<br />
                                <i-button type="primary" @click="addLinkByMatchRule(2)" size="small">驼峰全局匹配</i-button>
                                <i-button type="primary" @click="addLinkByMatchRule(3)" size="small">_全局匹配</i-button>
                            </p>
                        </Card>
                    </Col>
                    <Col span="12">
                        <Card>
                            <p slot="title">
                                <Icon type="document" class="margin-right-10"></Icon>变动记录
                            </p>
                                <div>
                                    <!-- <Table border :columns="logListColumn" :data="loglist" show-header=false></Table> -->
                                    <ul style="list-style:none">
                                        <li v-for="log in logList" class="margin-bottom-10 margin-right-10">
                                            <Icon type="arrow-right-b"></Icon>
                                            {{log.content}}
                                        </li>
                                    </ul>
                                </div>
                        </Card>
                    </Col>
                </TabPane>
                <TabPane label="分组设置">
                    <div style="margin-top-10 margin-bottom-10">
                        <i-button type="success" @click="addGroup">新建分组</i-button>
                    </div>
                    <div>
                        <div class="margin-top-10">
                            <can-edit-table border :columns-list="listColumn" v-model="listData" @on-delete="handleDel"
                            :hover-show="true" :edit-incell="true" @on-cell-change="editGroupByIdNet" ></can-edit-table>
                        </div>
                    </div>
                </TabPane>
                <TabPane label="表归组设置">
                    <div style="margin-top-10 margin-bottom-10">
                        <i-button type="success" @click="setGroup">设置分组</i-button>
                    </div>
                    <div style="margin-top-10 margin-bottom-10">
                        <!-- todo card高度 -->
                        <Card style="margin-top-10 margin-bottom-10">
                            <Tree ref="tree" :data="groupRelation.group_info" show-checkbox></Tree>
                        </Card>
                    </div>
                </TabPane>
            </Tabs>
        </Row>

        <Modal v-model="showAddGroup" title="新建分组" @on-ok="addGroupNet" @on-cancel="cancelAddGroup">
            <Row type="flex" justify="center">
                <Input v-model="groupDataModel.name" placeholder="分组名" autofocus style="width: 400px"  class="margin-bottom-10" />
                <Input v-model="groupDataModel.sort" placeholder="排序" style="width: 400px" class="margin-bottom-10" />
            </Row>
            <Row slot="footer">
                <Button type="text" @click="cancelAddGroup">取消</Button>
                <Button type="primary" @click="addGroupNet">确定</Button>
            </Row>
        </Modal>

        <Modal v-model="showSetGroup" title="设置分组" @on-ok="updateTableGroupRelationNet" @on-cancel="cancelSetGroup">
            <Row type="flex" justify="center">
                <Select v-model="selectGroupId" style="width:200px">
                    <Option v-for="item in listData" :value="item.id" :key="item.id">{{ item.name }}</Option>
                </Select>
            </Row>
            <Row slot="footer">
                <Button type="text" @click="cancelSetGroup">取消</Button>
                <Button type="primary" @click="updateTableGroupRelationNet">确定</Button>
            </Row>
        </Modal>
        <Modal v-model="showPwd" title="密码设置" @on-cancel="cancelPwdShow">
            <Row v-if="knowKey" type="flex" justify="center">
                <Input v-model="dbPwd" style="width: 400px"  class="margin-bottom-10" />
            </Row>
            <Row v-if="knowKey"  slot="footer">
                <Button type="text" @click="cancelPwdShow">取消</Button>
                <Button type="primary" @click="editDatabasePwdByIdNet">确定</Button>
            </Row>
            <Row v-if="!knowKey"  type="flex" justify="center">
                <Input v-model="dbKey" placeholder="请输入秘钥" style="width: 400px"  class="margin-bottom-10" />
            </Row>
            <Row v-if="!knowKey"  slot="footer">
                <Button type="text" @click="cancelPwdShow">取消</Button>
                <Button type="primary" @click="confirmDatabasePwdByIdNet">确定</Button>
            </Row>
        </Modal>
    </div>
</template>

<script>
import canEditTable from './components/canEditTable.vue';
import axios  from 'axios';
export default {
    name: 'cooperation-db-info',
    components: {
        canEditTable
    },
    data () {
        return {
            knowKey: false,
            matchRule: "",
            showAddGroup: false,
            showPwd: false,
            logListColumn: [
                    {
                        title: '信息',
                        key: 'content',
                    },
            ],
            listColumn: [
                {
                    title: '组名',
                    key: 'name',
                    editable: true,
                },
                {
                    title: '排序',
                    key: 'sort',
                    editable: true,
                },
                {
                    title: '操作',
                    key: 'id',
                    width: 250,
                    align: 'center',
                    render: (h, params) => {
                        return h('div', [
                            h('Button', {
                                props: {
                                    type: 'error',
                                    size: 'small'
                                },
                                style: {
                                    marginRight: '5px'
                                },
                                on: {
                                    click: () => {
                                        this.deleteGroupNet(params.row.id, params.row.define, params.row.db_id)                                  
                                    }
                                }
                            }, '删除')
                        ])
                    },
                },
            ],
            listData:[],
            databaseDataModel:{
                    id: 0,
                    name: "",
                    host: "",
                    port: 3309,
                    username: "",
                    schema_name: "",
                    business_unit: 2,
                    product_unit: 1,
            },
            dbPwd: "",
            dbKey: "",
            groupDataModel:{
                id: 0,
                name: "",
                db_id: 0,
                define: 1,
                sort: "",
            },
            groupRelation: {
                db_name: "",
                group_info: [],
            },
            dbId: 0,
            editIsHide: true,
            selectGroupId:"",
            showSetGroup: false,
            logList: [],
        }
    },
    methods: {
        getData() {
            this.dbId = this.$route.query.id
            this.getDatabaseInfoByIdNet()
            this.getTableGroupListNet()
            this.getTableGroupRelationListNet()
            this.getDBLogListBydbIdNet()
        },
        getDBLogListBydbIdNet() {
            axios.get("/v1/database/getDBLogList",
                {"params":{"id": this.dbId}}
            ).then((res)=>{
                if(res.data.success){
                    this.logList = res.data.message
                }else{
                    this.$Message.error("获取日志列表失败")
                }
            }
            )
        },
        getDatabaseInfoByIdNet() {
            axios.get("/v1/database/getDatabaseInfoById",
                {"params":{"id": this.dbId}}
            ).then((res)=>{
                if(res.data.success){
                    this.databaseDataModel=res.data.message[0]
                }else{
                    this.$Message.error("获取数据库信息失败")
                }
            }
            )
        },
        getTableGroupListNet() {
            axios.get("/v1/database/getTableGroupList",
                {"params":{"id": this.dbId}}
            ).then((res)=>{
                if(res.data.success){
                    this.listData=res.data.message
                }else{
                    this.$Message.error("获取分组列表失败")
                }
            }
            )
        },
        getTableGroupRelationListNet() {
            axios.get("/v1/database/getTableGroupRelationList",
                {"params":{"id": this.dbId}}
            ).then((res)=>{
                if(res.data.success){
                    this.groupRelation = res.data.message
                }else{
                    this.$Message.error("获取表归组列表失败")
                }
            })
        },
        editDatabaseByIdNet() {
            if(this.databaseDataModel.name.trim() == "" || this.databaseDataModel.name === null) {
                this.$Message.error('请输入自定义连接名')
                return
            } else if(this.databaseDataModel.host.trim() == "" || this.databaseDataModel.host === null) {
                this.$Message.error('请输入主机名')
                return
            } else if(this.databaseDataModel.port == "" || this.databaseDataModel.port === null) {
                this.$Message.error('请输入端口号')
                return
            } else if(this.databaseDataModel.username.trim() == "" || this.databaseDataModel.username === null) {
                this.$Message.error('请输入用户名')
                return
            } else if(this.databaseDataModel.schema_name.trim() == "" || this.databaseDataModel.schema_name === null) {
                this.$Message.error('请输入实例名')
                return
            } else {
                axios.post("/v1/database/editDatabase",
                    this.databaseDataModel
                ).then((res)=>{
                    if(res.data.success){
                        this.showAddDB = false
                        this.$Message.success("编辑数据库成功")
                        this.getData()
                        this.changeEditShow()

                    }else{
                        this.$Message.error(res.data.message)
                    }
                })
            }
        },
        addPwdShow() {
            this.showPwd = true
        },
        cancelPwdShow() {
            this.showPwd = false
            this.dbPwd = ""
            this.dbPwd = ""
            this.knowKey = false
        },
        changeEditShow() {
            this.editIsHide = !this.editIsHide
        },
        editDatabasePwdByIdNet() {
            if(this.dbPwd.trim() == "" || this.dbPwd === null) {
                this.$Message.error('请输入密码')
                return
            } else {
                axios.post("/v1/database/editDatabasePwdById",
                    {password: this.dbPwd, id: this.databaseDataModel.id}
                ).then((res)=>{
                    if(res.data.success){
                        this.showPwd = false
                        this.$Message.success("编辑密码成功")
                        this.getData()
                        this.cancelPwdShow()
                        this.dbPwd = ""
                    }else{
                        this.$Message.error(res.data.message)
                    }
                })
            }
        },
        confirmDatabasePwdByIdNet() {
            if(this.dbKey.trim() == "" || this.dbKey === null) {
                this.$Message.error('请输入秘钥')
                return
            } else {
                axios.post("/v1/database/confirmDatabasePwdById",
                    {"bu":this.databaseDataModel.business_unit, key:this.dbKey}
                ).then((res)=>{
                    if(res.data.success){
                        this.getDatabasePwdByIdNet()
                        this.knowKey = !this.knowKey
                        this.dbKey = ""
                    }else{
                        this.$Message.error(res.data.message)
                    }
                })
            }
        },
        getDatabasePwdByIdNet() {
            axios.get("/v1/database/getDatabasePwdById",
                    {"params":{"id":this.databaseDataModel.id}}
                ).then((res)=>{
                    if(res.data.success){
                        let result = res.data.message
                        this.dbPwd = result[0]["password"]
                        console.log(res.data.message.password)
                        console.log(this.dbPwd)
                    }else{
                        this.$Message.error(res.data.message)
                    }
                })
        },
        editGroupByIdNet(val, index, key) {
            // todo 编辑为空不能保持编辑状态
            this.groupDataModel = val[index]
            if(this.groupDataModel.name.trim() == "" || this.groupDataModel.name == null) {
                this.getTableGroupListNet()
                this.$Message.error('编辑失败，未输入分组名')
                return
            } else if(this.groupDataModel.sort == "" || this.groupDataModel.sort == null) {
                this.getTableGroupListNet()
                this.$Message.error('编辑失败，未输入排序或排序不能为0')
                return
            } else {
                this.groupDataModel["sort"] = parseInt(this.groupDataModel["sort"])
                axios.post("/v1/database/editTableGroup",
                    this.groupDataModel
                ).then((res)=>{
                    if(res.data.success){
                        this.$Message.success("编辑分组成功")
                        this.getTableGroupListNet()
                        this.initGroupDataModel()
                    }else{
                        this.$Message.error(res.data.message)
                    }
                })
            }
        },
        handleDel(val, index) {
            // console.log(val)
            // console.log(index)
        },
        addGroup() {
            this.showAddGroup = true
        },
        cancelAddGroup() {
            this.initGroupDataModel()
            this.showAddGroup = false
        },
        addGroupNet() {
            this.groupDataModel.db_id = this.dbId
            this.groupDataModel.sort == "" ? "" : parseInt(this.groupDataModel.sort)
            if(this.groupDataModel.name.trim() == "" || this.groupDataModel.name === null) {
                this.$Message.error('请输入分组名')
                return
            } else if(this.groupDataModel.sort == "" || this.groupDataModel.sort === null) {
                this.$Message.error('请输入排序')
                return
            } else {
                axios.post("/v1/database/addTableGroup",
                    this.groupDataModel
                ).then((res)=>{
                    if(res.data.success){
                        this.showAddGroup = false
                        this.$Message.success("新建分组成功")
                        this.initGroupDataModel()
                        this.getTableGroupListNet()
                    }else{
                        this.$Message.error(res.data.message)
                    }
                })
            }
        },
        initGroupDataModel() {
            this.groupDataModel = {
                    id: 0,
                    name: "",
                    db_id: this.db_id,
                    define: 1,
                    sort: "",
            }
        },
        deleteGroupNet(index, define, db_id) {
            axios.post("/v1/database/deleteTableGroup",
                {"id": index, "define": define, "db_id": db_id}
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("删除分组成功")
                    this.getTableGroupListNet()
                }else{
                    this.$Message.error(res.data.message)
                }
            }
            )
        },
        setGroup() {
            this.showSetGroup = true
        },
        cancelSetGroup() {
            this.selectGroupId = ""
            this.showSetGroup = false
        },
        updateTableGroupRelationNet() {
            let groups = this.$refs.tree.getCheckedNodes()
            let groupId = this.selectGroupId

            if(groups.length == 0) {
                this.$Message.error('请选择要分组的表')
                return
            } else if(groupId == "") {
                this.$Message.error('请选择分组')
                return
            }

            let tables = []
            for(var i = 0; i < groups.length; i++) {
                if(groups[i].children === undefined) {
                    tables.push((groups[i].id).toString())
                }
            }

            axios.post("/v1/database/updateTableGroupRelation",
                {"tables": tables, "db_id": this.dbId, "group_id": groupId}
            ).then((res)=>{
                if(res.data.success){
                    this.showSetGroup = false
                    this.$Message.success("重新分组成功")
                    this.selectGroupId = ""
                    this.getTableGroupRelationListNet()
                }else{
                    this.$Message.error(res.data.message)
                }
            })
        },
        addLinkByMatchRule(type) {
            let content = ""
            if(type == 1) {
                content = this.matchRule
            }
            axios.post("/v1/database/addLinkByMatchRule",
                {"db": this.dbId, "content": content, "type":type}
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("同步关联关系成功")
                }else{
                    this.$Message.error(res.data.message)
                }
            })
        },       
    },
    mounted () {
        // this.getData()
    },
    // created () {
    //     this.getData()
    // },
    // watch: {
    //     '$route': function (route) {
    //         console.log(1)
    //         this.getData()
    //         console.log(2)
    //     },
    // },
    beforeRouteEnter(to, from, next) {
        next(vm => {
            vm.getData()
        })
    },
};
</script>
