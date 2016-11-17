'''
Created on May 30, 2016

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

from aero_tracker.network.mac_address import MacAddress


class TX_Item(object):
    '''
    Transmitting target vehicle definition.
    '''
    
    target_id = 0
    mac_address = ""
    uuid = ""
    major = 0
    minor = 0

    def __init__(self, mac_address, target_id, uuid, major, minor):
        '''
        Constructor
        '''
        self.mac_address = MacAddress.unformat_mac_address(mac_address)
        self.target_id = target_id
        self.uuid = uuid
        self.major = major
        self.minor = minor
                