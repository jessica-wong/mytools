# -*- coding: utf-8 -*-

from src.main.master.service.impl.TaskCenterServiceImpl import TaskCenterService


def crontabCaseInstanceJob():
    print(TaskCenterService().crontabTask())
