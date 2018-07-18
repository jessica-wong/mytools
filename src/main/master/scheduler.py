# -*- coding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler
from src.main.master.service.impl.TaskCenterServiceImpl import TaskCenterService

def query_task_queue():
    print (TaskCenterService().sendTask().dict__)

sched = BlockingScheduler()
sched.add_job(query_task_queue,'interval',seconds=10)
sched.start()
