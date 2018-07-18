<style lang="less">
    @import '../../../styles/common.less';
</style>

<template>
    <div>
        <Col span="4">
            <Card>
                <Tree :data="groupList" @on-check-change="setInterfaceInGroup" show-checkbox ref="tree" style="width:260px"></Tree>
            </Card>
        </Col>
        <Col span="14" class="padding-left-10">
            <Card>
                <div>
                    <Transfer
                        :data="caseData"
                        :target-keys="targetKeys3"
                        :list-style="listStyle"
                        :render-format="render3"
                        :operations="['添加到套件','从套件中移除']"
                        filterable

                        @on-change="handleChange3">

                    </Transfer>
                </div>
            </Card>
        </Col>
        <Col span="6" class="padding-left-10">
            <Card>
                <p slot="title">
                    <Icon type="ios-pricetags-outline"></Icon>
                    选择执行环境
                </p>
                <Row>
                    <Col span="18">
                        <Select v-model="envSelected" @on-change="handleSelectEnv" placeholder="请选择调试环境，不可为空">
                            <Option v-for="item in envList" :value="item.value" :key="item.value">{{ item.value }}</Option>
                        </Select>
                    </Col>
                    <Col span="6" class="padding-left-10">
                        <Button  @click="handleCase" long type="ghost">执行用例</Button>
                    </Col>
                </Row>
            </Card>
        </Col>
    </div>
</template>
<script>
import axios  from 'axios';
    export default {
        data () {
            return {
                groupList:[],
                caseData: [],
                targetKeys3: this.getTargetKeys(),
                listStyle: {
                    width: '350px',
                    height: '800px'
                },
                envSelected: [], // 选中的环境
                envList:[], // 所有环境列表
            }
        },
        methods: {
            getGroupList(){
                axios.get("/v1/group/getGroupByProjectId",{params:{projectId:this.$route.query.projectId,type:1}}).then((res)=>{
                    console.log(res);
                    if(res.data.success){
                        const that =this;
                        res.data.message.forEach(function(item){

                            that.groupList.push(item);
                        });
                    }else{
                        this.$Message.error("获取数据失败")
                    }
                })
            },
            getCaseData(group_id){
                axios.get("/v1/case/getCaseInfosByCondition",{params:{projectId:this.$route.query.projectId,groupId:group_id,offset:0,limit:10}}).then((res)=>{
                    console.log(res);
                    if(res.data.success){
                        this.$Message.success("获取数据成功")
                        let caseData=[];
                        for (let i = 1; i <= res.data.message.length; i++) {
                            caseData.push({
                                key: res.data.message[i-1].id,
                                label: res.data.message[i-1].name,
                                disabled: 0
                            });
                        }
                        return caseData;
                    }else{
                        this.$Message.error("获取数据失败")
                    }
                })
            },
            getMockData () {
                let mockData = [];
                for (let i = 1; i <= 20; i++) {
                    mockData.push({
                        key: i.toString(),
                        label: 'Content ' + i,
                        disabled: Math.random() * 3 < 1
                    });
                }
                return mockData;
            },
            getTargetKeys () {
                return this.getMockData()
                        .filter(() => Math.random() * 2 > 1)
                        .map(item => item.key);
            },
            handleChange3 (newTargetKeys) {
                this.targetKeys3 = newTargetKeys;
            },
            render3 (item) {
                return item.label;
            },
            setInterfaceInGroup(){
                const groupCheckedData=this.$refs.tree.getCheckedNodes()
                const testData= groupCheckedData[groupCheckedData.length-1]
                alert(JSON.stringify(testData))
                this.getCaseData(testData["groupId"])
            },
            getEnv(){
                axios.get("/v1/env/getEnvironmentInfoByUserId",{params:{userId:1}}
                    ).then((res)=>{
                    console.log(res)
                    if(res.data.success){
                        const that = this
                        res.data.message.forEach(function(item){
                            const tmpJson ={}
                            tmpJson["value"]=item["name"]
                            that.envList.push(tmpJson);
                        });
                    }else{
                        this.$Message.error("获取数据失败")
                    }
                });
            },
            handleSelectEnv () {
                localStorage.envsList = JSON.stringify(this.envSelected);
            },
            handleCase(){
            }
        },
        created () {
            this.getGroupList();
            this.getEnv();

        },
    }
</script>