import Main from '@/views/Main.vue';

// 不作为Main组件的子页面展示的页面单独写，如下
export const loginRouter = {
    path: '/login',
    name: 'login',
    meta: {
        title: 'Login - 登录'
    },
    component: resolve => { require(['@/views/login.vue'], resolve); }
};

export const page404 = {
    path: '/*',
    name: 'error-404',
    meta: {
        title: '404-页面不存在'
    },
    component: resolve => { require(['@/views/error-page/404.vue'], resolve); }
};

export const page403 = {
    path: '/403',
    meta: {
        title: '403-权限不足'
    },
    name: 'error-403',
    component: resolve => { require(['@//views/error-page/403.vue'], resolve); }
};

export const page500 = {
    path: '/500',
    meta: {
        title: '500-服务端错误'
    },
    name: 'error-500',
    component: resolve => { require(['@/views/error-page/500.vue'], resolve); }
};


export const locking = {
    path: '/locking',
    name: 'locking',
    component: resolve => { require(['@/views/main-components/lockscreen/components/locking-page.vue'], resolve); }
};

// 作为Main组件的子页面展示但是不在左侧菜单显示的路由写在otherRouter里
export const otherRouter = {
    path: '/',
    name: 'otherRouter',
    redirect: '/home',
    component: Main,
    children: [
        { path: 'home', title: {i18n: 'home'}, name: 'home_index', component: resolve => { require(['@/views/home/home.vue'], resolve); } },
        { path: 'ownspace', title: '个人中心', name: 'ownspace_index', component: resolve => { require(['@/views/own-space/own-space.vue'], resolve); } },
        { path: 'message', title: '消息中心', name: 'message_index', component: resolve => { require(['@/views/message/message.vue'], resolve); } },
        { path: 'project/project-info', title: '项目详情', name: 'project-info', component: resolve => { require(['@/views/project/project-info.vue'], resolve); } },
        { path: 'project/application-version-list', title: '项目应用', name: 'application-version-list', component: resolve => { require(['@/views/project/application-version-list.vue'], resolve); } },
        { path: 'project/version-config', title: '应用配置', name: 'version-config', component: resolve => { require(['@/views/project/version-config.vue'], resolve); } },
        { path: 'interface/interface-info', title: '接口信息', name: 'interface-info', component: resolve => { require(['@/views/interface/interface-info.vue'], resolve); } },
        { path: 'interface/interface-list', title: '接口列表', name: 'interface-list', component: resolve => { require(['@/views/interface/interface-list.vue'], resolve); } },
        { path: 'interface/interface-edit', title: '编辑接口', name: 'interface-edit', component: resolve => { require(['@/views/interface/interface-edit.vue'], resolve); } },
        { path: 'testcase/test-collection/case-list', title: '用例列表', name: 'case-list', component: resolve => { require(['@/views/testcase/test-collection/case-list.vue'], resolve); } },
        { path: 'testcase/test-collection/case-edit', title: '用例编辑', name: 'case-edit', component: resolve => { require(['@/views/testcase/test-collection/case-edit.vue'], resolve); } },
        { path: 'testcase/test-suite/suite-info', title: '套件详情', name: 'suite-info', component: resolve => { require(['@/views/testcase/test-suite/suite-info.vue'], resolve); } },
        { path: 'cooperation/environment-info', title: '环境详情', name: 'environment-info', component: resolve => { require(['@/views/cooperation/environment-info.vue'], resolve); } },
        { path: 'cooperation/cooperation-db-info', title: '数据库设置', name: 'cooperation-db-info', component: resolve => { require(['@/views/cooperation/cooperation-db-info.vue'], resolve); } },
        { path: 'cooperation/cooperation-dbdoc-list', title: '数据库文档详情', name: 'cooperation-dbdoc-list', component: resolve => { require(['@/views/cooperation/cooperation-dbdoc-list.vue'], resolve); } },
        { path: 'cooperation/cooperation-dbdoc-link', title: '数据库表联系', name: 'cooperation-dbdoc-link', component: resolve => { require(['@/views/cooperation/cooperation-dbdoc-link.vue'], resolve); } },
        { path: 'test-manage/interface-test', title: '接口测试', name: 'interface-test', component: resolve => { require(['@/views/test-manage/interface-test.vue'], resolve); } },
        { path: 'test-manage/interface-case-version', title: '用例版本', name: 'interface-case-version', component: resolve => { require(['@/views/test-manage/interface-case-version.vue'], resolve); } },
        { path: 'test-manage/interface-case-list', title: '用例列表', name: 'interface-case-list', component: resolve => { require(['@/views/test-manage/interface-case-list.vue'], resolve); } },

    ]
};

//// 作为Main组件的子页面展示并且在左侧菜单显示的路由写在appRouter里
export const appRouter = [
    {
        path: '/project',
        icon: 'ios-infinite',
        name: 'project',
        title: '项目管理',
        component: Main,
        children: [
            {
                path: 'project-center',
                title: '项目中心',
                name: 'project-center',
                icon: 'link',
                component: resolve => { require(['@/views/project/project-center.vue'], resolve); }
            },
            {
                path: 'command-centre',
                title: '指挥中心',
                name: 'command-centre',
                icon: 'android-send',
                component: resolve => { require(['@/views/project/command-centre.vue'], resolve); }
            }
        ]
    },
    {
        path: '/test-manage',
        icon: 'social-buffer',
        name: 'test-manage',
        title: '测试管理',
        component: Main,
        children: [
            {
                path: 'test-service',
                icon: 'compose',
                name: 'test-service',
                title: '测试服务',
                component: resolve => { require(['@/views/test-manage/test-service.vue'], resolve); }
            },
            {
                path: 'test-plan',
                icon: 'pound',
                name: 'test-plan',
                title: '测试计划',
                component: resolve => { require(['@/views/test-manage/test-plan.vue'], resolve); }
            },
            {
                path: 'test-measure',
                icon: 'thermometer',
                name: 'test-measure',
                title: '测试度量',
                component: resolve => { require(['@/views/test-manage/test-measure.vue'], resolve); }
            },
            {
                path: 'test-experiment',
                icon: 'erlenmeyer-flask',
                name: 'test-experiment',
                title: '实验中心',
                component: resolve => { require(['@/views/test-manage/test-experiment.vue'], resolve); }
            }
        ]
    },
    {
        path: '/cooperation',
        icon: 'arrow-move',
        name: 'cooperation',
        title: '协作管理',
        component: Main,
        children: [
            {
                path: 'environment-configuration',
                title: '环境配置',
                name: 'environment-configuration',
                icon: 'crop',
                component: resolve => { require(['@/views/cooperation/environment-configuration.vue'], resolve); }
            },
            {
                path: 'cooperation-db',
                title: '数据库管理',
                name: 'cooperation-db',
                icon: 'soup-can',
                component: resolve => { require(['@/views/cooperation/cooperation-db.vue'], resolve); }
            },
        ]
    },
    {
        path: '/task',
        icon: 'ios-grid-view',
        name: 'task',
        title: '任务管理',
        component: Main,
        children: [
            {
                path: 'task-timed',
                title: '定时任务',
                name: 'task-timed',
                icon: 'ionic',
                component: resolve => { require(['@/views/task/task-timed/task-timed.vue'], resolve); }
            },
            {
                path: 'task-trigger',
                title: '触发任务',
                name: 'task-trigger',
                icon: 'arrow-shrink',
                component: resolve => { require(['@/views/task/task-trigger/task-trigger.vue'], resolve); }
            }
        ]
    },
    {
        path: '/tools',
        icon: 'settings',
        name: 'tools',
        title: '工具管理',
        component: Main,
        children: [
            {
                path: 'tools-mock',
                title: 'mock工具',
                name: 'tools-mock',
                icon: 'help-buoy',
                component: resolve => { require(['@/views/tools/tools-mock.vue'], resolve); }
            },
            {
                path: 'tools-sign',
                title: 'sign工具',
                name: 'tools-sign',
                icon: 'asterisk',
                component: resolve => { require(['@/views/tools/tools-sign.vue'], resolve); }
            },
            {
                path: 'tools-MD5',
                title: 'MD5加密',
                name: 'tools-MD5',
                icon: 'shuffle',
                component: resolve => { require(['@/views/tools/tools-MD5.vue'], resolve); }
            },
        ]
    },
    {
        path: '/performance',
        icon: 'earth',
        name: 'performance',
        title: '监控中心',
        component: Main,
        children: [
            {
                path: 'performance-monitoring',
                title: '拨测监控',
                name: 'performance-monitoring',
                icon: 'ios-monitor',
                component: resolve => { require(['@/views/performance/performance-monitoring.vue'], resolve); }
            },
            {
                path: 'performance-source',
                title: '资源监控',
                name: 'performance-source',
                icon: 'ios-flask',
                component: resolve => { require(['@/views/performance/performance-source.vue'], resolve); }
            }
        ]
    },
    {
        path: '/analysis',
        icon: 'stats-bars',
        name: 'analysis',
        title: '统计分析',
        component: Main,
        children: [
            {
                path: 'analysis-bug',
                title: 'Bug分析',
                name: 'analysis-bug',
                icon: 'ios-pulse',
                component: resolve => { require(['@/views/analysis/analysis-bug.vue'], resolve); }
            },
            {
                path: 'analysis-case',
                title: 'Case分析',
                name: 'analysis-case',
                icon: 'clipboard',
                component: resolve => { require(['@/views/analysis/analysis-case.vue'], resolve); }
            },
            {
                path: 'analysis-coverage',
                title: '覆盖率分析',
                name: 'analysis-coverage',
                icon: 'ios-pie-outline',
                component: resolve => { require(['@/views/analysis/analysis-coverage.vue'], resolve); }
            }
        ]
    },
    {
        path: '/user',
        icon: 'android-contact',
        name: 'user',
        title: '用户管理',
        component: Main,
        children: [
            {
                path: 'user-list',
                title: '用户列表',
                name: 'user-list',
                icon: 'android-people',
                access:0,
                component: resolve => { require(['@/views/user/user-list.vue'], resolve); }
            }
        ]
    },
    {
        path: '/friendship-link',
        icon: "ios-infinite",
        name: 'friendship-link',
        title: '友情链接',
        component:Main,
        children: [
            {
                path: 'service-platform',
                title: '服务平台',
                name: 'service-platform',
                icon: 'aperture',
                component: resolve => { require(['@/views/friendship-link/service-platform.vue'], resolve); }
            },
            {
                path: 'data-platform',
                title: '数据平台',
                name: 'data-platform',
                icon: "stats-bars",
                component: resolve => { require(['@/views/friendship-link/data-platform.vue'], resolve); }
            }
        ]
    },
//    预留，别删
     {
         path: '/business',
         icon: 'android-contact',
         name: 'business',
         title: '事业线管理',
         component: Main,
         children: [
             {
                 path: 'business-product',
                 title: '产品管理',
                 name: 'business-product',
                 icon: 'android-people',
                 component: resolve => { require(['@/views/business/business-product.vue'], resolve); }
             },
//             {
//                 path: 'business-project',
//                 title: '项目管理',
//                 name: 'business-project',
//                 icon: 'android-people',
//                 component: resolve => { require(['@/views/business/business-project.vue'], resolve); }
//             }
         ]
     }
];

// 所有上面定义的路由都要写在下面的routers里
export const routers = [
    loginRouter,
    otherRouter,
    locking,
    ...appRouter,
    page500,
    page403,
    page404
];
