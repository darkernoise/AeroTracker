'''
Created on Aug 24, 2016

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

from aero_tracker.network.at_protocol import AT_Protocol
from aero_tracker.network.at_pipe_pool import AT_PipePool
from aero_tracker.network.at_socket_srvr_base import AT_SocketServerBase  

class AT_DataProcSocketServer(AT_SocketServerBase):
    '''
    Forking TCP Socket Server for data processing nodes.  Each remove sensor 
    will first contact the directory server to see which of the data 
    processing servers covers which target.  Essentially, there will be
    an address and a port for each data target.
    '''
    
    _data_proc_mgr_address = ''
    _data_proc_mgr_port = 0
    _log_file = '/var/log/aerotracker/at_socket.log'
    _pipe_pool = AT_PipePool
    
    @property
    def data_proc_manager_address(self):
        return self._data_proc_mgr_address
    
    @data_proc_manager_address.setter
    def data_proc_manager_address(self, val):
        self._data_proc_mgr_address = val
        return
    
    @property
    def data_proc_manager_port(self):
        return self._data_proc_mgr_port
    
    @data_proc_manager_port.setter
    def data_proc_manager_port(self, val):
        self._data_proc_mgr_port = val
        return
    
    @property
    def log_file(self):
        return self._log_file
    
    @log_file.setter
    def log_file(self, val):
        self._log_file = val
        return
    
    @property
    def pipe_pool(self)->AT_PipePool:
        return self._pipe_pool
    
    @pipe_pool.setter
    def pipe_pool(self, val):
        self._pipe_pool = val
        return
    
    
    
        
        