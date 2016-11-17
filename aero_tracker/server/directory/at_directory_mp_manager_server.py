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

import time
import socket
import multiprocessing as mp
from aero_tracker.exception.at_exception import AT_Exception
from aero_tracker.log.at_logging import AT_Logging
from aero_tracker.server.directory.at_directory_store import AT_DirectoryStore
from aero_tracker.server.directory.at_directory_mp_manager import AT_DirectoryMPManager
from aero_tracker.server.directory.at_directory_initializer import AT_DirectoryInitializer

class AT_DirectoryMPManagerServer(mp.Process):
    '''
    Multiprocessing Manager server Process.
    '''
    
    _params = None
    _directory_store = None #single instance of data for the directory server
    _manager = None
    _manager_server = None
    _manager_port = 0
    _log = None
#     _directory_initializer = None #process to set startup values in the directory store once started
    
    @property
    def manager_port(self):
        return self._manager_port
    
    def run(self):
#         super().run()
        self._log.log(msg1='Manager process started', caller=self, msgty=AT_Logging.MSG_TYPE_INFO)
        self._serve_queue_manager(self._params.server_name, self._manager_port)
        self._log.log(msg1='Manager process exiting', caller=self, msgty=AT_Logging.MSG_TYPE_INFO)
        time.sleep(1)
        return

    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__()
        self._params = params
        self._setup_directory_store()
        self._log = AT_Logging(self._params)
        self.daemon = True
#         self._directory_initializer = dir_initializer
        return
    
    def __del__(self):
        self.stop()
    
    def stop(self):
        if (self._manager_server != None):
            self._manager_server.stop()
        return
    
    def _setup_directory_store(self):
        self._directory_store = AT_DirectoryStore(self._log, self._params)
        AT_DirectoryMPManager.register(typeid='get_instance', callable=lambda:self._directory_store)
        self._manager_port = self._params.port
        return
    
    def _serve_queue_manager(self, client_address, port):
        tries = 0
        mgr_connected = False
        saddrstr = client_address + ':' + str(port)
        while ((not mgr_connected) and (tries < 10)):
            try:
                self._manager = AT_DirectoryMPManager(address=(client_address, port), \
                    authkey=bytearray(self._params.manager_auth_key,'ascii'))
                self._log.log(msg1='Getting manager server ready to start', caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
                self._manager_server = self._manager.get_server()
                mgr_connected = True
            except Exception as ex:
                self._log.log2(msg1='Error opening manager port:', msg2=str(ex), caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
                tries += 1

        if (not mgr_connected):
            self._log.log1(msg1='Critical error opening manager port.  Quitting.', caller=self, msgty=AT_Logging.MSG_TYPE_ERROR)
            self.stop()
            raise AT_Exception(source=self, method='_serve_queue_manager', message='Critical error opening Manager port', details=str(port))
        
        self._log.log3(msg1='Manger configured and about to start waiting for connections', \
            msg2='At:', msg3=saddrstr, caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
        self._manager_server.serve_forever()
        return
    