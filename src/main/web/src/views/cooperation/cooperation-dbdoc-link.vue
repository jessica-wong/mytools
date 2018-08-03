<style lang="less">
@import "../../styles/common.less";
</style>

<template>
    <div> 
        <Row type="flex" class="height-100">
            <Col span="24">
                <div class="container" ref='container'></div>
            </Col>
        </Row>
    </div>
</template>

<script>
import axios from "axios";
export default {
    name: "cooperation-dbdoc-link",
    data() {
        return {
            typeId: 0,
            type: 0,
            list: [],
        }
    },
    methods: {
        getData() {
            this.getId()
        },
        getId() {
            this.type = this.$route.query.type
            this.typeId = this.$route.query.id
        },
        getViewLinksNet() {
            return axios.get("/v1/database/getViewLinks",
                {"params":{"id": this.typeId, "type":this.type}}
            );
            
        },
        async getLinkGraph() {
            let list = await this.getViewLinksNet();
            // let list = this.getViewLinksNet();
            let src = list.data.message
            let src_data = src["data"]
            let type_name = src["type_name"]

            let tableInfoBK = [
                '{title|{b}}{abg|}',
                '{hr|}',
            ]

            let datus = []

            let richStyle = {
                title: {
                    color: '#eee',
                    align: 'center',
                    
                },
                abg: {
                    backgroundColor: '#333',
                    width: '100%',
                    align: 'right',
                    height: 25,
                    borderRadius: [4, 4, 0, 0]
                },
                hr: {
                    borderColor: '#777',
                    width: '100%',
                    borderWidth: 0.5,
                    height: 0
                },
                value0: {
                    width: 'auto',
                    height:20,
                    padding: [0, 20, 3, 5],
                    align: 'left',
                    color: 'rgb(194, 53, 49)',
                },
                value1: {
                    width: 'auto',
                    height:20,
                    padding: [0, 20, 3, 5],
                    align: 'left',
                    color: 'rgb(202, 134, 34)',
                },
                value2: {
                    width: 'auto',
                    height:20,
                    padding: [0, 20, 3, 5],
                    align: 'left',
                    color: 'rgb(91, 130, 105)',
                },
            };

            for(var i=0; i<src_data.length; i++) {
                let node = {}
                let info = src_data[i]['info']
                let t_name = src_data[i]['t_name']
                let db_name = src_data[i]['db_name']
                let line = src_data[i]['link_type']
                let bk = tableInfoBK.concat()
                for(var j=0; j<info.length; j++) {
                    let item = ``
                    if(line == 0){
                        item = `  {value0|${info[j]}}`
                    } else if(line == 1){
                        item = `  {value1|${info[j]}}`
                    } else if(line == 2){
                        item = `  {value2|${info[j]}}`
                    }
                    
                    bk.push(item)
                }

                let tableInfoNormal = {
                    formatter: bk.join('\n'),
                    backgroundColor: '#eee',
                    borderColor: '#777',
                    borderWidth: 1,
                    borderRadius: 4,
                    textBorderColor: 'transparent',
                    textBorderWidth: 0,
                    rich: richStyle
                }

                node["name"] = t_name
                node["value"] = db_name
                node["label"] = {"normal":tableInfoNormal} 
                datus.push(node)
            
            }


            let myChart = echarts.init(this.$refs.container);

            let linkStyle = {
                normal: {
                    show: true
                }
            };
            let option = {
                title: {
                    text: type_name
                },
                tooltip: {},
                animationDurationUpdate: 1500,
                animationEasingUpdate: 'quinticInOut',
                
                series : [
                    {
                        // id: 'a',
                        type: 'graph',
                        symbol: 'rect',
                        symbolSize: [160,60],
                        color: 'rgba(255, 255, 255, 0)',
                        layout: 'circular',
                        focusNodeAdjacency: true,
                        roam: true,
                        emphasis: {
                            lineStyle: {
                                width: 10
                            }
                        },
                        label: {
                            normal: {
                                show: true
                            }
                        },
                        // edgeSymbol: ['none', 'arrow'],
                        edgeSymbol: ['none', 'none'],
                        edgeSymbolSize: [10,20],
                        tooltip : {
                            trigger: 'item',
                            formatter: "{b} -- {c} "
                            // formatter: "{c} "
                        },
                        data: datus,
                        links: src["links"],
                        lineStyle: {
                            normal: {
                                opacity: 0.9,
                                width: 2,
                                curveness: 0.08
                            }
                        },
                    }
                ]
            }
            // myChart.setOption(option)
            // // myChart.on('click', function (params) {
            // //     // 控制台打印数据的名称
            // //     console.log(params);
            // // });
            // myChart.on('mousedown', function (params) {
            //     // console.log(params);
            //     console.log(params.event.offsetX);
            //     console.log(params.event.offsetY);
            // })

            // myChart.on('mouseup', function (params) {
            //     // console.log(params);
            //     // console.log(params.event.offsetX);
            //     // console.log(params.event.offsetY);
            //     params.event.offsetX += 10
            //     params.event.offsetY += 10
            // })
        }
    },
    // created() {
    //     this.getData()
    // },
    // watch: {
    //     '$route': function (route) {
    //         let query = route.query
    //         this.page = query.page
    //         // this.getData()
    //         // this.getLinkGraph()
    //     },
    // },

    // async mounted() {
    //     this.getData()
    //     this.getLinkGraph()
    // },
    beforeRouteEnter(to, from, next) {
        next(vm => {
            vm.getData()
            vm.getLinkGraph()
        })
    },

}
</script>

<style scoped>
.container {
    width: 1600px;
    height: 850px;
}

</style>