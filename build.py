# -*- coding: utf-8 -*-

import os
import platform

#将所有src中py文件加入环境变量中
def setSystemPath():
    return os.system("python3 setup.py install")

#清理产生的invaild文件
def removeInvalidFiles():
    sysstr = platform.system()
    if(sysstr =="Windows"):
        print ("Call Windows tasks")
        return os.system("""rmdir /S /Q src.egg-info && rmdir /S /Q build && rmdir /S /Q dist""")
    elif(sysstr == "Linux"):
        print ("Call Linux tasks")
        return os.system("""rm -rf src.egg-info && rm -rf build && rm -rf dist""")
    else:
        print ("Other System tasks")
        return os.system("""rm -rf src.egg-info && rm -rf build && rm -rf dist""")

if __name__=="__main__":
    result = setSystemPath()
    if int(result) ==0:
        result = removeInvalidFiles()
        if int(result) == 0:
            print ("init success")
        else:
            print ("removeInvalidFiles run Fail:{0}".format(result))
    else:
        print ("setSystemPath run Fail:{0}".format(result))


