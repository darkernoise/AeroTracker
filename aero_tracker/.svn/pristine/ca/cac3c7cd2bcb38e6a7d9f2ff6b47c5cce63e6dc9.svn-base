'''
Created on Aug 20, 2016

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

from aero_tracker.common.at_threaded_base import AT_ThreadedBase
from aero_tracker.log.at_logging import AT_Logging
from aero_tracker.server.directory.at_directory_mp_manager import AT_DirectoryMPManager
from aero_tracker.exception.at_exception import AT_Exception
import time

class AT_DirectoryInitializer(AT_ThreadedBase):
    '''
    The directory store cannot be updated until the server is started.  This thread
    is started before the manager server is started with the intention of waiting for
    the start, initializing startup values, and then exits.
    '''
    
    LOG_FILE = '/var/log/aerotracker/at_directory.log'
    _manager_address = ""
    _log = None
    _manager_port = 0
    _initialized = False
    
    @property
    def thread_name(self):
        #TODO
        return 'Directory Manager Init'
    
    def set_manager_address(self, manager_address):
        self.thread_lock.acquire(blocking=True)
        self._manager_address = manager_address
        self.thread_lock.release()
        
    def set_manager_port(self, manager_port):
        self.thread_lock.acquire(blocking=True)
        self._manager_port = manager_port
        self.thread_lock.release()
        
    def run_clycle(self):
        '''
        Executes within the while is_running loop.
        '''
        if (self._initialized):
            self._log.log(msg1='Already initialized', caller=self, msgty=AT_Logging.MSG_TYPE_ERROR)
            time.sleep(.5)
            return
        
        self.thread_lock.acquire(blocking=True)
        tries = 0
        mgr_connected = False
        dir_store = None
        s_addr_port = str(self._manager_address) + ':' + str(self._manager_port)
        AT_DirectoryMPManager.register_client_methods()
        time.sleep(1)
        while ((not mgr_connected) and (tries < 100)):
            try:
                if (self._manager_port > 0):
                    self._manager = AT_DirectoryMPManager(address=(self._manager_address, self._manager_port), \
                        authkey=bytearray(self._params.manager_auth_key,'ascii'))
                    self._log.log2(msg1='Attempting manager connection to at', msg2=s_addr_port, caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
                    self._manager.connect()
                    dir_store = self._manager.get_instance()
                    mgr_connected = True
            except Exception as ex:
                self._log.log2(msg1='Error opening manager port:', msg2=str(ex), caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
                tries += 1
                time.sleep(.5)
        if (not mgr_connected):
            self._log.log2(msg1='Critical error opening manager port:', msg2=str(ex), caller=self, msgty=AT_Logging.MSG_TYPE_ERROR)
            self.stop()
            raise AT_Exception(source=self, method='run_clycle', message='Critical error opening Manager port', details=str(self._manager_port))
        
        
        #Save the manager port number into the directory store
        dir_store.set_manager_port(self._manager_port)
        self._initialized = True
        self._log.log(msg1='Successfully set manager store initial values', caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
        self.thread_lock.release()
        self.stop()
        return

    def __init__(self, log, params):
        '''
        Constructor
        '''
        super().__init__(params=params,log_file=self.LOG_FILE)
        return
        