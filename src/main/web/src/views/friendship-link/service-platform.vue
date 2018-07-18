<style>
    .demo-spin-icon-load{
        animation: ani-demo-spin 1s linear infinite;
    }
    @keyframes ani-demo-spin {
        from { transform: rotate(0deg);}
        50%  { transform: rotate(180deg);}
        to   { transform: rotate(360deg);}
    }
    .demo-spin-col{
        display: inline-block;
        width: 1700px;
        height: 850px;
        position: relative;
        border: 1px solid #eee;
    }
</style>
<template>
    <Row>
        <Col class="demo-spin-col" span="8">
            <Spin fix>
                <Icon type="load-c" size=20 class="demo-spin-icon-load"></Icon>
                <div>Loading</div>
            </Spin>
        </Col>
    </Row>
</template>

<script>
    import axios from 'axios';
    export default {
        data(){
            return{
            unionid:'',
            }
        },
        methods:{
            jumpToPage(){
                axios.get("/v1/user/getCurrentUser").then((res)=>{
                    console.log(res)
                    if(res.data.success){
                        this.$Message.success("跳转成功")
                        console.log(res.data.message[0])
                        this.unionid=res.data.message[0].unionid
                        window.location.href="http://192.168.50.157/#/login?unionid="+this.unionid
                    }else{
                        this.$Message.error("获取数据失败")
                    }
                })
            },
        },
        created () {
            this.jumpToPage()
        }
    }
</script>