<style lang="less">
    @import '../../../styles/common.less';
</style>

<template>
    <div>
        <Row class="margin-top-10">
            <Col>
                <Card>
                    <div>
                        <Table border :columns="lsitColumns" :data="list" @on-row-click="onRowClick"></Table>
                    </div>
                </Card>
            </Col>
        </Row>
    </div>
</template>

<script>
import axios  from 'axios';
export default {
    name: 'case-collection',
    data () {
        return {
            lsitColumns: [

                    {
                        title: '项目名称',
                        key: 'name'
                    },
                    {
                        title: '项目描述',
                        key: 'remarks'
                    },
                    {
                        title: '编辑时间',
                        key: 'gmt_modify'
                    },
                    {
                        title: '版本信息',
                        key: 'version'
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
                                            this.show(params.index)
                                        }
                                    }
                                }, '详情')
                            ]);
                        }
                    }
            ],
            list:[],
            addProjectData:{
                    name:"",
                    userName:"",
                    userId:0,
                    version:"",
                    remarks:""
            }
        };
    },
    methods: {
        onRowClick(rowData,index){
                console.log(rowData)
                this.$router.push({path:"/testcase/test-collection/case-list",query:{projectId:rowData.id}})
        },
        getData () {
                axios.get("http://localhost:8090/v1/project/getProjectList").then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.list = res.data.message;
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
    },
    created () {
        this.getData();
    }
};
</script>
