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

class MacAddress(object):
    '''
    Helper Functions for Mac Address
    '''
    MAC_ADDRESS_SEP = ":"
    
    @staticmethod
    def format_mac_address(mac_address):
        prts = mac_address.split(MacAddress.MAC_ADDRESS_SEP)
        if (len(prts) == 1):
            macAddr = mac_address.upper()
            return MacAddress.mac_bytes_pad(macAddr[0:2]) + ":" + \
                MacAddress.mac_bytes_pad(macAddr[2:4]) + ":" + \
                MacAddress.mac_bytes_pad(macAddr[4:6]) + ":" + \
                MacAddress.mac_bytes_pad(macAddr[6:8]) + ":" + \
                MacAddress.mac_bytes_pad(macAddr[8:10]) + ":" + \
                MacAddress.mac_bytes_pad(macAddr[10:12])
        else:
            return mac_address
    
    @staticmethod
    def unformat_mac_address(macAddress):
        rval = ""
        prts = macAddress.split(MacAddress.MAC_ADDRESS_SEP)
        if (len(prts) == 1):
            return prts[0].upper()
        else:
            for prt in prts:
                rval += prt.upper()
            return rval
    
    @staticmethod    
    def mac_bytes_pad(macBytes):
        if (len(macBytes) == 2):
            return macBytes
        else:
            return "0" + macBytes

        