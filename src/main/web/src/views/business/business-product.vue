<style lang="less">
    @import '../../styles/common.less';
    @import './components/table.less';
</style>

<template>
    <div>
        <Row type="flex" class="height-100">
            <Col span="8">
                <i-button type="success" @click="addProduct" style="margin-top-10">新建产品</i-button>
            </Col>
        </Row>
        <Row class="margin-top-10">
            <Col>
                <!-- <Card> -->
                    <div class="edittable-table-height-con">
                        <Table border :columns="listColumns" :data="list"></Table>
                    </div>
                <!-- </Card> -->
            </Col>
        </Row>
    </div>
</template>

<script>
import axios  from 'axios';
export default {
    name: 'business-product',
    data () {
        return {
            listColumns: [

                    {
                        title: '事业部',
                        key: 'department_id'
                    },
                    {
                        title: '应用',
                        key: 'name'
                    },
                    {
                        title: '描述',
                        key: 'application_describe'
                    },
                    {
                        title: '操作',
                        key: 'id',
                        width: 150,
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
                                            this.getProductInfoByIdNet(params.row.id)
                                        }
                                    }
                                }, '编辑'),
                                h('Button', {
                                    props: {
                                        type: 'error',
                                        size: 'small'
                                    },
                                    on: {
                                        click: () => {
                                            this.deleteProductNet(params.row.id)
                                        }
                                    }
                                }, '删除')
                            ]);
                        }
                    }
            ],
            list:[],
            applicationDataModel:{
                    id: 0,
                    departmentId: 0,
                    applicationName: "",
                    applicationDescribe:"",
            },
        };
    },
    methods: {
        // onRowClick(rowData,index){
        //         console.log(rowData)
        //         this.$router.push({path:"/interface/interface-info",query:{projectId:rowData.id}})
        // },
        initapplicationDataModel() {
            this.applicationDataModel = {
                    id: 0,
                    departmentId: 0,
                    applicationName: "",

            };
        },
        getData () {
                axios.get("/v1/application/getApplicationList").then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.list = res.data.message;
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        addProduct(){
            this.initapplicationDataModel()
            this.$Modal.confirm({
                onOk: () => {
                       this.addProductNet();
                    },
                    render: (h) => {
                    return h('div',[
                        h('Select', {
                            props: {
                                value:'TBU' ,
                                placeholder: '请选择事业部'
                            },
                            on: {
                                select: (val) => {
                                    console.log(val);
                                    this.applicationDataModel.departmentId = val;
                                }
                            }
                            },[
                            h('Option', {props: {value: 'TBU', key:1}}),
                            h('Option', {props: {value: 'IBU', key:2}}),
                            h('Option', {props: {value: 'NBU', key:3}}),
                        ]),
                        h('Input', {
                            props: {
                                value: this.applicationDataModel.applicationName,
                                autofocus: false,
                                placeholder: '应用名'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.applicationDataModel.applicationName = val;
                                }
                            }
                        }),
                        h('Input', {
                            props: {
                                value: this.applicationDataModel.applicationDescribe,
                                autofocus: false,
                                placeholder: '应用描述'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.applicationDataModel.applicationDescribe = val;
                                }
                            }
                        }),
                    ])
                }
            })
        },
        addProductNet(){
            axios.post("/v1/application/addApplication",
            this.applicationDataModel
            ).then((res)=>{
                //console.log(res)
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getData();

                }else{
                    this.$Message.error("失败")
                }
            }
            )
            this.initapplicationDataModel()
        },
        deleteProductNet(index){
            axios.post("/v1/application/deleteApplication",
            {"id": index}
            ).then((res)=>{
                //console.log(res)
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getData();
                    // this.list.splice(index,1);

                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        editProductNet(index){
            axios.post("/v1/application/editApplication",
            this.applicationDataModel
            ).then((res)=>{
                //console.log(res)
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getData();
                    // this.list.splice(index,1);

                }else{
                    this.$Message.error("失败")
                }
            }
            )
            this.initapplicationDataModel()
        },
        getProductInfoByIdNet(index){
            axios.get("/v1/application/getApplicationById",
            {"params":{"id": index}}
            ).then((res)=>{
                //console.log(res)
                if(res.data.success){
                    this.$Message.success("成功");
                    this.applicationDataModel.id=res.data.message[0].id
                    this.applicationDataModel.applicationDescribe=res.data.message[0].application_describe
                    this.applicationDataModel.departmentId=res.data.message[0].departmentId
                    this.applicationDataModel.applicationName=res.data.message[0].name
                    this.editProduct()
                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        editProduct(){
            this.$Modal.confirm({
                onOk: () => {
                       console.log(this.applicationDataModel)
                       this.editProductNet();
                    },
                    render: (h) => {
                    console.log(this.applicationDataModel)
                    return h('div',[
                        h('Select', {
                            props: {
                                value: 'NBU', 
                                placeholder: '请选择事业部'
                            },
                            on: {
                                change: (val) => {
                                    console.log(val)
                                    this.applicationDataModel.departmentId = 2
                                }
                            }
                            },[
                            h('Option', {props: {value: 'IBU', key:1}}),
                            h('Option', {props: {value: 'TBU', key:2}}),
                            h('Option', {props: {value: 'NBU', key:3}}),
                        ]),
                        h('Input', {
                            props: {
                                value: this.applicationDataModel.applicationName,
                                autofocus: false,
                                placeholder: '应用名'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.applicationDataModel.applicationName = val;
                                }
                            }
                        }),
                        h('Input', {
                            props: {
                                value: this.applicationDataModel.applicationDescribe,
                                autofocus: false,
                                placeholder: '应用描述'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.applicationDataModel.applicationDescribe = val;
                                }
                            }
                        }),
                    ])
                }
            })
        },
    },
    
    created () {
        this.getData();
    }
};
</script>
