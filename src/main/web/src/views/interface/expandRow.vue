<style lang="less">
    @import './advanced-router.less';
</style>

<template>
    <div>
        <Card>
            <!--<Row>
                <Col span="8">
                    <span class="expand-key">请求方式：</span>
                    <span class="expand-value">{{ row.Method }}</span>
                </Col>
            </Row>-->
                <Row class="advanced-router">
                    <Col span="8">
                        <span class="expand-key">请求参数：</span>
                    </Col>
                    <Col span="8">
                        <pre class="expand-value">{{row.Schema_request | jsonFormat}}</pre>
                    </Col>
                </Row>
                <Row>
                    <Col span="8">
                        <span class="expand-key">返回参数：</span>
                    </Col>
                    <Col span="8">
                        <pre class="expand-value" >{{row.Schema_response | jsonFormat}}</pre>
                        <!--<i-input v-model="formattedJSON" :readonly="true" type="textarea" :autosize="true" placeholder="Enter something..."></i-input>-->
                    </Col>
                </Row>
        </Card>
    </div>
</template>
<script>
import Vue from 'vue'
import jsBeautify from 'js-beautify/js/lib/beautify'
    export default {
        props: {
            row: Object
        },
        filters:{
            jsonFormat(value){
                return jsBeautify.js_beautify(value,{indent_size:2})
            }
        }
    };
</script>