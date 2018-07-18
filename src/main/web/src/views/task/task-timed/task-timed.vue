
<template>
    <div>
        <Row>
            <Col span="24">
                <Card>
                    <p slot="title">
                        <Icon type="ios-list"></Icon>
                        定时任务列表
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
export default {
    name: 'task-trigger',
    data () {
        return {
            taskColumns: [
                {
                    type: 'index',
                    title: '序号',
                    width: 60
                },
                {
                    title: '任务ID',
                    key: 'task_id',
                    align: 'center'
                },
                {
                    title: '状态',
                    key: 'status',
                    render: (h, params) => {
                        const row = params.row;
                        const color = row.status === 1 ? 'blue' : row.status === 2 ? 'green' : 'red';
                        const text = row.status === 1 ? '构建中' : row.status === 2 ? '构建完成' : '构建失败';

                        return h('Tag', {
                            props: {
                                type: 'dot',
                                color: color
                            }
                        }, text);
                    }
                },
                {
                    title: '用户',
                    key: 'user_name'
                },
                {
                    title: '详情',
                    key: 'show_more',
                    align: 'center',
                    render: (h, params) => {
                        return h('Button', {
                            props: {
                                type: 'text',
                                size: 'small'
                            },
                            on: {
                                click: () => {
                                    let argu = { order_id: params.row.order_id };
                                    this.$router.push({
                                        name: 'order-info',
                                        params: argu
                                    });
                                }
                            }
                        }, '查看详情');
                    }
                }
            ],
            taskData: [
                {
                    task_id: '1000001',
                    user_name: 'Aresn',
                    status:Math.floor(Math.random() * 3 + 1)
                },
                {
                    task_id: '1000002',
                    user_name: 'Lison',
                    status:Math.floor(Math.random() * 3 + 1)
                },
                {
                    task_id: '1000003',
                    user_name: 'lili',
                    status:Math.floor(Math.random() * 3 + 1)
                },
                {
                    task_id: '1000004',
                    user_name: 'lala',
                    status:Math.floor(Math.random() * 3 + 1)
                }
            ]
        };
    },
    computed: {
        avatorImage () {
            return localStorage.avatorImgPath;
        }
    }
};
</script>
