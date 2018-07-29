
<template>
    <div>
        <Row>
            <Col span="24">
                <Card>
                    <p slot="title">
                        <Icon type="ios-list"></Icon>
                        触发任务列表
                    </p>
                    <Row type="flex" justify="center" align="middle" >
                        <Table :columns="taskColumns" :data="taskData" style="width: 100%;"></Table>
                    </Row>
                </Card>
            </Col>
        </Row>
    </div>
</template>

<script>
import axios  from 'axios';
export default {
    name: 'task-trigger',
    data () {
        return {
            taskColumns: [
                {
                    title: '任务ID',
                    key: 'id',
                    align: 'center'
                },
                {
                    title: '项目名称',
                    key: 'project_name'
                },
                {
                    title: '应用名称',
                    key: 'application_name'
                },
                {
                    title: '状态',
                    key: 'status',
                    render: (h, params) => {
                        const row = params.row;
                        const color = row.status === 1 ? 'blue' : row.status === 2 ? 'green' : row.status === 0 ? 'grey' : 'red';
                        const text = row.status === 1 ? '运行' : row.status === 2 ? '成功' : row.status === 0 ? '排队' : '失败';

                        return h('Tag', {
                            props: {
                                type: 'dot',
                                color: color
                            }
                        }, text);
                    }
                },
                {
                    title: '开始时间',
                    key: 'build_start',
                    width: 100
                },
                {
                    title: '结束时间',
                    key: 'build_end',
                    width: 100
                },
                {
                    title: '用户',
                    key: 'create_username'
                },
                {
                    title: '操作',
                    key: 'details',
                    align: 'center',
                    render: (h, params) => {
                        return h('Button', {
                            props: {
                                type: 'text',
                                size: 'small'
                            },
                            on: {
                                click: () => {
                                    let query = { instanceId: params.row.id };
                                    this.$router.push({
                                        name: 'task-result',
                                        query: query
                                    });
                                }
                            }
                        }, '查看详情');
                    }
                }
            ],
            taskData: [
            ]
        };
    },
    methods:{
        getCaseInstanceInfos () {
            axios.get("/v1/instance/getTaskInstanceInfos",{}).then((res)=>{
                console.log(res);
                if(res.data.success){
                    const that =this;
                    res.data.message.forEach(function(item){
                        console.log(item);
                        that.taskData.push(item);
                    });
                }else{
                    this.$Message.error("获取数据失败")
                }
            })
        },
        getCaseInstanceInfoById (taskInstanceId) {
            axios.get("/v1/instance/getTaskInstanceInfoById",{params:{"instanceId":taskInstanceId}}).then((res)=>{
                console.log(res);
                if(res.data.success){
                    const that =this;
                    res.data.message.forEach(function(item){
                        console.log(item);
                        that.taskData.push(item);
                    });
                }else{
                    this.$Message.error("获取数据失败")
                }
            })
        },
    },
    computed: {
        avatorImage () {
            return localStorage.avatorImgPath;
        }
    },
    created () {
        const taskInstanceId= this.$route.query.taskInstanceId;
        if(taskInstanceId != null){
            this.getCaseInstanceInfoById(taskInstanceId);
        }else{taskInstanceId
            this.getCaseInstanceInfos();
        }

    }
};
</script>
