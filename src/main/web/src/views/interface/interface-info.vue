<style lang="less">
    @import '../../styles/common.less';
</style>

<template>
    <div>
        <Row type="flex" class="height-100">
            <Col span="8">
                <i-button type="success" @click="addInterface" style="margin-top-10">新建接口</i-button>
                <i-button type="success">导入接口</i-button>
            </Col>
        </Row>
        <Row class="margin-top-20">
            <Col span="6">
                <Card>
                    <Tree :data="groupData" show-checkbox :render="renderContent" style="width:260px" @on-check-change="getInterfaceInfosByGroupId" ref="tree"></Tree>
                </Card>
            </Col>
            <Col span="18" class="padding-left-10">
                <Card>
                    <div >
                        <Table border :columns="lsitColumns" :data="list" ></Table>
                    </div>
                </Card>
            </Col>
        </Row>
    </div>
</template>

<script>
import axios  from 'axios';
export default {
    name: 'interface-info',
    data () {
        return {
            lsitColumns: [
                {
                    title: '接口Id',
                    key: 'id'
                },
                {
                    title: '接口名称',
                    key: 'name'
                },
                {
                     title: '接口地址',
                     key: 'url'
                },
                {
                    title: '编辑时间',
                    key: 'gmt_modify'
                },
                {
                    title: '编辑人',
                    key: 'create_username'
                },
                {
                    title: '操作',
                    key: 'action',
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
                                        let query = {projectId:this.$route.query.id,interfaceId: params.row.id}
                                        this.$router.push({
                                            name:'interface-edit',
                                            query:query
                                        })
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
                                        this.removeInterfaceData.interfaceId = params.row.id
                                        this.removeInterface()
                                    }
                                }
                            }, '删除')
                        ]);
                    }
                }
            ],
            list: [],
            groupData: [
                {
                    title: '分组名称',
                    expand: true,
                    checked: true,
                    render: (h, { root, node, data }) => {
                        return h('span', {
                            style: {
                                display: 'inline-block',
                                width: '100%'
                            }
                        }, [
                            h('span', [
                                h('Icon', {
                                    props: {
                                        type: 'ios-folder-outline'
                                    },
                                    style: {
                                        marginRight: '8px'
                                    }
                                }),
                                h('span', data.title)
                            ]),
                            h('span', {
                                style: {
                                    display: 'inline-block',
                                    float: 'right',
                                    marginRight: '32px'
                                }
                            }, [
                                h('Button', {
                                    props: Object.assign({}, this.buttonProps, {
                                        icon: 'ios-plus-empty',
                                        type: 'primary'
                                    }),
                                    style: {
                                        width: '40px'
                                    },
                                    on: {
                                        click: () => { this.addGroup(data) }
                                    }
                                })
                            ])
                        ]);
                    },
                    children: [
                    ],
                    groupId: 0
                }
            ],
            buttonProps: {
                type: 'ghost',
                size: 'small'
            },
            removeInterfaceData:{
                interfaceId:""
            },
            addGroupData:{
                parent_groupid:"",
                name:""
            }
        };
    },
    methods: {
        getData (group_id) {
            axios.get("/v1/interface/getInterfaceInfosByProject",{params:{projectId:this.$route.query.id,groupId: group_id,offset:0,limit:10}}
                ).then((res)=>{
                console.log(res)
                console.log(this.$route.query.id)
                if(res.data.success){
                    this.list = []
                    this.list = res.data.message;
                }else{
                    this.$Message.error("获取数据失败");
                }
            }
            )
        },
        getGroupData () {
            axios.get("/v1/group/getGroupInfoByProjectId",{params:{projectId:this.$route.query.id,type:0}}).then((res)=>{
                console.log(res);
                if(res.data.success){
                    const that =this;
                    res.data.message.forEach(function(item){
                        console.log(item);
                        that.groupData.push(item);
                    });
                }else{
                    this.$Message.error("获取数据失败")
                }
            })
        },
        addInterface(){
            this.$router.push({path:"/interface/interface-edit",query:{projectId:this.$route.query.id,interfaceId:""}})
        },
        addGroup(data){
            alert(JSON.stringify(data));
            this.$Modal.confirm({
                onOk: () => {
                       data["name"]=this.addGroupData.name;
                       data["userId"]=1;
                       data["type"]="0";
                       data["parentGroupId"]=data["groupId"];
                       data["isChild"]=1;
                       this.addGroupNet(data);
                    },
                    render: (h) => {
                    return h('div',[
                        h('Input', {
                            props: {
                                value: this.addGroupData.name,
                                autofocus: false,
                                placeholder: '分组名称'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.addGroupData.name = val;
                                }
                            }
                        })
                    ])
                }
            });
        },
        removeGroup(root,node,data){
            alert(JSON.stringify(root));
            alert(JSON.stringify(node));
            axios.post("/v1/group/deleteGroup",data).then((res)=>{
                console.log(data);
                console.log(res);
                if(res.data.success){
                    this.$Message.success("删除成功");
                    const parentKey = root.find(el => el === node).parent;
                    const parent = root.find(el => el.nodeKey === parentKey).node;
                    const index = parent.children.indexOf(data);
                    parent.children.splice(index, 1);
                    this.getGroupData();
                }else{
                    this.$Message.error("删除数据失败");
                }
            });
        },
        renderContent (h, { root, node, data }) {
            return h('span', {
                    style: {
                        display: 'inline-block',
                        width: '100%'
                    }
                }, [
                    h('span', [
                        h('Icon', {
                            props: {
                                type: 'ios-paper-outline'
                            },
                            style: {
                                marginRight: '8px'
                            }
                        }),
                        h('span', data.name)
                    ]),
                    h('span', {
                        style: {
                            display: 'inline-block',
                            float: 'right',
                            marginRight: '32px'
                        }
                    }, [
                        h('Button', {
                            props: Object.assign({}, this.buttonProps, {
                                icon: 'ios-plus-empty'
                            }),
                            style: {
                                marginRight: '8px'
                            },
                            on: {
                                click: () => { this.addGroup(data) }
                            }
                        }),
                        h('Button', {
                            props: Object.assign({}, this.buttonProps, {
                                icon: 'ios-minus-empty'
                            }),
                            on: {
                                click: () => { this.removeGroup(root, node, data) }
                            }
                        })
                    ])
                ]);
            },
        addGroupNet(data){
            alert(JSON.stringify(data));
            data["projectId"]=this.$route.query.id;
            axios.post("/v1/group/addChildGroup",data).then((res)=>{
                console.log(data);
                console.log(res)
                if(res.data.success){
                    this.$Message.success("添加成功");
                    const children = data.children || [];
                    alert(JSON.stringify(res.data.message));
                    children.push({
                       title: res.data.message.name,
                       expand: true,
                       groupId: res.data.message.id

                    });
                    this.$set(data, 'children', children);
                }else{
                    this.$Message.error("添加数据失败");
                }
            })
        },
        removeInterface(){
            axios.post("/v1/interface/deleteInterfaceItem",this.removeInterfaceData).then((res)=>{
                console.log(this.removeInterfaceData)
                console.log(res)
                if(res.data.success){
                    this.$Message.success("删除成功");
                }else{
                    this.$Message.error("删除数据失败")
                }
            })
        },
        getInterfaceInfosByGroupId(){
            const groupCheckedData=this.$refs.tree.getCheckedNodes()
            const testData= groupCheckedData[groupCheckedData.length-1]
            alert(JSON.stringify(testData))
            this.getData(testData["groupId"])
        }
    },
    created () {
        this.getGroupData();

    },
};
</script>
