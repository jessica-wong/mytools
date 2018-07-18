
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