'''
Created on Aug 15, 2016

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

from aero_tracker.exception.at_exception import AT_Exception
from aero_tracker.network.at_protocol import AT_Protocol

class AT_Command(object):
    '''
    Base of all commands in AT_Protocol.
    '''
    _command = ""
    _data = []
    
    @property
    def command(self):
        return self._command
    
    @property
    def data(self):
        return self._data

    def __init__(self, packet_bytes, delimiter=AT_Protocol.COMMAND_DELIMITER):
        '''
        Constructor
        '''
        ex = AT_Exception(source=self, method='__init__', message='Invalid packet_bytes', details=packet_bytes)
        
        #validate raw packet Bytes
        if (packet_bytes == None):
            raise ex
        if (len(packet_bytes) == 0):
            raise ex
        if (packet_bytes[0] != delimiter):
            raise ex
        try:
            self._command = packet_bytes[1:3]
            dat = packet_bytes[4:]
            self._data = str(dat).split(sep=delimiter)
        except Exception as ex2:
            ex.details = str(ex2)
        return
            
            