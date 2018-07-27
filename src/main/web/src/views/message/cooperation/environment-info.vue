<style lang="less">
    @import '../../styles/common.less';
    @import './environment-info.less';
</style>

<template>
    <div>
        <Row>
            <Col span="18">
                <Card>
                    <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
                        <FormItem label="环境名称" prop="name">
                            <Input v-model="formValidate.name" placeholder="Enter environment name"></Input>
                        </FormItem>
                        <FormItem label="前置URL" prop="url">
                            <Input v-model="formValidate.url" placeholder="Example http://www.baidu.com"></Input>
                        </FormItem>
                        <FormItem label="DB名称" prop="dbname">
                            <Input v-model="formValidate.dbname" placeholder="DataBase name..."></Input>
                        </FormItem>
                        <FormItem label="DBHostName" prop="dbhostname">
                            <Input v-model="formValidate.dbhostname" placeholder="DataBase hostName..."></Input>
                        </FormItem>
                        <FormItem label="DBPort" prop="dbport">
                            <Input v-model="formValidate.dbport" placeholder="DataBase port..."></Input>
                        </FormItem>
                        <FormItem label="DBUserName" prop="dbusername">
                            <Input v-model="formValidate.dbusername" placeholder="DataBase userName..."></Input>
                        </FormItem>
                        <FormItem label="DBPassWord" prop="dbpasswd">
                            <Input v-model="formValidate.dbpasswd" placeholder="DataBase passWord..."></Input>
                        </FormItem>
                        <FormItem label="全局变量" prop="template">
                            <Input v-model="formValidate.template" type="textarea" :autosize="{minRows: 2,maxRows: 100}" placeholder="请以json格式保存设置的全局变量：{key:value}"></Input>
                        </FormItem>
                        <FormItem label="请求头管理" prop="headers">
                            <Input v-model="formValidate.headers" type="textarea" :autosize="{minRows: 2,maxRows: 100}" placeholder="请以json格式保存设置headers信息：{key:value}"></Input>
                        </FormItem>
                        <FormItem label="登录信息" prop="authInfo">
                            <Input v-model="formValidate.authInfo" type="textarea" :autosize="{minRows: 2,maxRows: 100}" placeholder="若执行用例前需通过登录获取用户信息，请以json格式保存登录用户信息，如{key:value}"></Input>
                        </FormItem>
                        <FormItem>
                            <Button type="primary" @click="handleSubmit('formValidate')">Submit</Button>
                            <Button type="ghost" @click="handleReset('formValidate')" style="margin-left: 8px">Reset</Button>
                        </FormItem>
                    </Form>
                </Card>
            </Col>
            <!--<Col span="6" class="padding-left-10">
                <div class="margin-top-10">
                    <Card>
                        <p slot="title">
                            <Icon type="navicon-round"></Icon>
                            修改记录
                        </p>
                    </Card>
                </div>
            </Col>-->
        </Row>
    </div>
</template>

<script>
import axios  from 'axios';
export default {
    name: 'environment-info',
    data () {
        return {
            formValidate: {
                    name: '',
                    url: '',
                    template: '',
                    dbname: '',
                    dbhostname:'',
                    dbport: '',
                    dbusername: '',
                    dbpasswd: '',
                    envId:'',
                    headers:'',
                    authInfo:'',
                },
            ruleValidate: {
                name: [
                        { required: true, message: 'The name cannot be empty', trigger: 'blur' }
                    ]
                }
        };
    },
    methods: {
        handleSubmit (name) {
            this.$refs[name].validate((valid) => {
                if (valid) {
                    this.formValidate.envId=this.$route.query.id
                    axios.post("/v1/env/editEnvironmentItem",this.formValidate).then((res)=>{
                        console.log(res)
                        if(res.data.success){
                            this.$Message.success("成功");
                            this.$router.push({path:"/cooperation/environment-configuration"});
                        }else{
                            this.$Message.error("失败")
                        }
                    }
                    );
                } else {
                    this.$Message.error('失败!');
                }
            })
        },
        handleReset (name) {
            this.$refs[name].resetFields();
        },
        getEnvironmentInfoById(){
            axios.get("/v1/env/getEnvironmentInfoById",{params:{envId:this.$route.query.id}}).then((res)=>{
                console.log(res);
                if(res.data.success){
                    const envInfo = res.data.message[0]
                    this.formValidate.name= envInfo["env_name"]
                    this.formValidate.url= envInfo["url"]
                    this.formValidate.template= envInfo["data_template"]
                    this.formValidate.dbname= envInfo["db_name"]
                    this.formValidate.dbhostname= envInfo["db_hostname"]
                    this.formValidate.dbport= envInfo["db_port"]
                    this.formValidate.dbusername= envInfo["db_username"]
                    this.formValidate.dbpasswd= envInfo["db_passwd"]
                    this.formValidate.envId= envInfo["id"]
                    this.formValidate.authInfo=envInfo["authInfo"]
                    this.formValidate.headers=envInfo["headers"]

                }else{
                    this.$Message.error("获取环境详情失败")
                }
            });
        }
    },
    created () {
        this.getEnvironmentInfoById();

    },
};
</script>
