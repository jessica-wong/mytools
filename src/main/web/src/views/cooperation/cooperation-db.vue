<style lang="less">
    @import '../../styles/common.less';
    @import './components/table.less';
</style>

<template>
    <div>
        <Row type="flex" class="height-100" :gutter="16">
            <div class="margin-left-10">
                <Select v-model="selectBU" @on-change="getDatabaseListNet(selectBU)" style="width:100px">
                    <Option :value="1" :key="1">NBU</Option>
                    <Option :value="2" :key="2">TBU</Option>
                    <Option :value="3" :key="3">IBU</Option>
                </Select>
                <i-button type="success" @click="addDatabase" class="margin-left-10" >新建数据库</i-button>
            </div>
        </Row>
        <Row class="margin-top-10">
            <div class="edittable-table-height-con">
                <Table border :columns="listColumn" :data="list"></Table>
            </div>
        </Row>
    
        <Modal v-model="showAddDB" title="新建数据库" @on-ok="addDatabaseNet" @on-cancel="cancelAddDatabase">
            <Row type="flex" justify="center">
                <Input v-model="databaseDataModel.name" placeholder="自定义连接名" autofocus style="width: 400px"  class="margin-bottom-10" />
                <Input v-model="databaseDataModel.host" placeholder="主机名" style="width: 400px" class="margin-bottom-10" />
                <Input v-model="databaseDataModel.port" placeholder="端口号" style="width: 400px" class="margin-bottom-10" />
                <Input v-model="databaseDataModel.username" placeholder="用户名" style="width: 400px" class="margin-bottom-10" />
                <Input v-model="databaseDataModel.password" placeholder="密码" style="width: 400px" class="margin-bottom-10" />
                <Input v-model="databaseDataModel.schema_name" placeholder="实例名(schema)" style="width: 400px" class="margin-bottom-10" />
                <Select v-model="databaseDataModel.business_unit" style="width:400px">
                    <Option :value="1" :key="1">NBU</Option>
                    <Option :value="2" :key="2">TBU</Option>
                    <Option :value="3" :key="3">IBU</Option>
                </Select>
            </Row>
            <Row slot="footer">
                <Button type="text" @click="cancelAddDatabase">取消</Button>
                <Button type="primary" @click="addDatabaseNet">确定</Button>
            </Row>
        </Modal>
    </div>
</template>

<script>
// 新建做非空校验，返回message。其它默认
// 发请求的方法末尾加Net
// 命名默认驼峰。数据库字段以_方式，所以字段的数据模型_方式
import axios  from 'axios';
export default {
    name: 'cooperation-db',
    data () {
        return {
            selectBU: 2,
            showAddDB: false,
            listColumn: [
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
                                        this.deleteDatabaseNet(params.row.id)
                                    }
                                }
                            }, '删除'),
                            h('Button', {
                                props: {
                                    type: 'warning',
                                    size: 'small'
                                },
                                style: {
                                    marginRight: '5px'
                                },
                                on: {
                                    click: () => {
                                        this.isSynchronizeDatabaseNet(params.row.id, 1)
                                    }
                                }
                            }, '同步'),
                            h('Button', {
                                props: {
                                    type: 'primary',
                                    size: 'small'
                                },
                                style: {
                                    marginRight: '5px'
                                },
                                on: {
                                    click: () => {
                                        this.$router.push({path:"/cooperation/cooperation-db-info",query:{id:params.row.id}})
                                    }
                                }
                            }, '编辑'),
                            h('Button', {
                                props: {
                                    type: 'info',
                                    size: 'small'
                                },
                                style: {
                                    marginRight: '5px'
                                },
                                on: {
                                    click: () => {
                                        this.isSynchronizeDatabaseNet(params.row.id, 2)                                      
                                    }
                                }
                            }, '查看文档'),
                            
                        ])
                    },
                },
                {
                    title: '连接名',
                    key: 'name',
                },
                {
                    title: '主机名',
                    key: 'host',
                },
                {
                    title: '端口',
                    key: 'port',
                },
                {
                    title: '用户名',
                    key: 'username',
                },
                //不暴露在外面
                // {
                //     title: '密码',
                //     key: 'password',
                // },
                {
                    title: '实例名(scheam)',
                    key: 'schema_name',
                },
            ],
            list:[],
            databaseDataModel:{
                id: 0,
                name: "",
                host: "",
                port: 3309,
                username: "",
                password: "",
                schema_name: "",
                business_unit: 2,
                // todo 从当前用户的数据读，先写死了
                product_unit: 1,
            },
        }
    },
    methods: {
        initDatabaseDataModel() {
            this.databaseDataModel = {
                id: 0,
                name: "",
                host: "",
                port: 3309,
                username: "",
                password: "",
                schema_name: "",
                business_unit: 2,
                // todo 从当前用户的数据读，先写死了
                product_unit: 1,
            }
        },
        getData () {
            this.getDatabaseListNet(this.selectBU)
        },
        getDatabaseListNet(id) {
            // todo id写死了
            return axios.get("/v1/database/getDatabaseList",
                {"params":{"id": id}}
            ).then((res)=>{
                if(res.data.success){
                    this.list = res.data.message
                }else{
                    this.$Message.error("获取数据库列表失败")
                }
            })
        },
        addDatabase() {
            this.showAddDB = true
        },
        cancelAddDatabase() {
            this.initDatabaseDataModel()
            this.showAddDB = false
        },
        addDatabaseNet() {
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
            } else if(this.databaseDataModel.password.trim() == "" || this.databaseDataModel.password === null) {
                this.$Message.error('请输入密码')
                return
            } else if(this.databaseDataModel.schema_name.trim() == "" || this.databaseDataModel.schema_name === null) {
                this.$Message.error('请输入实例名')
                return
            } else {
                axios.post("/v1/database/addDatabase",
                    this.databaseDataModel
                ).then((res)=>{
                    if(res.data.success){
                        this.showAddDB = false
                        this.selectBU = this.databaseDataModel.business_unit
                        this.$Message.success("新建数据库成功")
                        this.initDatabaseDataModel()
                        this.getData()

                    }else{
                        this.$Message.error(res.data.message)
                    }
                })
            }
        },
        deleteDatabaseNet(index){
            axios.post("/v1/database/deleteDatabase",
                {"id": index}
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("删除数据库成功")
                    this.getData()
                }else{
                    this.$Message.error(res.data.message)
                }
            })
        },
        isSynchronizeDatabaseNet(index, type) {
            axios.get("/v1/database/isInitSynchronize",
                {"params":{"id": index}}
            ).then((res)=>{
                if(res.data.success){
                    let tableCount = res.data.message[0]["tableCount"]
                    if(tableCount == 0 && type == 1) {
                        this.initSynchronizeDatabaseNet(index)
                    } else if(tableCount > 0 && type == 1) {
                        this.synchronizeDatabaseNet(index)
                    } else if(tableCount > 0 && type ==2) {
                        this.showDoc(index)
                    } else if(tableCount == 0 && type ==2) {
                        this.$Message.error("还未同步，请先同步！")
                    }
                }else{
                    this.$Message.error("初始化数据库数据失败")
                }
            })
        },
        initSynchronizeDatabaseNet(index) {
            axios.post("/v1/database/initSynchronizeDatabase",
            {"id":index}
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("初始化数据库数据成功")
                }else{
                    this.$Message.error("初始化数据库数据失败")
                }
            })
        },
        synchronizeDatabaseNet(index) {
            axios.post("/v1/database/synchronizeDatabase",
            {"id":index}
            ).then((res)=>{
                if(res.data.success){
                    this.$Message.success("同步数据库数据成功")
                }else{
                    this.$Message.error("同步数据库数据失败")
                }
            })
        },
        showDoc(index) {
            this.$router.push({path:"/cooperation/cooperation-dbdoc-list",query:{id:index}})
        },
    },
    // created () {
    //     this.getData()
    // },
    beforeRouteEnter(to, from, next) {
        next(vm => {
            vm.getData()
        })
    },
}
</script>
