# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from src.main.master.common.constants import SystemConfig
from src.main.master.controller.UserController import UserHandler
from src.main.master.controller.ProjectController import ProjectHandler
from src.main.master.controller.EnvironmentController import EnvironmentHandler
from src.main.master.controller.GroupController import GroupHandler
from src.main.master.controller.InterfaceController import InterfaceHandler
from src.main.master.controller.CaseContentController import CaseContentHandler
from src.main.master.controller.TestCaseController import TestCaseHandler
from src.main.master.controller.AssertController import AssertHandler
from src.main.master.controller.TestSuiteController import TestSuiteHandler
from src.main.master.controller.TestCaseInstanceController import TestCaseInstanceHandler
from src.main.master.controller.DatabaseController import DatabaseHandler
from src.main.master.controller.ProductController import ProductHandler
from src.main.master.controller.LoginController import LoginHandler
from src.main.master.controller.ApplicationController import ApplicationHandler
from src.main.master.controller.WebApiController import WebApiHandler
from src.main.master.controller.CommomController import CommonHandler

def start_server():

    tornado.options.parse_command_line()
    settings = {
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "login_url": "/login"
    }
    
    app = tornado.web.Application(handlers=[
              #route
              (r"/v1/user/(.*)",UserHandler),
              (r"/v1/project/(.*)",ProjectHandler),
              (r"/v1/env/(.*)",EnvironmentHandler),
              (r"/v1/group/(.*)",GroupHandler),
              (r"/v1/interface/(.*)",InterfaceHandler),
              (r"/v1/case/(.*)", TestCaseHandler),
              (r"/v1/content/(.*)", CaseContentHandler),
              (r"/v1/assert/(.*)", AssertHandler),
              (r"/v1/suite/(.*)", TestSuiteHandler),
              (r"/v1/instance/(.*)", TestCaseInstanceHandler),
              (r"/v1/database/(.*)", DatabaseHandler),
              (r"/v1/product/(.*)", ProductHandler),
              (r"/v1/login/(.*)", LoginHandler),
              (r"/v1/application/(.*)",ApplicationHandler),
              (r"/v1/webapi/(.*)",WebApiHandler),
              (r"/v1/common/(.*)", CommonHandler),
              ],**settings)

    http_server = tornado.httpserver.HTTPServer(app,xheaders=True)
    http_server.listen(SystemConfig.httpPost)

    tornado.ioloop.IOLoop.instance().start()

if __name__=='__main__':
    start_server()
