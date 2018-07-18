<style lang="less">
    @import '../../../styles/common.less';
</style>

<template>
    <div>
        <Row type="flex" class="height-100">
            <Col span="8">
                <i-button type="success" @click="addTestSuite" style="margin-top-10">新建套件</i-button>
            </Col>
        </Row>
        <Row class="margin-top-10">
            <Col>
                <Card>
                    <div>
                        <can-edit-table
                                    v-model="list"
                                    @on-cell-change="handleCellChange"
                                    :editIncell="true"
                                    :columns-list="lsitColumns"
                         ></can-edit-table>
                    </div>
                </Card>
            </Col>
        </Row>
    </div>
</template>

<script>
import canEditTable from './canEditTable-suite.vue';
import axios  from 'axios';
export default {
    name: 'interface-manage',
    components: {
        canEditTable
    },
    data () {
        return {
            lsitColumns: [
                    {
                        title: '套件ID',
                        key: 'id'
                    },
                    {
                        title: '套件名称',
                        key: 'name',
                        editable: true,
                    },
                    {
                        title: '对应项目ID',
                        key: 'projectid'
                    },
                    {
                        title: '创建人',
                        key: 'create_username'
                    },
                    {
                        title: '操作',
                        key: 'action',
                        width: 150,
                        align: 'center',
                        render: (h, params) => {
                            return h('div', [
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
                                            let query = { projectId:params.row.projectid,suiteId: params.row.id };
                                            this.$router.push({
                                                name: 'suite-info',
                                                query: query
                                            });
                                        }
                                    }
                                }, '查看'),
                                h('Button', {
                                    props: {
                                        type: 'error',
                                        size: 'small'
                                    },
                                    on: {
                                        click: () => {
                                            this.removeTestSuiteData.suiteId = params.row.id
                                            this.removeTestSuite()
                                        }
                                    }
                                }, '删除')
                            ]);
                        }
                    }
            ],
            list:[],
            addTestSuiteData:{
                name:"",
                caseIds:"",
                userId:"",
                status:"",
                remarks:"",
                envId:"",
                projectId:""
            },
            removeTestSuiteData:{
                suiteId:"",
            },
            editTestSuiteData:{
                suiteId:"",
                name:"",

            }
        };
    },
    methods: {
        getData () {
                axios.get("/v1/suite/getSuiteList").then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.list = res.data.message;
                }else{
                    this.$Message.error("获取数据失败")
                }
            });
        },
        handleCellChange (val, index, key) {
            this.editTestSuiteData.suiteId = val[index]["id"]
            this.editTestSuiteData.name = val[index]["name"]
            axios.post("/v1/suite/editTestSuiteName",this.editTestSuiteData).then((res)=>{
            // console.log(val,index,key)
            if(res.data.success){
                  this.$Message.success("成功");
                  this.getData();

            }else{
                  this.$Message.error("失败")
            }
        }
        )
            this.$Message.success('修改了第 ' + (index + 1) + ' 行列名为 ' + key + ' 的数据');
        },
        removeTestSuite() {
                axios.post("/v1/suite/deleteTestSuite",
                this.removeTestSuiteData).then((res)=>{
                //console.log(res)
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getData();

                }else{
                    this.$Message.error("失败")
                }
            }
            )
            this.removeTestSuiteData = {
                suiteId:"",
            };
        },
        addTestSuite(){
            this.$Modal.confirm({
                onOk: () => {
                       this.addTestSuiteNet();
                    },
                    render: (h) => {
                    return h('div',[
                        h('Input', {
                            props: {
                                value: this.addTestSuiteData.name,
                                autofocus: true,
                                placeholder: '套件名称'
                            },
                            on: {
                                input: (val) => {
                                    this.addTestSuiteData.name = val;
                                }
                            }
                        }),
                        h('Input', {
                            props: {
                                value: this.addTestSuiteData.projectId,
                                autofocus: true,
                                placeholder: '对应项目ID'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.addTestSuiteData.projectId = val;
                                }
                            }
                        })
                    ])
                }
            })
        },
        addTestSuiteNet(){
            this.addTestSuiteData.userId=1,
            this.addTestSuiteData.status=1,
            axios.post("/v1/suite/addTestSuite",
            this.addTestSuiteData
            ).then((res)=>{
                //console.log(res)
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getData();

                }else{
                    this.$Message.error("失败")
                }
            }
            )
            this.addTestSuiteData = {
                name:"",
                caseIds:"",
                userId:"",
                status:"",
                remarks:"",
                envId:"",
                projectId:""
            };
        }
    },
    created () {
        this.getData();
    }
};
</script>
