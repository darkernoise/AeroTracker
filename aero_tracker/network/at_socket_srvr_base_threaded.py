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

import socketserver
from aero_tracker.network.at_protocol import AT_Protocol

class AT_SocketServerBaseThreaded(socketserver.ThreadingTCPServer):
    
    '''
    classdocs
    '''
    
    @property
    def args(self):
        return self._args
    
    @property
    def params(self):
        return self._params
    
    @property
    def terminator(self):
        return self._terminator
    
    @property
    def allow_reuse_address(self):
        return True

    _args = None
    _params = None
    _log = None
    _terminator = AT_Protocol.DATA_TERMINATOR
    
    def __init__(self, *args, server_address, RequestHandlerClass, params, terminator=AT_Protocol.DATA_TERMINATOR):
        socketserver.ThreadingTCPServer.__init__(self, 
                                                 server_address, 
                                                 RequestHandlerClass)
         
        self._args = args
        self._params = params
        self._terminator = terminator
        return
        