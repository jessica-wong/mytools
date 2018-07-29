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
    data(){
        return{
            columns: [
                {
                    title: '名称用例',
                    key: 'case_name',
                    width: 200,
                },
                {
                    title: '运行时间(ms)',
                    key: 'runtime'
                },
                {
                    title: '执行结果',
                    key: 'exe_status'
                },
                {
                    title: '结果详情',
                    key: 'message'
                },
            ],
            data: []
        }
    },
    methods: {
        getCaseResultInfosByInstanceId(instanceId){
            return axios.get("/v1/case/getCaseResultInfosByInstanceId",
            {params:{"instanceId": instanceId}}).then((res)=>{
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
        const instanceId = this.$route.query.instanceId
        if(instanceId != null){
            this.getCaseResultInfosByInstanceId(instanceId)
        }else{
            this.$Message.error("需要指定instanceId参数")
        }

    }
}
</script>