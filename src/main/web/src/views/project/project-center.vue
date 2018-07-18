<style lang="less">
    @import '../../styles/common.less';
</style>
<template>
    <Tabs>
        <TabPane label="项目列表">
            <div>
                <Row type="flex" class="height-100">
                    <Col span="8">
                        <i-button type="success" @click="addProject" style="margin-top-10">新建项目</i-button>
                    </Col>
                </Row>
                <Row class="margin-top-10">
                    <Col>
                        <Card>
                            <div>
                                <can-edit-table
                                            v-model="list"
                                            @on-cell-change="handleCellChange"
                                            :editIncell="true"
                                            :columns-list="lsitColumns"
                                 ></can-edit-table>
                            </div>
                        </Card>
                    </Col>
                </Row>
            </div>
        </TabPane>
        <TabPane label="里程碑">
            <Timeline pending>
                <TimelineItem color="red">仅做展示，更多内容敬请期待</TimelineItem>
                <TimelineItem>2018.6.20 发布3.0版本</TimelineItem>
                <TimelineItem color="green">紧急发布</TimelineItem>
                <TimelineItem>2018.6.18 发布2.0版本</TimelineItem>
                <TimelineItem color="red">严重故障</TimelineItem>
                <TimelineItem>2018.6.18 发布1.0版本</TimelineItem>
                <TimelineItem><a href="#">查看更多</a></TimelineItem>
            </Timeline>
        </TabPane>
    </Tabs>
</template>
<script>
import canEditTable from './canEditTable.vue';
import axios  from 'axios';
export default {
    name: 'interface-manage',
    components: {
        canEditTable
    },
    data () {
        return {
            lsitColumns: [
//                    {
//                        title: '项目ID',
//                        key: 'id'
//                    },
                    {
                        title: '项目名称',
                        key: 'name',
                        editable: true,
                    },
                    {
                        title: '项目描述',
                        key: 'project_describe',
                        editable: true
                    },
                    {
                        title: '发布时间',
                        key: 'release_time'
                    },
                    {
                        title: '版本信息',
                        key: 'version'
                    },
                    {
                        title: '创建人',
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
                                            let query = { id: params.row.id };
                                            this.$router.push({
                                                name: 'project-info',
                                                query: query
                                            });
                                        }
                                    }
                                }, '查看'),
                                h('Button', {
                                    props: {
                                        type: 'error',
                                        size: 'small'
                                    },
                                    on: {
                                        click: () => {
                                            this.removeProjectData.projectId = params.row.id
                                            this.removeProject()
                                        }
                                    }
                                }, '删除')
                            ]);
                        }
                    }
            ],
            list:[],
            addProjectData:{
                    name:"",
                    userName:"",
                    userId:1,
                    version:"",
                    project_describe:""
            },
            removeProjectData:{
                projectId:"",
            },
            editProjectData:{
                projectId:"",
                name:"",
                project_describe:"",
                release_time:""
            },
        };
    },
    methods: {
//        onRowClick(rowData,index){
//                console.log(rowData)
//                this.$router.push({path:"/interface/interface-info",query:{projectId:rowData.id}})
//        },
        getData () {
            axios.get("/v1/project/getProjectList").then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.list = res.data.message;
                }else{
                    this.$Message.error("获取数据失败")
                }
            }
            )
        },
        handleCellChange (val, index, key) {
            this.editProjectData.projectId = val[index]["id"]
            this.editProjectData.name = val[index]["name"]
            this.editProjectData.project_describe = val[index]["project_describe"]
            axios.post("/v1/project/editProject",this.editProjectData).then((res)=>{
            // console.log(val,index,key)
            if(res.data.success){
                  this.$Message.success("成功");
                  this.getData();

            }else{
                  this.$Message.error("失败")
            }
        }
        )
            this.$Message.success('修改了第 ' + (index + 1) + ' 行列名为 ' + key + ' 的数据');
        },
        removeProject() {
                axios.post("/v1/project/deleteProject",
                this.removeProjectData).then((res)=>{
                //console.log(res)
                if(res.data.success){
                    this.$Message.success("成功");
                    this.getData();

                }else{
                    this.$Message.error("失败")
                }
            }
            )
            this.removeProjectData = {
                projectId:"",
            };
        },
        addProject(){
            this.$Modal.confirm({
                onOk: () => {
                       this.addProjectNet();
                    },
                    render: (h) => {
                    return h('div',[
                        h('Input', {
                            props: {
                                value: this.addProjectData.name,
                                autofocus: true,
                                placeholder: '项目名称'
                            },
                            on: {
                                input: (val) => {
                                    this.addProjectData.name = val;
                                }
                            }
                        }),
                        h('Input', {
                            props: {
                                value: this.addProjectData.version,
                                autofocus: false,
                                placeholder: '项目版本'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.addProjectData.version = val;
                                }
                            }
                        }),
                        h('Input', {
                            props: {
                                value: this.addProjectData.project_describe,
                                autofocus: false,
                                placeholder: '项目描述'
                            },
                            style: {
                                marginTop: '8px'
                            },
                            on: {
                                input: (val) => {
                                    this.addProjectData.project_describe = val;
                                }
                            }
                        })
                    ])
                }
            })
        },
        addProjectNet(){
            axios.post("/v1/project/addProject",
            this.addProjectData
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
            this.addProjectData = {
                name:"",
                userName:"",
                userId:1,
                version:"",
                project_describe:""

            };
        }
    },
    created () {
        this.getData();
    }
};
</script>
