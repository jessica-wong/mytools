<style lang="less">
    @import '../../styles/common.less';
</style>

<template>
    <div>
        <Card class="margin-top-20">
            <div>
                <Table border :columns="columns" :data="data"></Table>
            </div>
        </Card>
    </div>
</template>
<script>
import axios  from 'axios';
export default {
    name: 'interface-test',
    data(){
        return{
            columns: [
                {
                    title: '用例名称',
                    key: 'name',
                },
                {
                    title: '用例描述',
                    key: 'describe'
                },
                {
                    title: '操作',
                    key: 'action',
                    width: 350,
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
                                        let query={caseId:params.row.id}

                                    }
                                }
                            }, '编辑'),
                            h('Button', {
                                props: {
                                    type: 'primary',
                                    size: 'small'
                                },
                                on: {
                                    click: () => {
                                        this.remove(params.index)
                                    }
                                }
                            }, '删除')
                        ]);
                    }
                }
            ],
            data: [],

        }
    },
    methods: {
        getCaseList(){
            return axios.get("/v1/case/getCaseList",
            {params:{applicationId:this.$route.query.applicationId,projectId:this.$route.query.projectId}}).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.data = res.data.message;
                }else{
                    this.$Message.error("获取数据失败")
                }
            })
        },
        remove (index) {
            this.data.splice(index, 1);
        }
    },
    created () {
        this.getCaseList()
    }
}
</script>