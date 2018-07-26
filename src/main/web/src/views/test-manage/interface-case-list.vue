<style lang="less">
    @import '../../styles/common.less';
</style>

<template>
    <div>
        <Card class="margin-top-20">
            <div>
                <Row type="flex" class="height-100">
                    <Col span="8">
                        <i-button type="success" @click="addCase" style="margin-top-10">新增用例</i-button>
                        <i-button type="success" @click="modalImport = true" style="margin-top-10">导入用例</i-button>
                        <i-button type="success" @click="modalExecute = true" style="margin-top-10">批量执行</i-button>
                    </Col>
                    <Col span='8'>
                        <Input v-model="searchValue" placeholder="用例名">
                            <Button slot="append" icon="ios-search"  @click="searchCaseByName"></Button>
                        </Input>
                    </Col>
                </Row>
                <Row class="margin-top-20">
                    <Col >
                        <Table border :columns="columns" :data="data"></Table>
                    </Col>
                </Row>
            </div>
        </Card>
        <Modal
            v-model="modalImport"
            title="选择导入方式"
            @on-ok="ok"
            @on-cancel="cancel">
            <a>Json文件</a>
            <a>Har文件</a>
        </Modal>
        <Modal
            v-model="modalExecute"
            title="选择环境"
            @on-ok="execute"
            @on-cancel="cancel">
            <Select v-model="envSelected" @on-change="handleSelectEnv" placeholder="请选择调试环境，可为空">
                <Option v-for="item in envList" :value="item.env_name" :key="item.value">{{ item.env_name }}</Option>
            </Select>
        </Modal>
    </div>

</template>
<script>
import axios  from 'axios';
export default {
    name: 'interface-test',
    data(){
        return{
            envSelected: [],
            envList:[], // 所有环境列表
            columns: [
                {
                    type: 'selection',
                    width: 60,
                    align: 'center'
                },
                {
                    title: '用例名称',
                    key: 'name',
                },
                {
                    title: '用例描述',
                    key: 'case_describe'
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
                                        this.$router.push({
                                        path:"/test-manage/interface-case-edit",
                                        query:{projectId:this.$route.query.projectId,applicationId:this.$route.query.applicationId,caseId:params.row.id}})
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
                                        this.removeCaseData.caseId = params.row.id
                                        this.removeCase()
                                    }
                                }
                            }, '删除')
                        ]);
                    }
                }
            ],
            data: [],
            modalImport: false,
            modalExecute:false,
            searchValue:"",
            removeCaseData:{
                caseId:""
            },
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
        removeCase() {
                axios.post("/v1/case/deleteTestCase",this.removeCaseData).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getCaseList();

                }else{
                    this.$Message.error("失败")
                }
            })
            this.removeCaseData = {
                caseId:"",
            };
        },
        addCase(){
            this.$router.push({
            path:"/test-manage/interface-case-edit",
            query:{projectId:this.$route.query.projectId,applicationId:this.$route.query.applicationId}})
        },
        getEnv(){
            axios.get("/v1/env/getEnvironmentInfos"
                ).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.envList=res.data.message;
                }else{
                    this.$Message.error("获取数据失败")
                }
            });
        },
        handleSelectEnv () {
            return localStorage.tagsList = this.envSelected;
        },
        importCase(){
        },
        handleSelectAll (status) {
            this.$refs.selection.selectAll(status);
        },
        ok () {
            this.$Message.info('Clicked ok');
        },
        cancel () {
            this.$Message.info('Clicked cancel');
        },
        execute(){
            const data={}
            data["projectId"]=this.$route.query.projectId
            data["applicationId"]=this.$route.query.applicationId
            data["envName"]=this.handleSelectEnv()
            axios.post("/v1/task/startTaskByBatchCase",data).then((res)=>{
                if(res.data.success){
                    this.$Message.success("触发成功");
                    this.$router.push({
                        path:"/test-manage/interface-test-result",
                        query:{projectId:this.$route.query.projectId,applicationId:this.$route.query.applicationId}})
                }else{
                    this.$Message.error("触发失败");
                }
            });
        },
        searchCaseByName(){
            axios.get("/v1/case/searchCaseByName",{params:{applicationId:this.$route.query.applicationId,projectId:this.$route.query.projectId,searchValue:this.searchValue}}).then((res)=>{
                if(res.data.success){
                    this.$Message.success("成功");
                    this.data=res.data.message
                }else{
                    this.$Message.error("失败")
                }
            })
        },
    },
    created () {
        this.getCaseList();
        this.getEnv();
    }
}
</script>