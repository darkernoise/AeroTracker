'''
Created on Aug 16, 2016

@author: Joel Blackthorne

AeroTracker, Copyright (C) 2016 Joel Blackthorne
This file is part of AeroTracker.

AeroTracker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

AeroTracker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with AeroTracker.  If not, see <http://www.gnu.org/licenses/>.
'''
import os
import sys
import datetime
import time
import logging
import logging.handlers
import multiprocessing as mp
import traceback
from multiprocessing import util

class AT_Logging(object):
    '''
    Logging module
    '''
    DEFAULT_LOG_FILE = '/var/log/aerotracker/at.log'
    DEFAULT_LOG_DIR = '/var/log/aerotracker'
    MSG_TYPE_DEBUG = 8
    MSG_TYPE_INFO = 1
    MSG_TYPE_WARNING = 2
    MSG_TYPE_ERROR = 4
    MAX_LOG_FILE_BYTES = 1000000
    LOG_BACKUP_COUNT = 10
    LOG_ROLLOVER_SECS = 200
    LOG_DIR = 'log'
    
    _params = None
    _log = None
    _lock = None
    _log_file = ''
    
    @staticmethod
    def get_log_dir():
        rval = os.getcwd()
        if (rval.endswith('gui')):
            base_dir = rval[:-17]
            rval = os.path.normpath(base_dir + os.sep + AT_Logging.LOG_DIR + os.sep)
        else:
            rval = AT_Logging.DEFAULT_LOG_DIR
        return rval
    
    @staticmethod
    def get_log_file_full(log_file_name='at.log'):
        rval = os.path.normpath(AT_Logging.get_log_dir() + log_file_name)
        return rval
    
    def get_log_file(self):
        if (self._log_file == ''):
            return self.DEFAULT_LOG_FILE
        else:
            return self._log_file
    
    def log5(self, msg1, msg2, msg3, msg4, msg5, caller, msgty=1):
        self.log(msg1=msg1 + ' ' + msg2 + ' ' + msg3 + ' ' + msg4 + ' ' + msg5, caller=caller,msgty=msgty)
        return
    
    def log4(self, msg1, msg2, msg3, msg4, caller, msgty=1):
        self.log(msg1=msg1 + ' ' + msg2 + ' ' + msg3 + ' ' + msg4, caller=caller,msgty=msgty)
        return
    
    def log3(self, msg1, msg2, msg3, caller, msgty=1):
        self.log(msg1=msg1 + ' ' + msg2 + ' ' + msg3, caller=caller,msgty=msgty)
        return
    
    def log2(self, msg1, msg2, caller, msgty=1):
        self.log(msg1=msg1 + ' ' + msg2, caller=caller,msgty=msgty)
        return
    
    def log(self, msg1, caller, msgty=1):
        try:
            stime = datetime.datetime.now().strftime('%y-%m-%d %H %M %S')
            msg = stime + ' - ' + msg1
#             if (caller != None):
#                 mfrm = type(caller).__name__
#                 msg = '[' + mfrm + '] ' + msg
            self._lock.acquire()
            print(msg)
            if (msgty == self.MSG_TYPE_ERROR):
                pass
                self._log.error(msg)
            elif (msgty == self.MSG_TYPE_WARNING):
                self._log.warning(msg)
            elif (msgty == self.MSG_TYPE_DEBUG):
                self._log.debug(msg)
            else:
                self._log.info(msg)
            
            self._lock.release()
        except:
            pass
        return
    
    def print_traceback(self, ex, caller, msgty=4):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tbitms = traceback.extract_tb(tb=exc_traceback)
        lvl = 0
        for tbitm in tbitms:
            self.log2(msg1='Lvl: ' + str(lvl), msg2=str(tbitm), caller=caller, msgty=msgty)
            lvl += 1
        return

    def __init__(self, params, log_file=''):
        '''
        Constructor
        '''
        self._params = params
        try:
            self._log_file = log_file
            self._check_log_directories()
            self._cleanup_old_handlers()
            self._log = self._get_logger()
            logging.basicConfig(filename=self.get_log_file(),format="%(threadName)s:%(message)s")
            self._log.setLevel(logging.DEBUG)
            
            log_handler = logging.handlers.RotatingFileHandler(
                  self.get_log_file(), maxBytes=self.MAX_LOG_FILE_BYTES, backupCount=self.LOG_BACKUP_COUNT)
            #force log file rollover
            self._check_log_rollover(log_handler)
            self._log.addHandler(log_handler)
            time.sleep(1)
        except Exception as ex:
            print(ex)
            raise ex
        
        self._lock = mp.RLock()
        return
    
    def _check_log_directories(self):
        log_dir = os.path.dirname(self.get_log_file())
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return
    
    def _check_log_rollover(self, log_handler):
        mtime = os.path.getmtime(self.get_log_file())
        tst_change = time.time() - mtime
        if (tst_change > self.LOG_ROLLOVER_SECS):
            try:
                log_handler.doRollover()
            except Exception as ex:
                print(ex)
        return
    
    def __del__(self):
        
        return
    
    def _get_logger(self):
        logr = logging.getLogger(self.__class__.__name__)
        if (logr == None):
            if (os.sep == '/'):
#                 logr = mp.log_to_stderr()
                logr = mp.get_logger()
            else:
                logr = logging.getLogger()
        return logr
    
    def _cleanup_old_handlers(self):
        logr = logging.getLogger(self.__class__.__name__)
        if (logr != None):
#             logr.propagate = False
            for hndlr in logr.handlers:
                logr.removeHandler(hndlr)
#         logr.handlers = []
#         for hndlr in logging.Logger.manager.loggerDict.keys():
#             print(hndlr)
#             logging.getLogger(name)
        return
            
            
            