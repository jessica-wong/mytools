<style lang="less">
    @import '../../styles/common.less';
</style>

<template>
    <div>
        <Row type="flex" class="height-100">
            <Col span="8">
                <i-button type="success" @click="addEnvironment" style="margin-top-10">添加环境</i-button>
            </Col>
        </Row>
        <Row class="margin-top-10">
            <Col>
                <Card>
                    <div>
                        <Table border :columns="lsitColumns" :data="list"></Table>
                    </div>
                </Card>
            </Col>
        </Row>
    </div>
</template>

<script>
import axios  from 'axios';
export default {
    name: 'interface-manage',
    data () {
        return {
            lsitColumns: [

                    {
                        title: '环境名称',
                        key: 'env_name'
                    },
                    {
                        title: '创建人',
                        key: 'create_username'
                    },
                    {
                        title: '编辑时间',
                        key: 'gmt_modify'
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
                                            let query = { id: params.row.id };
                                            this.$router.push({
                                                name: 'environment-info',
                                                query: query
                                            });
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
                                            this.removeEnvironmentData.envId = params.row.id
                                            this.removeEnvironment()
                                        }
                                    }
                                }, '删除')
                            ]);
                        }
                    }
            ],
            list:[],
            addEnvironmentData:{
                    env_name:"",
                    userId:1
            },
            removeEnvironmentData:{
                envId:""
            }
        };
    },
    methods: {
        getData () {
                axios.get("/v1/env/getEnvironmentInfos").then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.list = res.data.message;
                }else{
                    this.$Message.error("获取数据失败")
                }
            }
            )
        },
        addEnvironment(){
            this.$Modal.confirm({
                onOk: () => {
                       this.addEnvironmentNet();
                    },
                    render: (h) => {
                    return h('div',[
                        h('Input', {
                            props: {
                                value: this.addEnvironmentData.env_name,
                                autofocus: true,
                                placeholder: '环境名称'
                            },
                            on: {
                                input: (val) => {
                                    this.addEnvironmentData.env_name = val;
                                }
                            }
                        }),
                    ])
                }
            })
        },
        addEnvironmentNet(){
            axios.post("/v1/env/addEnvironmentItem",
            this.addEnvironmentData
            ).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getData();

                }else{
                    this.$Message.error("失败")
                }
            }
            )
            this.addEnvironmentData = {
                env_name:"",
                userId:1
            };
        },
        removeEnvironment(){
            axios.post("/v1/env/deleteEnvironmentItem",
            this.removeEnvironmentData
            ).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getData();

                }else{
                    this.$Message.error("失败")
                }
            }
            )
        }
    },
    created () {
        this.getData();
    }
};
</script>
