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

from aero_tracker.target.tx_item import TX_Item

class TX_Item_List(object):
    '''
    List of TX Items to track.
    '''
    STATIC_TRANSMITTERS_LIST = "/etc/popt/aero_tracker/at_static_transmitters.conf"
    _list = None
    
    def add(self, mac_address, target_id, uuid, major, minor):
        if (self._list == None):
            self._list = []
        self._list.append(TX_Item(mac_address=mac_address, target_id=target_id, uuid=uuid, major=major, minor=minor))
        return self._list
    
    def inList(self, mac_address, uuid, major, minor):
        if (self._list == None):
            return True
        else:
            for txItm in self._list:
                if (txItm.mac_address == mac_address):
                    return True
        return False

    def __init__(self):
        '''
        Constructor
        '''
        self._load_static_transmitters()
        return
        
        
    def _load_static_transmitters(self):
        try:
            fl = open(self.STATIC_TRANSMITTERS_LIST, "r");
            paramsRaw = fl.read();
            paramsList = paramsRaw.split("\n");
            cnt = 1
            for paramLine in paramsList:
                if (len(paramLine) == 0):
                    pass
                elif (paramLine[0] == "#"):
                    pass
                else:
                    paramPair = paramLine.split("=");
                    numItems = len(paramPair);
                    if (numItems == 2):
                        mac_address = paramPair[0].strip();
                        param_value = paramPair[1].strip();
                        self.add(mac_address=mac_address, target_id=cnt, uuid=param_value, major="", minor="")
                        cnt += 1
        except Exception as ex:
            print("Cannot read static transmitters config: ", self.STATIC_TRANSMITTERS_LIST)
            print(ex)
            raise ex
        return
    
            