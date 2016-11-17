'''
Created on Oct 4, 2016

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
import typing
from aero_tracker.network.at_socket_handler_base import AT_SocketHandlerBase
from aero_tracker.log.at_logging import AT_Logging
from aero_tracker.network.at_protocol import AT_Protocol

class AT_ResultDataListenerHandler(AT_SocketHandlerBase):
    '''
    Socket handler for the result data listener.
    '''
    
    _first_packet = True
    _target_id = None
    _cluster_id = None
    
    
    def process_data(self, data_packet, *args):
        '''
        Receives result data from data processing servers.
        
        params:
        * data_packet is in form: timestamp|X|Y|Z<terminator>  : 
        Example 1474427065.842134|12.782021852893136|6.995738723356363|-10.270705111024654?
        '''
        try:
            if (self._first_packet):
                self._target_id = data_packet[:-1]
                self._first_packet = False
            else:
                dat_list = data_packet[:-1].split(AT_Protocol.DATA_DELIMITIER)
                if (len(dat_list) == 2):
                    #Server is re-sending cluster and target ID
                    self._cluster_id = dat_list[0]
                    self._target_id = dat_list[1]
                else:
                    conv_dat = []
                    for d in dat_list:
                        conv_dat.append(float(d))
        #             print('data received:', conv_dat)
                    self.server.result_queue.put([self._cluster_id, self._target_id, conv_dat])
            
        except Exception as ex:
            self._log.log3(msg1="Exception:", msg2=str(ex), msg3='Type:' + type(ex).__name__, caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
            self._log.print_traceback(ex=ex, caller=self)
            raise ex
        return

    def handle_start(self, connection, address, *args):
        '''
        Called at the initial connection from a socket and before entering in a data receive loop. Redefine 
        for any actions that should be executed once before data receive.
        '''
        return
    
    def handle_end(self, connection, address, *args):
        '''
        Called when the socket has disconnected and about to shut down.
        '''
        self._first_packet = False
        return
        