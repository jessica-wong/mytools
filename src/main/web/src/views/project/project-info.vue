<style lang="less">
    @import '../../styles/common.less';

    //项目详情页面
    .card-text{color:grey;margin-top:20px;}
</style>
<template>
    <div>
        <Col span="14">
            <Row>
                <Col>
                    <Card class="margin-right-10">
                        <p slot="title">
                            <Icon type="ios-film-outline"></Icon>
                            项目详情
                        </p>
                        <a slot="extra">
                            <i-button  v-if="editIsHide" type="info" @click="changeEditShow" style="margin-right-10" size="small">编辑</i-button>
                            <i-button  v-if="!editIsHide" type="success" @click="editProjectInfo" style="margin-right-10" size="small">保存</i-button>
                        </a>
                        <ul>
                            <p class="margin-bottom-10">项目描述：
                                <label v-show="editIsHide">{{projectInfo.project_describe}}</label>
                                <Input  v-show="!editIsHide" v-model="projectInfo.project_describe" style="width: 300px" ></Input>
                            </p>
                            <p class="margin-bottom-10">上线时间：
                                <label v-show="editIsHide">{{projectInfo.release_time | timeFilter}}</label>
                                <DatePicker type="datetime" v-show="!editIsHide" v-model="projectInfo.release_time" style="width: 300px" ></DatePicker>
                            </p>
                        </ul>
                    </Card>
                </Col>
                <Col :md="12" :lg="15">
                    <Card class="margin-top-10" style="width:180px" >
                        <div style="text-align:center" @click="jumpTopage">
                            <h2>
                                <Icon type="social-github"></Icon>
                                {{applicationCount}}个
                            </h2>
                            <p class="card-text">影响项目数</p>
                        </div>
                    </Card>
                </Col>
            </Row>
        </Col>
        <Col span="8">
            <Card>
                <p slot="title">
                    <Icon type="document"></Icon>
                    项目动态
                    <div>
                        <ul>
                            <li v-for="log in logListData" class="margin-bottom-10">
                                <Icon type="arrow-right-b"></Icon>
                                {{log.Path}} 有变化
                            </li>
                        </ul>
                    </div>
                </p>
            </Card>
        </Col>
    </div>
</template>
<script>
import canEditTable from './canEditTable.vue';
import {formatDate} from '../../libs/filter.js'
import axios  from 'axios';
    export default {
        data () {
            return {
                logListData:[],
                editIsHide: true,
                projectInfo:{
                    project_describe:"",
                    release_time:"0000-00-00 00:00:00",
                    name:"",
                    projectId:""
                },
                applicationCount:""
            }
        },
        filters:{
            timeFilter(date){
                return formatDate(date,"YYYY-MM-DD HH:mm:ss")
            }
        },
        methods: {
            getProjectInfoById(){
                axios.get("/v1/project/getProjectInfoById",{params:{projectId: this.$route.query.id}}).then((res)=>{
                    console.log(res)
                    if(res.data.success){
                        this.projectInfo = res.data.message[0];
                    }else{
                        this.$Message.error("获取数据失败")
                    }
                })
            },
            changeEditShow() {
                this.editIsHide = !this.editIsHide
            },
            editProjectInfoNet(){
                this.projectInfo.projectId=this.$route.query.id
                axios.post("/v1/project/editProject",this.projectInfo
                ).then((res)=>{
                    if(res.data.success){
                        this.$Message.success("成功")
                        this.getProjectInfoById()
                    }else{
                        this.$Message.error("失败")
                    }
                }
                )
            },
            editProjectInfo () {
                this.changeEditShow()
                this.editProjectInfoNet()
            },
            getProjectLogListData(){
                axios.get("/v1/project/getProjectLogListData",{params:{projectId: this.$route.query.id}}).then((res)=>{
                    console.log(res)
                    if(res.data.success){
                        this.logListData = res.data.message;
                    }else{
                        this.$Message.error("获取数据失败")
                    }
                })
            },
            jumpTopage(){
                this.$router.push({
                    path:"application-version-list",
                    query:{id: this.$route.query.id}
                })
            },
            getApplicationCountByProject(){
                axios.get("/v1/application/getApplicationCountByProject",{params:{projectId: this.$route.query.id}}
                ).then((res)=>{
                    if(res.data.success){
                        this.applicationCount=res.data.message[0].count
                    }else{
                        this.$Message.error("失败")
                    }
                }
                )
            }
        },
        created () {
        this.getProjectInfoById()
        this.getProjectLogListData()
        this.getApplicationCountByProject()
        }
    }
</script>
