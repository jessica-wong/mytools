<style lang="less">
    @import '../../styles/common.less';
</style>

<template>
    <div>

    </div>

</template>
<script>
import axios  from 'axios';
export default {
    data(){
        return{

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

    },
    created () {
        this.getCaseList();

    }
}
</script>