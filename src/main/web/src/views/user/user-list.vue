<style lang="less">
    @import '../../styles/common.less';
</style>

<template>
    <div>
        <Row class="margin-top-20">
            <Col span="18">
                <Card>
                    <div >
                        <Table border :columns="lsitColumns" :data="list" ></Table>
                    </div>
                </Card>
            </Col>
        </Row>
    </div>
</template>

<script>
import axios  from 'axios';
export default {
    name: 'case-list',
    data () {
        return {
            lsitColumns: [
                {
                    title: '名字',
                    key: 'username',
                    render: (h, params) => {
                        return h('div', [
                            h('Icon', {
                                props: {
                                    type: 'person'
                                }
                            }),
                            h('strong', params.row.username)
                        ]);
                    }
                },
                {
                    title: '部门',
                    key: 'department_id'
                },
                {
                    title: '角色',
                    key: 'roles'
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
                                        this.getUserInfo(params.index)
                                    }
                                }
                            }, '详情'),
                            h('Button', {
                                props: {
                                    type: 'primary',
                                    size: 'small'
                                },
                                on: {
                                    click: () => {
                                        this.team(params.index)
                                    }
                                }
                            }, '权限分配')
                        ]);
                    }
                }
            ],
            list: [],
            userInfo:[]
        };
    },
    methods: {
        getData () {
            axios.get("/v1/user/getUserList"
                ).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.list=[]
                    this.list = res.data.message;
                }else{
                    this.$Message.error("获取数据失败");
                }
            }
            )
        },
        getUserInfo(index){
            axios.get("/v1/user/getUserInfo",{params:{userName:this.list[index].username}}
                ).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.userInfo=[]
                    this.userInfo = res.data.message;
                    this.show()
                }else{
                    this.$Message.error("获取数据失败");
                }
            }
            )
        },

        show () {
            this.$Modal.info({
                title: 'User Info',
                content: `姓名：${this.userInfo[0].username}<br>部门：${this.userInfo[0].department_id}<br>角色：${this.userInfo[0].roles}<br>手机：${this.userInfo[0].mobile}<br>状态:${this.userInfo[0].status}`
            })
        },
        team (index) {
            this.list.splice(index, 1);
        },
    },
    created () {
        this.getData()
    },
}
</script>
