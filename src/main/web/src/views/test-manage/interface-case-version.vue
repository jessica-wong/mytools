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
                    title: '项目名称',
                    key: 'name',
                },
                {
                    title: '项目描述',
                    key: 'project_describe'
                },
                {
                    title: '上线时间',
                    key: 'release_time'
                },
                {
                    title: '操作',
                    key: 'action',
                    width: 400,
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
                                        let query={projectId:params.row.id,applicationId:this.$route.query.applicationId}
                                        this.$router.push({
                                            name:"interface-case-list",
                                            query:query
                                        })
                                    }
                                }
                            }, '查看详情'),
                            h('Button', {
                                props: {
                                    type: 'primary',
                                    size: 'small'
                                },
                                on: {
                                    click: () => {
                                        this.createCaseData.projectId=params.row.id
                                        this.createCaseData.applicationId=this.$route.query.applicationId
                                        this.createCase()
                                    }
                                }
                            }, '生成用例')
                        ]);
                    }
                }
            ],
            data: [],
            createCaseData:{
                projectId:"",
                applicationId:""
            },
        }
    },
    methods: {
        getProjectListByApplicationId(){
            return axios.get("/v1/project/getProjectListByApplicationId",
            {params:{applicationId: this.$route.query.applicationId}}).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.data = res.data.message;
                }else{
                    this.$Message.error("获取数据失败")
                }
            })
        },
        createCase(){
            axios.post("/v1/case/createTestCase",this.createCaseData).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.$Message.success("创建成功")
                }else{
                    this.$Message.error("创建失败")
                }
            })
        }
    },
    created () {
        this.getProjectListByApplicationId()
    }
}
</script>