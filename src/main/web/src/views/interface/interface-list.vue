<style lang="less">
    @import '../../styles/common.less';
    @import './advanced-router.less';
</style>

<template>
    <div>
        <Row type="flex" class="height-100">
            <Col span="8">
                <i-button type="success" @click="addInterface" style="margin-top-10">新建接口</i-button>
                <i-button type="success" @click="synchronizeWebApi">同步接口</i-button>
            </Col>
            <Col span='8'>
                <Input v-model="searchValue" placeholder="接口path，如/api/swaggerservice/createwebapis">
                    <Button slot="append" icon="ios-search"  @click="searchApiByPath"></Button>
                </Input>
            </Col>
        </Row>
        <Row class="margin-top-10">
            <Card>
                <div class="margin-top-10">
                    <Table :columns="listColumns" :data="list"></Table>
                </div>
            </Card>
        </Row>
    </div>
</template>

<script>
import expandRow from './expandRow.vue';
import axios  from 'axios';
export default {
    components: {
        expandRow
    },
    data () {
        return {
            listColumns: [
                {
                    type: 'selection',
                    width: 60,
                    align: 'center'
                },
                {
                    type: 'expand',
                    width: 50,
                    render: (h, params) => {
                        return h(expandRow, {
                            props: {
                                row: params.row
                            }
                        });
                    }
                },
                {
                    title: '请求方式',
                    key: 'Method',
                    filters: [
                            {
                                label: 'Get',
                                value: 1
                            },
                            {
                                label: 'Post',
                                value: 2
                            }
                        ],
                        filterMultiple: false,
                        filterMethod (value, row) {
                            if (value === 1) {
                                return row.Method = get;
                            } else if (value === 2) {
                                return row.Method = post;
                            }
                        }
                },
                {
                    title: '接口地址',
                    key: 'Path'
                },
                {
                     title: '接口描述',
                     key: 'Summary'
                },
                {
                    title: '接口状态',
                    key: 'DiffType',
                    filters: [
                            {
                                label: '新增接口',
                                value: 1
                            },
                            {
                                label: '变动接口',
                                value: 2
                            },
                            {
                                label: '删除接口',
                                value: 3
                            },
                            {
                                label: '当前版本',
                                value: 4
                            }
                        ],
                        filterMultiple: false,
                        filterMethod (value, row) {
                            if (value === 1) {
                                return row.DiffType = 1;
                            } else if (value === 2) {
                                return row.DiffType = 2;
                            }
                        }
                },
                {
                    title: '测试情况',
                    key: 'DiffType',
                    filters: [
                            {
                                label: '未覆盖',
                                value: 1
                            },
                            {
                                label: '已覆盖',
                                value: 2
                            },
                        ],
                        filterMultiple: false,
                        filterMethod (value, row) {
                            if (value === 1) {
                                return row.DiffType = 1;
                            } else if (value === 2) {
                                return row.DiffType = 2;
                            }
                        }
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
                                        let query = {projectId:this.$route.query.id,interfaceId: params.row.id}
                                        this.$router.push({
                                            name:'interface-edit',
                                            query:query
                                        })
                                    }
                                }
                            }, '编辑'),
                            h('Button', {
                                props: {
                                    type: 'error',
                                    size: 'small'
                                },
                                on: {
                                    click: () => {
                                        this.removeInterfaceData.interfaceId = params.row.id
                                        this.removeInterface()
                                    }
                                }
                            }, '确认')
                        ]);
                    }
                }
            ],
            list: [],
            searchValue:"",
            formItem:{},
        };
    },
    methods: {
        addInterface(){
            this.$router.push({path:"/interface/interface-edit",query:{projectId:this.$route.query.projectId,applicationId:this.$route.query.applicationId}})
        },
        getWebapiList(){
            axios.get("/v1/webapi/getWebApiList",{params:{projectId:this.$route.query.projectId,applicationId:this.$route.query.applicationId}}
                ).then((res)=>{
                console.log(res)
                console.log(this.$route.query.id)
                if(res.data.success){
                    this.list = []
                    this.list = res.data.message;
                }else{
                    this.$Message.error("获取数据失败");
                }
            }
            )
        },
        searchApiByPath(){
            let Path=this.searchValue
            axios.get("/v1/webapi/getWebApiInfoByPath",{params:{projectId:this.$route.query.projectId,applicationId:this.$route.query.applicationId,Path:Path}}
                ).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.list = []
                    this.list = res.data.message;
                }else{
                    this.$Message.error("获取数据失败");
                }
            }
            )
        },
        synchronizeWebApi(){
            return axios.get("/v1/application/getVersionConfig",{params:{projectId:this.$route.query.projectId,applicationId:this.$route.query.applicationId}}).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.formItem = res.data.message[0];
                    axios.get("/v1/webapi/synchronizeWebApi",{params:{projectId:this.$route.query.projectId,applicationId:this.$route.query.applicationId,swaggerJsonOrUrl:this.formItem.swagger_url}}
                        ).then((res)=>{
                        console.log(res)
                        if(res.data.success){
                            this.$Message.success("同步成功");
                        }else{
                            this.$Message.error("同步失败");
                        }
                    })
                }else{
                    this.$Message.error("获取数据失败")
                }
            })
        },
        handleSelectAll (status) {
            this.$refs.selection.selectAll(status);
        },
    },
    created () {
        this.getWebapiList();
    }
};
</script>
