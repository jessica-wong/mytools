<style lang="less">
    @import '../../styles/common.less';
    @import './interface-case-edit.less';
</style>

<template>
    <div>
        <Row>
            <Col span="18" class="padding-left-10">
                <Card>
                    <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
                        <FormItem label="Desc" prop="desc">
                            <Input v-model="formValidate.desc" placeholder="Enter case desc" type="textarea" :autosize="{minRows: 2,maxRows: 5}"></Input>
                        </FormItem>
                        <FormItem label="Name" prop="name">
                            <Input v-model="formValidate.name" placeholder="Enter case name"></Input>
                        </FormItem>
                        <FormItem
                                v-for="(itemStep, indexStep) in formValidate.itemsSteps"
                                v-if="itemStep.statusStep"
                                :key="indexStep"
                                :label="'Step ' + itemStep.indexStep"
                                :prop="'itemsSteps.' + indexStep + '.value'"
                                >
                            <Row>
                                <Col span="18">
                                    <Input type="text" v-model="itemStep.value" placeholder="Enter example step1..."></Input>
                                </Col>
                                <Col span="4" offset="1">
                                    <Button type="ghost" @click="handleRemoveStep(indexStep)">Delete</Button>
                                </Col>
                            </Row>
                            <!--<FormItem label="Type" prop="type">
                                <RadioGroup v-model="itemStep.type">
                                    <Radio label=0>API</Radio>
                                    <Radio label=1>SQL</Radio>
                                </RadioGroup>
                            </FormItem>-->
                            <FormItem label="ContentType" prop="content_type">
                                <RadioGroup v-model="itemStep.content_type">
                                    <Radio label=0>json</Radio>
                                    <Radio label=1>form-data</Radio>
                                </RadioGroup>
                            </FormItem>
                            <FormItem label="Request">
                                <Row :gutter="8">
                                    <Col span="2">
                                        <FormItem prop="method">
                                            <Select v-model="itemStep.method" placeholder="Get">
                                                <Option value=0>Get</Option>
                                                <Option value=1>Post</Option>
                                            </Select>
                                        </FormItem>
                                    </Col>
                                    <Col span="6">
                                        <FormItem prop="host">
                                            <Input v-model="itemStep.host" placeholder="如：http://www.baidu.com 可为空"></Input>
                                        </FormItem>
                                    </Col>
                                    <Col span="6">
                                        <FormItem prop="path">
                                            <Input v-model="itemStep.path" placeholder="如：/api/login"></Input>
                                        </FormItem>
                                    </Col>
                                    <!--<Col span="5">
                                        <FormItem>
                                            <Button type="primary" @click="selectInterface(indexStep)" >select Interface </Button>
                                        </FormItem>
                                    </Col>-->
                                </Row>
                            </FormItem>
                            <FormItem label="Header" prop="header">
                                <Input v-model="itemStep.header" type="textarea" :autosize="{minRows: 1,maxRows: 10}"></Input>
                            </FormItem>
                            <FormItem label="Params" prop="params">
                                <Input v-model="itemStep.params" type="textarea" :autosize="{minRows: 2,maxRows: 100}"></Input>
                            </FormItem>

                            <FormItem
                                    v-for="(itemAssert, index) in itemStep.itemsAsserts"
                                    v-if="itemAssert.statusAssert"
                                    :key="index"
                                    :label="'Assert ' + itemAssert.index"
                                    :prop="'itemStep.itemsAsserts.' + index + '.actual'"
                                    >
                                <Row :gutter="10">
                                    <Col span="8">
                                        <Input type="text" v-model="itemAssert.actual" placeholder="实际结果"></Input>
                                    </Col>
                                    <Col span="2">
                                        <FormItem prop="rules">
                                            <Select v-model="itemAssert.rules" placeholder="=">
                                                <Option value=0>=</Option>
                                                <Option value=1>!=</Option>
                                                <Option value=2><</Option>
                                                <Option value=3>></Option>
                                            </Select>
                                        </FormItem>
                                    </Col>
                                    <Col span="8">
                                        <Input type="text" v-model="itemAssert.expect" placeholder="期望结果"></Input>
                                    </Col>
                                    <Col span="2" offset="1">
                                        <Button type="ghost" @click="handleRemoveAssert(indexStep,index)">Delete</Button>
                                    </Col>
                                </Row>
                            </FormItem>
                            <FormItem>
                                <Row>
                                    <Col span="12">
                                        <Button type="dashed" long @click="handleAddAssert(indexStep)" icon="plus-round">Add Assert</Button>
                                    </Col>
                                </Row>
                            </FormItem>

                        </FormItem>

                        <FormItem>
                            <Row>
                                <Col span="12">
                                    <Button type="dashed" long @click="handleAddStep" icon="plus-round">Add Step</Button>
                                </Col>
                            </Row>
                        </FormItem>

                        <FormItem>
                            <Button type="primary" @click="handleSubmit('formValidate')">Submit</Button>
                        </FormItem>
                    </Form>
                </Card>
            </Col>
            <Col span="6" class="padding-left-10">
                <!--<Card>
                    <p slot="title">
                        <Icon type="paper-airplane"></Icon>
                        设置
                    </p>
                    <p class="margin-top-10">
                        <Icon></Icon>&nbsp;&nbsp;状&nbsp;&nbsp;&nbsp; 态：
                        <Select size="small" style="width:90px" value=0>
                            <Option value=0>正常</Option>
                            <Option value=1>弃用</Option>
                        </Select>
                    </p>
                </Card>-->
                <!--<div class="margin-top-10">
                    <Card>
                        <p slot="title">
                            <Icon type="navicon-round"></Icon>
                            选择分组
                        </p>
                        <p type="card">
                            <Tree :data="groupList" @on-check-change="setCaseInGroup" show-checkbox ref="tree"></Tree>
                        </p>
                    </Card>
                </div>-->
                <div class="margin-top-10">
                    <Card>
                        <p slot="title">
                            <Icon type="ios-pricetags-outline"></Icon>
                            调试
                        </p>
                        <Row>
                            <Col span="18">
                                <Select v-model="envSelected" @on-change="handleSelectEnv" placeholder="请选择调试环境，可为空">
                                    <Option v-for="item in envList" :value="item.env_name" :key="item.value">{{ item.env_name }}</Option>
                                </Select>
                            </Col>
                            <Col span="6" class="padding-left-10">
                                <Button  @click="handleCase" long type="ghost">调试</Button>
                            </Col>
                        </Row>
                    </Card>
                </div>
                <div class="margin-top-10">
                    <Card>
                        <p slot="title">
                            <Icon type="clipboard"></Icon>
                            返回信息
                        </p>
                        <p>
                        {{message}}
                        </p>
                    </Card>
                </div>
            </Col>
        </Row>
    </div>
</template>

<script>
import axios  from 'axios';
export default {
    name: 'interface-case-edit',
    data () {
        return {
            envSelected: [], // 选中的环境
            envList:[], // 所有环境列表
            indexStep: 1,
            message:"",
            formValidate: {
                    desc: '',
                    name: '',
                    itemsSteps: [
                        {
                            method: 0,
                            host:'',
                            path: '',
                            header: '',
                            params: '',
                            content_type: 1,
                            statusStep:1,
                            indexStep: 1,
                            itemsAsserts: [
                                {
                                    statusAssert: 1,
                                    index: 1,
                                    actual:'',
                                    rules:'',
                                    expect:''
                                }
                            ]
                        }
                    ],
                },
            ruleValidate: {
                name: [
                        { required: true, message: 'The name cannot be empty', trigger: 'blur' }
                    ],
                desc: [
                        { required: true, message: 'Please enter a personal introduction', trigger: 'blur' },
                        { type: 'string', min: 10, message: 'Introduce no less than 10 words', trigger: 'blur' }
                    ]
                },
            groupList:[],
            selectInterfaceData:"",
            interfaceInfo:[],
            testCaseId:"",
        };
    },
    methods: {
        getData(){
            if (this.$route.query.caseId){
                axios.get("/v1/case/getCaseInfosById",{params:{caseId:this.$route.query.caseId}}
                    ).then((res)=>{
                    if(res.data.success){
                        this.formValidate = res.data.message;
                        console.log(this.formValidate)
                    }else{
                        this.$Message.error("获取数据失败")
                    }
                });
            }else{
                this.formValidate = this.formValidate
            }
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
//            return localStorage.tagsList = JSON.stringify(this.envSelected);
            return localStorage.tagsList = this.envSelected;
        },
        handleCase(){
            if(this.$route.query.caseId){
                const data={}
                data["caseId"]=this.$route.query.caseId
                data["envName"]=this.handleSelectEnv()
                axios.post("/v1/task/startTaskBySingleCase",data).then((res)=>{
                    if(res.data.success){
                        this.$Message.success("触发成功");
                        this.message = res.data.message;
                    }else{
                        this.$Message.error("触发失败");
                    }
                });
            }else{
                if (this.testCaseId==""){
                    this.$Message.error('暂时不能发起调试接，请先保存用例');
                    return ;
                }else{
                    const data={}
                    data["caseId"]=this.testCaseId
                    data["envName"]=this.handleSelectEnv()
                    axios.post("/v1/case/startTaskBySingleCase",data).then((res)=>{
                        if(res.data.success){
                            this.$Message.success("触发成功");
                            this.message = res.data.message;
                        }else{
                            this.$Message.error("触发失败");
                        }
                    });
                }
            }
        },
        handleAddStep () {
            this.indexStep++;
            this.formValidate.itemsSteps.push({
                method: 0,
                host:'',
                path: '',
                header: '',
                params: '',
                content_type: 1,
                indexStep: this.indexStep,
                statusStep: 1,
                itemsAsserts: [
                    {
                        statusAssert: 1,
                        index: 1,
                        actual:'',
                        rules:'',
                        expect:''
                    }
                ]
            });
        },
        handleRemoveStep (indexStep) {
            this.formValidate.itemsSteps[indexStep].statusStep = 0;
        },
        handleAddAssert (indexStep) {
            const index = this.formValidate.itemsSteps[indexStep].itemsAsserts.length + 1;
            alert(index)
            this.formValidate.itemsSteps[indexStep].itemsAsserts.push({
                actual:'',
                rules:'',
                expect:'',
                index: index,
                statusAssert: 1
            });
        },
        handleRemoveAssert (indexStep,index) {
            this.formValidate.itemsSteps[indexStep].itemsAsserts[index].statusAssert = 0;
        },
        handleSubmit (name) {
            this.$refs[name].validate((valid) => {
                if (valid) {
                    if(this.$route.query.caseId){
                        const data= this.formValidate;
                        data["projectId"] = this.$route.query.projectId;
                        data["applicationId"] = this.$route.query.applicationId;
                        data["caseId"] = this.$route.query.caseId;
                        axios.post("/v1/case/updateTestCase",data).then((res)=>{
                            if(res.data.success){
                                this.$Message.success("编辑成功");
//                                alert(JSON.stringify(res.data.message));
                            }else{
                                this.$Message.error("编辑失败");
                            }
                        });
                    }else{
                        const data= this.formValidate;
                        data["projectId"] = this.$route.query.projectId;
                        data["applicationId"] = this.$route.query.applicationId;
                        axios.post("/v1/case/addTestCase",data).then((res)=>{
                            if(res.data.success){
                                this.$Message.success("添加成功");
                                this.testCaseId = res.data.message
                                return this.testCaseId
//                                alert(JSON.stringify(res.data.message));
                            }else{
                                this.$Message.error("添加失败");
                            }
                        });
                    }
                } else {
                    this.$Message.error('请添加有效的name!');
                }
            })
        },
        selectInterface(indexStep){
            this.$Modal.confirm({
                onOk: () => {
                       this.selectInterfaceNet(indexStep);
                    },
                    render: (h) => {
                    return h('div',[
                        h('Input', {
                            props: {
                                value: this.selectInterfaceData,
                                autofocus: true,
                                placeholder: '接口名称'
                            },
                            on: {
                                input: (val) => {
                                    this.selectInterfaceData = val;
                                }
                            }
                        }),
                    ])
                }
            })
        },
        selectInterfaceNet(indexStep){
            axios.get("/v1/webapi/getWebApiInfoByPath",{params:{projectId:this.$route.query.projectId,applicationId:this.$route.query.applicationId,Path:this.selectInterfaceData}}
                ).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.interfaceInfo=res.data.message;
                    this.formValidate.itemsSteps[indexStep].method=res.data.message[0]["Method"];
                    this.formValidate.itemsSteps[path].method=res.data.message[0]["Path"];
                    this.formValidate.itemsSteps[content_type].params=res.data.message[0]["Produces"];
                }else{
                    this.$Message.error("获取数据失败")
                }
            });
        },
    },
    created () {
        this.getData();
        this.getEnv();
    },
};
</script>
