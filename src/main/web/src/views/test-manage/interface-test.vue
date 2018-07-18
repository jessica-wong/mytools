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
                    title: '应用名称',
                    key: 'name',
                },
                {
                    title: '应用描述',
                    key: 'application_describe'
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
                                        let query={applicationId:params.row.id}
                                        this.$router.push({
                                            name:"interface-case-version",
                                            query:query
                                        })
                                    }
                                }
                            }, '查看详情'),
//                            h('Button', {
//                                props: {
//                                    type: 'primary',
//                                    size: 'small'
//                                },
//                                on: {
//                                    click: () => {
//                                        this.remove(params.index)
//                                    }
//                                }
//                            }, 'Delete')
                        ]);
                    }
                }
            ],
            data: [],

        }
    },
    methods: {
        getApplicationList(){
            return axios.get("/v1/application/getApplicationList").then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.data = res.data.message;
                }else{
                    this.$Message.error("获取数据失败")
                }
            })
        }
    },
    created () {
        this.getApplicationList()
    }
}
</script>