'''
Created on Sep 18, 2016

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

# from aero_tracker.network.at_socket_srvr_base import AT_SocketServerBase
from aero_tracker.network.at_socket_srvr_base_threaded import AT_SocketServerBaseThreaded

class AT_ResultListenerSocketServer(AT_SocketServerBaseThreaded):
    '''
    Result Listeners open listening ports so that data processing servers
    can direct connect and stream results.
    '''
    
    _listener_address = ""
    _listener_port = 0
    _log_file = '/var/log/aerotracker/at_socket.log'
    _rslt_queue = None #Multithreading.Queue
    
    @property
    def listener_address(self):
        return self._listener_address
    
    def set_listener_address(self, val):
        self._listener_address = val
        return
    
    @property
    def listner_port(self):
        return self._listener_port
    
    def set_listener_port(self, val):
        self._listener_port = val
        return
    
    @property
    def result_queue(self):
        return self._rslt_queue
    
    def set_result_queue(self, val):
        self._rslt_queue = val
        return
    
    @property
    def log_file(self):
        return self._log_file
    
    @log_file.setter
    def log_file(self, val):
        self._log_file = val
        return
    
        