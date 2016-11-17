'''
Created on Aug 27, 2016

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

from aero_tracker.common.at_process_base import AT_ProcessBase
# from aero_tracker.trilateration.time_slice_queue import TimeSliceQueue
# from aero_tracker.trilateration.at_time_slice_queue import AT_TimeSliceQueue
from aero_tracker.server.data_proc.at_data_proc_worker_mp_manager import AT_DataProcWorkerMPManager
from aero_tracker.log.at_logging import AT_Logging
from aero_tracker.exception.at_exception import AT_Exception
from aero_tracker.network.at_pipe_pool import AT_PipePool

class AT_DataProcMPManagerServer(AT_ProcessBase):
    '''
    Process to host the local data processing worker shared memory manager.  The most
    critical thing this manager hosts is the AT_TimeSliceQueue instance.
    '''
    LOCAL_ADDRESS = '127.0.0.1'
    
    _manager_port = 0
#     _time_slice_queue = None
    _params = None
    _pipe_pool = AT_PipePool
    
    @property
    def manager_address(self):
        return self.LOCAL_ADDRESS
    
    @property
    def manager_port(self):
        return self._manager_port
    
    @property
    def process_name(self):
        rval = 'Data Proc Worker MP Manager Server'
        try:
            if (self.pid != None):
                rval += (' ' + str(self.pid))
        except:
            pass
        return rval
    
    def run_clycle(self):
        '''
        Executes within the while is_running loop.
        '''
        self._serve_queue_manager(client_address=self.manager_address, port=self._manager_port)
        return
        
    
    def __init__(self, params, pipe_pool):
        '''
        Constructor
        '''
        super().__init__(params)
        self._params = params
        self._pipe_pool = pipe_pool
        self._manager_port = self._params.port + 1
#         self._setup_time_slice_queue()
        self._setup_pipe_pool_info()
        return

    
    def stop(self):
        if (self._manager_server != None):
            self._manager_server.stop()
        super().stop()
        return
    
    def _setup_pipe_pool_info(self):
        AT_DataProcWorkerMPManager.register(typeid='get_pipe_pool', callable=lambda:self._pipe_pool)
        return
        
    
    def _serve_queue_manager(self, client_address, port):
        tries = 0
        mgr_connected = False
        saddrstr = client_address + ':' + str(port)
        while ((not mgr_connected) and (tries < 20)):
            try:
                self._manager = AT_DataProcWorkerMPManager(address=(client_address, port), \
                    authkey=bytearray(self.params.manager_auth_key,'ascii'))
                self._log.log(msg1='Getting manager server ready to start', caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
                self._manager_server = self._manager.get_server()
                self._manager_port = port
                mgr_connected = True
            except Exception as ex:
#                 self._log.log2(msg1='Error opening manager port:', msg2=str(ex), caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
                tries += 1
                port += 1

        if (not mgr_connected):
            self._log.log2(msg1='Critical error opening manager port:', msg2=str(ex), caller=self, msgty=AT_Logging.MSG_TYPE_ERROR)
            self.stop()
            raise AT_Exception(source=self, method='_serve_queue_manager', message='Critical error opening Manager port', details=str(port))
        
        self._log.log3(msg1=self.process_name + ' configured and about to start waiting for connections', \
            msg2='At:', msg3=saddrstr, caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
        self._manager_server.serve_forever()
        return

    
        