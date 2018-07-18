# -*- coding: utf-8 -*-
import threading


class Lock(object):

    def __init__(self):
        self._invoke_task_lock = threading.Condition()

    def getLock(self):
        print ("get Lock")
        self._invoke_task_lock.acquire()

    def unLock(self):
        print ("release Lock")
        self._invoke_task_lock.release()