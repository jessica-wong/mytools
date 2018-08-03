<style lang="less">
    @import '../../styles/common.less';
</style>

<template>
    <div>
         <Card>
             <p class="margin-bottom-10">gitUrl：
                <label v-show="editIsHide">{{formItem.git_url}}</label>
                <Input v-show="!editIsHide" v-model="formItem.git_url" style="width: 500px"  placeholder="Example:http://git.greedyint.com"></Input>
             </p>
             <p class="margin-bottom-10">swaggerUrl:
                <label v-show="editIsHide">{{formItem.swagger_url}}</label>
                <Input v-show="!editIsHide" v-model="formItem.swagger_url" style="width: 500px"  placeholder="Example:http://testpro.schoolpal.cn/swagger/v1/swagger.json"></Input>
             </p>
             <p class="margin-bottom-10">testUrl
                <label v-show="editIsHide">{{formItem.test_url}}</label>
                <Input v-show="!editIsHide" v-model="formItem.test_url" style="width: 500px"  placeholder="Example:http://testpro.schoolpal.cn"></Input>
             </p>
             <p class="margin-bottom-10">
                <i-button  v-if="editIsHide" type="info" @click="changeEditShow" style="margin-right-10" size="small">编辑</i-button>
                <i-button  v-if="!editIsHide" type="success" @click="eidtApplicationVersionConfig" style="margin-right-10" size="small">保存</i-button>
             </p>
        </Card>
    </div>
</template>

<script>
import axios  from 'axios';
export default {
    name: 'version-config',
    data () {
        return {
            formItem:{
                git_url:"",
                swagger_url:"",
                test_url:"",
                application_id:"",
                project_id:""
            },
            editIsHide: true,
        }
    },
    methods: {
        getVersionConfig(){
            return axios.get("/v1/application/getVersionConfig",{params:{projectId:this.$route.query.projectId,applicationId:this.$route.query.applicationId}}).then((res)=>{
                console.log(res)
                if(res.data.success){
                    if(res.data.message.length==0){
                        this.formItem = {
                            git_url:"",
                            swagger_url:"",
                            test_url:"",
                            application_id:"",
                            project_id:""
                        }
                    }else{
                        this.formItem = res.data.message[0];
                    }
                }else{
                    this.$Message.error("获取数据失败")
                }
            })
        },
        eidtApplicationVersionConfig(){
            if(this.formItem.id>0){
                console.log("?????"+this.formItem.id.length)
                axios.post("/v1/application/editVersionConfig",this.formItem
                ).then((res)=>{
                    if(res.data.success){
                        this.$Message.success("成功")
                        this.editIsHide = !this.editIsHide
                    }else{
                        this.$Message.error("失败")
                    }
                })
            }else{
                this.formItem.application_id=this.$route.query.applicationId
                this.formItem.project_id=this.$route.query.projectId
                axios.post("/v1/application/addApplicationVersionConfig",this.formItem
                ).then((res)=>{
                    if(res.data.success){
                        this.$Message.success("成功")
                        this.editIsHide = !this.editIsHide
                    }else{
                        this.$Message.error("失败")
                    }
                })
            }
        },
        changeEditShow() {
            this.editIsHide = !this.editIsHide
        },
    },
    created () {
            this.getVersionConfig().then(()=>{
                console.log(this.formItem)
                if(!this.formItem.git_url.length && !this.formItem.swagger_url.length && !this.formItem.test_url.length){
                    this.changeEditShow()
                    }
            })
        }
};
</script>
