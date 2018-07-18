
export const editInlineColumns = [
    {
        title: '序号',
        type: 'index',
        width: 80,
        align: 'center'
    },
    {
        title: '项目名称',
        align: 'center',
        key: 'name',
        width: 90,
        editable: true
    },
    {
        title: '性别',
        align: 'center',
        key: 'sex'
    },
    {
        title: '岗位',
        align: 'center',
        key: 'work',
        width: 150,
        editable: true
    },
    {
        title: '操作',
        align: 'center',
        width: 190,
        key: 'handle',
        handle: ['edit', 'delete']
    }
];

export const editInlineData = [
    {
        name: 'Aresn',
        sex: '男',
        work: '前端开发'
    },
    {
        name: 'Lison',
        sex: '男',
        work: '前端开发'
    },
    {
        name: 'lisa',
        sex: '女',
        work: '程序员鼓励师'
    }
];


//export const showCurrentColumns = [
//    {
//        title: '序号',
//        type: 'index',
//        width: 80,
//        align: 'center'
//    },
//    {
//        title: '姓名',
//        align: 'center',
//        key: 'name',
//        width: 300,
//        editable: true
//    },
//    {
//        title: '性别',
//        align: 'center',
//        key: 'sex'
//    },
//    {
//        title: '岗位',
//        align: 'center',
//        width: 300,
//        key: 'work',
//        editable: true
//    }
//];

const tableData = {
    editInlineColumns: editInlineColumns,
    editInlineData: editInlineData,
//    showCurrentColumns: showCurrentColumns
};

export default tableData;
