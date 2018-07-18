<style lang="less">
    @import './login.less';
</style>

<template>
    <div class="login">
        <div class="login-con">
            <Tabs type="card">
                <TabPane label="登录" icon="log-in">
                    <div class="form-con">
                        <Form ref="loginForm" :model="form" :rules="rules">
                            <FormItem prop="userName">
                                <Input v-model="form.userName" placeholder="请输入用户名">
                                    <span slot="prepend">
                                        <Icon :size="16" type="person"></Icon>
                                    </span>
                                </Input>
                            </FormItem>
                            <FormItem prop="passWord">
                                <Input type="password" v-model="form.passWord" placeholder="请输入密码">
                                    <span slot="prepend">
                                        <Icon :size="14" type="locked"></Icon>
                                    </span>
                                </Input>
                            </FormItem>
                            <FormItem>
                                <Button @click="handleSubmit" type="primary" long>登录</Button>
                            </FormItem>
                        </Form>
                        <p class="login-tip">记住密码,暂不支持修改</p>
                    </div>
                </TabPane>
                <TabPane label="注册" icon="ionic">
                    <div class="form-con">
                        <Form ref="registerForm" :model="registerForm" :rules="registerRules">
                            <FormItem prop="userName">
                                <Input v-model="registerForm.userName" placeholder="请输入用户名">
                                    <span slot="prepend">
                                        <Icon :size="16" type="person"></Icon>
                                    </span>
                                </Input>
                            </FormItem>
                            <FormItem prop="userPasswd">
                                <Input type="password" v-model="registerForm.userPasswd" placeholder="请输入密码">
                                    <span slot="prepend">
                                        <Icon :size="14" type="locked"></Icon>
                                    </span>
                                </Input>
                            </FormItem>
                            <FormItem>
                                <Button @click="handleRegister" type="primary" long>注册</Button>
                            </FormItem>
                        </Form>
                        <p class="login-tip">记住密码,暂不支持修改</p>
                    </div>
                </TabPane>
            </Tabs>
        </div>
    </div>
</template>

<script>
import Cookies from 'js-cookie';
import axios  from 'axios';
export default {
    data () {
        return {
            form: {
                userName: '',
                passWord: ''
            },
            registerForm:{
                userName: '',
                userPasswd: '',
                mobile:'',
                unionid:'',
                userIdDing:'',
                departmentId:'',
            },
            rules: {
                userName: [
                    { required: true, message: '账号不能为空', trigger: 'blur' }
                ],
                passWord: [
                    { required: true, message: '密码不能为空', trigger: 'blur' }
                ]
            },
            registerRules:{
                userName: [
                    { required: true, message: '账号不能为空', trigger: 'blur' }
                ],
                userPasswd: [
                    { required: true, message: '密码不能为空', trigger: 'blur' }
                ]
            }
        };
    },
    methods: {
        getUnionId(){
            axios.get("/v1/user/getUserByUnionid",{params:{unionid:this.$route.query.unionid}}
            ).then((res)=>{
                console.log(res)
                if(res.data.success && res.data.message.length){
//                    this.$Message.success("成功")
                    this.form.userName=res.data.message[0].username;
                    this.form.passWord=res.data.message[0].passwd;
                    this.handleSubmit()
                }else if(res.data.success && !res.data.message.length){
//                    this.$Message.error("当前用户不存在，正在为你创建用户")
                    this.getUserDingDingInfo().then(this.handleRegister())

                }
            });
        },
        getUserDingDingInfo(){
            return axios.get("/v1/user/getUserDingDingInfo",{params:{unionid:this.$route.query.unionid}}
            ).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.registerForm.userName=res.data.message.name;
                    this.registerForm.userPasswd="123456";
                    this.registerForm.mobile=res.data.message.mobile;
                    this.registerForm.userIdDing=res.data.message.userid;
                    this.registerForm.unionid=res.data.message.unionid;
                    this.registerForm.departmentId=res.data.message.department[0];
                }
            });
            //return undefined
        },
        handleSubmit(){
            axios.post("/v1/login/auth_login",this.form
            ).then((res)=>{
                console.log(res)
                if(res.data.success){
                    Cookies.set('user', this.form.userName);
                    if (this.form.userName === 'admin') {
                        Cookies.set('access', 0);
                    } else {
                        Cookies.set('access', 1);
                    }
                    this.$router.push({
                        name: 'home_index'
                    });
                }else{
                    this.$Message.error("失败")
                }
            });
        },
        handleRegister(){
//            this.registerForm=this.getUserDingDingInfo()
            axios.post("/v1/user/addUser",this.registerForm
            ).then((res)=>{
                console.log(res)
                if(res.data.success){
                    Cookies.set('user', this.registerForm.userName);
                    Cookies.set('access', 1);
                    this.$router.push({
                        name: 'home_index'
                    });
                }
//                else{
//                    this.$Message.error("失败")
//                }
            });
        }
    },
    created () {
        this.getUnionId()
    }
};
</script>

<style>

</style>
