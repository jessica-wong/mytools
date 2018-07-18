# -*- coding: utf-8 -*-

class Assert(object):

    def __init__(self):
        pass

    def assertTrue(self,actual):
        if actual == True:
            return True
        return False

    def assertFalse(self,actual):
        if actual == False:
            return True
        return False

    def isEqual(self,actual,expect):
        if actual == expect:
            return True
        return False

    def notEqual(self,actual,expect):
        if actual != expect:
            return True
        return False

    def isContain(self,actual,expect):
        if str(actual).find(expect) > 0:
            return True
        return False

    def notContain(self,actual,expect):
        if str(actual).find(expect) <= 0:
            return True
        return False

class AssertInstance(object):
    _INSTANCE = Assert()

    @staticmethod
    def get_instance():
        return AssertInstance._INSTANCE