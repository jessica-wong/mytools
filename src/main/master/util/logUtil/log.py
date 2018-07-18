# -*- coding: utf-8 -*-

import logging
import logging.handlers

logging.basicConfig()

class Log(object):
    def __init__(self, name, level=logging.INFO,
        fmt = '%(asctime)s - %(name)s - %(thread)d - %(levelname)s - %(funcName)s - %(message)s'):
        self.logger = logging.getLogger(name)
        self.level = level
        self.logger.setLevel(level)
        self.formatter = logging.Formatter(fmt)
        self.logger.propagate = False
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warn = self.logger.warn
        self.error = self.logger.error

    def write_to_file(self, file_name, maxBytes=10485760, backupCount=10):
        for handler in self.logger.handlers:
            if isinstance(handler, logging.handlers.RotatingFileHandler):
                if str(handler.baseFilename) == str(file_name):
                    return
        fh = logging.handlers.RotatingFileHandler(file_name, maxBytes=maxBytes,
            backupCount=backupCount)
        fh.setLevel(self.level)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        fh2 = logging.handlers.RotatingFileHandler(file_name + "_warn", maxBytes=maxBytes,
            backupCount=backupCount)
        fh2.setLevel(logging.WARNING)
        fh2.setFormatter(self.formatter)
        self.logger.addHandler(fh2)

    def write_to_console(self):
        ch = logging.StreamHandler()
        ch.setLevel(self.level)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)