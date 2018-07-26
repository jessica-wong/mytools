from apscheduler.schedulers.blocking import BlockingScheduler
from src.main.master.scheduler.jobManage import crontabCaseInstanceJob


def init_scheduler_jobs():
    print('This job is run every three minutes.')

if __name__=="__main__":
    print('scheduler server is starting')
    sched = BlockingScheduler()
    sched.add_job(crontabCaseInstanceJob, 'interval', seconds=10)
    sched.start()
    print('scheduler server is started')