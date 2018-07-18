<style lang="less">
    @import '../../styles/common.less';
</style>
<template>
    <div>
        <Row class="margin-top-20">
            <Col span="8" class="padding-left-10">
                <Card style="width:320px" class="margin-top-20">
                    <div style="text-align:center" @click="jumpToInterfaceTest">
                        <Icon type="wrench"></Icon>
                        <h3>接口自动化测试</h3>
                        <a>点击访问</a>
                    </div>
                </Card>
            </Col>
            <Col span="8" class="padding-left-10">
                <Card style="width:320px" class="margin-top-20">
                    <div style="text-align:center">
                        <Icon type="wrench"></Icon>
                        <h3>UI自动化测试</h3>
                        <p>敬请期待</p>
                    </div>
                </Card>
            </Col>
        </Row>
        <Row class="margin-top-20">
            <Col span="8" class="padding-left-10">
                <Card style="width:320px" class="margin-top-20">
                    <div style="text-align:center" @click="jumpToPerformanceTest">
                        <Icon type="wrench"></Icon>
                        <h3>性能测试</h3>
                        <p>敬请期待</p>
                    </div>
                </Card>
            </Col>
            <Col span="8" class="padding-left-10">
                <Card style="width:320px" class="margin-top-20">
                    <div style="text-align:center" @click="jumpToCodeTest">
                        <Icon type="wrench"></Icon>
                        <h3>代码扫描</h3>
                        <p>敬请期待</p>
                    </div>
                </Card>
            </Col>
        </Row>

    </div>
</template>
<script>
    export default {
        methods:{
            jumpToInterfaceTest(){
                this.$router.push({
                    name:"interface-test",
                })
            },
            jumpToUITest(){
                this.$router.push({
                    name:"ui-test",
                })
            },
            jumpToPerformanceTest(){
                this.$router.push({
                    name:"performance-test",
                })
            },
            jumpToCodeTest(){
                this.$router.push({
                    name:"code-test",
                })
            },
        }
    }
</script>