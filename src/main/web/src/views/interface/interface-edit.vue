<style lang="less">
    @import '../../styles/common.less';
    @import './interface-edit.less';
</style>

<template>
    <div>
        <Row>
            <Col span="18">
                <Card>
                    <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
                        <FormItem label="Name" prop="name">
                            <Input v-model="formValidate.name" placeholder="Enter interface name"></Input>
                        </FormItem>
                        <FormItem label="URL" prop="url">
                            <Input v-model="formValidate.url" placeholder="Enter interface url"></Input>
                        </FormItem>
                        <FormItem label="Method" prop="method">
                            <Select v-model="formValidate.method" placeholder="Select interface method">
                                <Option value=0>Get</Option>
                                <Option value=1>Post</Option>
                            </Select>
                        </FormItem>
                        <FormItem label="Format" prop="format">
                            <RadioGroup v-model="formValidate.format">
                                <Radio label="0">application/form-data</Radio>
                                <Radio label="1">application/json</Radio>
                            </RadioGroup>
                        </FormItem>
                        <FormItem label="Type" prop="response_type">
                            <RadioGroup v-model="formValidate.response_type">
                                <Radio label="0">json</Radio>
                                <Radio label="1">view</Radio>
                            </RadioGroup>
                        </FormItem>
                        <FormItem label="Params" prop="params">
                            <Input v-model="formValidate.params" type="textarea" :autosize="{minRows: 2,maxRows: 100}" placeholder="Request params..."></Input>
                        </FormItem>
                        <FormItem label="Success" prop="success_response">
                            <Input v-model="formValidate.success_response" type="textarea" :autosize="{minRows: 2,maxRows: 100}" placeholder="Success response..."></Input>
                        </FormItem>
                        <FormItem label="Failure" prop="failure_response">
                            <Input v-model="formValidate.failure_response" type="textarea" :autosize="{minRows: 2,maxRows: 100}" placeholder="Failure response..."></Input>
                        </FormItem>
                        <FormItem label="Desc" prop="describe">
                            <Input v-model="formValidate.describe" type="textarea" :autosize="{minRows: 2,maxRows: 50}" placeholder="Enter your describe..."></Input>
                        </FormItem>
                        <FormItem>
                            <Button type="primary" @click="handleSubmit('formValidate')">Submit</Button>
                            <Button type="ghost" @click="handleReset('formValidate')" style="margin-left: 8px">Reset</Button>
                        </FormItem>
                    </Form>
                </Card>
            </Col>
            <Col span="6" class="padding-left-10">
                <Card>
                    <p slot="title">
                        <Icon type="paper-airplane"></Icon>
                        设置
                    </p>
                    <p class="margin-top-10">
                        <Icon type="android-time"></Icon>&nbsp;&nbsp;状&nbsp;&nbsp;&nbsp; 态：
                        <Select v-model="formValidate.status" placeholder="正常" style="width:150px;">
                            <Option value=0>正常</Option>
                            <Option value=1>弃用</Option>
                        </Select>
                    </p>
                </Card>
                <div class="margin-top-10">
                    <Card>
                        <p slot="title">
                            <Icon type="navicon-round"></Icon>
                            选择分组
                        </p>
                        <p type="card">
                            <Tree :data="groupList" @on-check-change="setInterfaceInGroup" show-checkbox ref="tree"></Tree>
                        </p>
                    </Card>
                </div>
                <div class="margin-top-10">
                    <Card>
                        <p slot="title">
                            <Icon type="compose"></Icon>
                            修改记录
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
    name: 'interface-edit',
    data () {
        return {
            interfaceStateList: {status: ''},
            formValidate: {
                name: '',
                url: '',
                method: '',
                format: '',
                response_type: '',
                params: '',
                success_response: '',
                failure_response:'',
                describe: '',
                create_userid:1,
                status: 0,
                projectid:'',
                groupid:""
            },
            ruleValidate: {
                name: [
                        { required: true, message: 'The name cannot be empty', trigger: 'blur' }
                    ],
                url: [
                        { required: true, message: 'The url cannot be empty', trigger: 'blur' }
                    ],
                method: [
                        { required: true, message: 'The method cannot be empty', trigger: 'blur' }
                    ],
                success_response: [
                        { required: true, message: 'The success cannot be empty', trigger: 'blur' }
                    ],
                response_type: [
                        { required: true, message: 'Please select type', trigger: 'change' }
                    ],
                format: [
                        { required: true, message: 'Please select format', trigger: 'change' }
                    ],
                describe: [
                        { required: true, message: 'Please enter a personal introduction', trigger: 'blur' },
                        { type: 'string', min: 10, message: 'Introduce no less than 10 words', trigger: 'blur' }
                    ]
                },
            groupList:[],
            setGroupData:{
                interfaceId:'',
                groupId:''
            }
        };
    },
    methods: {
        getData(){
            axios.get("/v1/interface/getInterfaceInfoById",{params:{interfaceId:this.$route.query.interfaceId}}
                ).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.formValidate.name = res.data.message[0].name;
                    this.formValidate.url = res.data.message[0].url;
                    this.formValidate.method = res.data.message[0].method;
                    this.formValidate.format = res.data.message[0].format;
                    this.formValidate.response_type = res.data.message[0].response_type;
                    this.formValidate.params = res.data.message[0].params;
                    this.formValidate.success_response = res.data.message[0].success_response;
                    this.formValidate.failure_response = res.data.message[0].failure_response;
                    this.formValidate.describe = res.data.message[0].interface_describe;
                    this.formValidate.status = res.data.message[0].status;
                    this.formValidate.groupid = res.data.message[0].groupid;
                }else{
                    this.$Message.error("获取数据失败")
                }
            }
            )
        },
        getGroupList(){
            axios.get("/v1/group/getGroupByProjectId",{params:{projectId:this.$route.query.projectId,type:0}}).then((res)=>{
                console.log(res);
                if(res.data.success){
                    const that =this;
                    res.data.message.forEach(function(item){
                        console.log(item);
                        that.groupList.push(item);
                    });
                }else{
                    this.$Message.error("获取数据失败")
                }
            })
        },
        handleSubmit (name) {
            this.$refs[name].validate((valid) => {
                if (valid) {
                    this.formValidate.projectid=this.$route.query.projectId
                    if(this.formValidate.groupid ==""){
                       this.$Message.error("请选择分组")
                       return
                    }
                    axios.post("/v1/interface/addInterfaceItem",this.formValidate).then((res)=>{
                        console.log(res)
                        if(res.data.success){
                            this.$Message.success("成功");
                            this.$router.push({path:"/interface/interface-info",query:{id:1}});
                        }else{
                            this.$Message.error("失败")
                        }
                    }
                    );
                } else {
                    this.$Message.error('Fail!');
                }
            })
        },
        handleReset (name) {
            this.$refs[name].resetFields();
        },
        setInterfaceInGroup(){
            console.log(this.$refs.tree.getCheckedNodes())
            const groupCheckedData=this.$refs.tree.getCheckedNodes()
            this.formValidate.groupid = this.$refs.tree.getCheckedNodes()[0].groupId
        }
    },
    created () {
        this.getData();
        this.getGroupList();
    },
};
</script>
