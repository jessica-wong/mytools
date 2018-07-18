<style lang="less">
    @import '../../styles/common.less';
</style>

<template>
    <div>
        <Row type="flex" class="height-100">
            <Col span="8">
                <i-button type="success" @click="addApplicationVersion" style="margin-top-10">添加应用</i-button>
            </Col>
        </Row>
        <Row class="margin-top-20">
            <Col span="8" class="padding-left-10" v-for="item in applicationVersionList">
                <Card style="width:320px" class="margin-top-20">
                    <p slot="title">
                        {{ item.name }}
                    </p>
                    <a slot="extra">
                        <i-button type="success" @click="addConfigItem(item.application_id)" style="margin-top-10">配置</i-button>
                        <i-button type="success" @click="removeApplicationVersion(item.application_id)" style="margin-top-10">移除</i-button>
                    </a>
                    <ul>
                        <div >
                            <!--<p class="margin-bottom-10">git地址：
                                <label>{{item.git_url}}</label>
                            </p>
                            <p class="margin-bottom-10">swagger地址：
                                <label>{{item.swagger_url}}</label>
                            </p>
                            <p class="margin-bottom-10">test地址：
                                <label >{{item.test_url}}</label>
                            </p>-->
                            <a style="text-align:center" @click="jumpTopage(item.application_id)">
                                查看项目中接口变动详情
                            </a>
                            <!--<p>
                                <a>影响接口数</a>
                                <span>
                                    {{ item.number_interface }}
                                </span>
                            </p>
                            <p>
                                <a>影响页面数</a>
                                <span>
                                    {{ item.number_page }}
                                </span>
                            </p>-->
                        </div>
                    </ul>
                </Card>
            </Col>
        </Row>
        <Modal
            v-model="modal"
            title="选择本次项目影响的应用"
            @on-ok="addApplicationVersionNet"
            @on-cancel="modal=false">
            <Select v-model="addApplicationVersionData.applicationId" style="width:200px">
                <Option v-for="application in applicationList" :value="application.id" :key="application.id">{{ application.name }}</Option>
            </Select>
        </Modal>
        <!--<Modal
            v-model="showAddConfig"
            title="编辑项目相关配置"
            @on-ok="addApplicationVersionConfig"
            @on-cancel="showAddConfig=false">
            <Input v-model="formItem.gitUrl" placeholder="https://github.com/" style="width: 300px" class="margin-bottom-10">项目git地址</Input>
            <Input v-model="formItem.swaggerUrl" placeholder="http://test.com/swagger/v1/swagger.json" style="width: 300px" class="margin-bottom-10">项目swagger地址</Input>
            <Input v-model="formItem.testUrl" placeholder="http://testpro2.shcoolpal.cn" style="width: 300px" class="margin-bottom-10">项目测试地址</Input>
        </Modal>-->
    </div>
</template>

<script>
import axios  from 'axios';
export default {
    name: 'application-version-list',
    data () {
        return {
            applicationVersionList: [
            ],
            applicationList:[
            ],
            addApplicationVersionData:{
                applicationId:"",
                projectId:"",
                departmentId:""
            },
            modal:false,
            modal1:"",
            formItem:{
                gitUrl:"",
                swaggerUrl:"",
                testUrl:"",
                applicationId:"",
                projectId:""
            }
        }
    },
    methods: {
        getApplicationOfProject(){
            axios.get("/v1/application/getApplicationByProjectId",{params:{projectId: this.$route.query.id}}).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.applicationVersionList = res.data.message;
                }else{
                    this.$Message.error("获取数据失败")
                }
            })
        },
        getApplicationList(){
            return axios.get("/v1/application/getApplicationList").then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.applicationList = res.data.message;
                }else{
                    this.$Message.error("获取数据失败")
                }
            })
        },
        addApplicationVersion(id){
            this.getApplicationList().then(()=>{
//                console.log(">>>>>>>>>>>>>>>>>>>>>>",this.applicationList)
                this.applicationList.map((one)=>{
                    one.value = one.id;
                    one.lable = one.name;
                });
                this.modal=true;
            });
        },
        addApplicationVersionNet(id){
            this.addApplicationVersionData.projectId=this.$route.query.id
            this.departmentId=1
            axios.post("/v1/application/addApplicationVersion",
                this.addApplicationVersionData
                ).then((res)=>{
                    //console.log(res)
                    if(res.data.success){
                        this.$Message.success("成功")
                        this.getApplicationOfProject()
                    }else{
                        this.$Message.error("失败")
                    }
                }
                )
                this.addApplicationVersionData = {
                    applicationId:"",
                    projectId:"",
                    departmentId:1
            };
        },
        addConfigItem (id) {
            this.$router.push({
                    name:'version-config',
                    query:{projectId: this.$route.query.id,applicationId:id}
            })
        },
        removeApplicationVersion(id){
            console.log(">>>>>>>",id)
//            this.removeApplicationVersionData.versionId=this.item.application_id
            axios.post("/v1/application/deleteApplicationVersion",{
                "applicationId":id,"projectId":this.$route.query.id
            }).then((res)=>{
                //console.log(res)
                if(res.data.success){
                    this.$Message.success("成功")
                    this.getApplicationOfProject()
                }else{
                    this.$Message.error("失败")
                }
            })
        },
        jumpTopage(id){
            this.$router.push({
                    name:"interface-list",
                    query:{projectId: this.$route.query.id,applicationId:id}
            })
        },
    },
    created () {
        this.getApplicationOfProject()
        }
};
</script>
