from jinja2 import Template

class CommonTool():

    def __init__(self):
        pass

    def is_none_str(self, arg):
        if arg is None or arg.strip() == "":
            return True
        else:
            return False

    def is_zero(self, arg):
        if arg == 0:
            return True
        else:
            return False

    def is_none_list(self, arg):
        if arg is None or arg == []:
            return True
        else:
            return False


    # 渲染用户返回参数的方法
    #参数:template 为用户的待渲染模板，目前只支持字符串类型，举例如下：
    # 1. 渲染方法返回值：约定返回替换值为RESULT 使用{{RESULT}}
    # 2. 渲染方法返回状态：约定返回替换状态为STATUS 使用{{STATUS}}
    def render(self,template,data,status):
        template = Template(template)
        return template.render(RESULT=data,STATUS=status)

