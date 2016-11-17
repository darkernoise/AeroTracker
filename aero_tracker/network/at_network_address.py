'''
Created on Aug 21, 2016

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

class AT_NetworkAddress(object):
    '''
    Base properties for a client or server address.
    '''

    display_name = ""
    address = ""
    port = 0
    
    @property
    def full_address(self):
        return self.address + ':' + str(self.port)

    def __init__(self, display_name:str, address:str, port:int):
        '''
        Constructor
        '''
        self.display_name = display_name
        self.address = address
        self.port = port
        return
    
    