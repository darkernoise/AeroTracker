'''
Created on Sep 19, 2016

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
import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import mpl_toolkits.mplot3d.axes3d as p3
# import bisect

from aero_tracker.network.at_socket_handler_base import AT_SocketHandlerBase
from aero_tracker.log.at_logging import AT_Logging
from aero_tracker.network.at_protocol import AT_Protocol
from aero_tracker.data.lap_data_sort import LapDataSort
from aero_tracker.client.at_graphing_gui_display import AT_GraphingGUIDisplay

class AT_GraphingGUIHander(AT_SocketHandlerBase):
    '''
    Data socket handler class for the AeroTracker real-time graphing GUI.
    '''
    
    _lap_data_sort = None
    _graph_display = None
    
    def process_data(self, data_packet, *args):
        '''
        Receives result data from data processing servers.
        
        params:
        * data_packet is in form: timestamp|X|Y|Z<terminator>  : 
        Example 1474427065.842134|12.782021852893136|6.995738723356363|-10.270705111024654?
        '''
        try:
            dat_list = data_packet[:-1].split(AT_Protocol.DATA_DELIMITIER)
            conv_dat = []
            for d in dat_list:
                conv_dat.append(float(d))
            new_graph = self._lap_data_sort.append_data(dat=conv_dat)
            if (new_graph):
                self._graph_display.reset_graph()
            self._graph_display.append_coordinate(rslt=dat_list)
                
#             plt.draw()
#             plt.pause(0.05)
        except Exception as ex:
            self._log.log3(msg1="Exception:", msg2=str(ex), msg3='Type:' + type(ex).__name__, caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
            self._log.print_traceback(ex=ex, caller=self)
            raise ex
        return
    
#     def _smooth_and_distribute_axis(self, axis_list):
#         '''
#         The graphing GUI can only display a limited number of data points.  Thus, this method
#         takes incoming data points for an axis to smooth the values.
#         '''
#         right_indx = bisect.bisect_right(a=self._key_list, x=rssi)
#         return
    
    def handle_start(self, connection, address, *args):
        '''
        Called at the initial connection from a socket and before entering in a data receive loop. Redefine 
        for any actions that should be executed once before data receive.
        '''
        self._lap_data_sort = LapDataSort(self.params)
        self._graph_display = AT_GraphingGUIDisplay(self.params)
        self._graph_display.start()
        return
    
    def handle_end(self, connection, address, *args):
        '''
        Called when the socket has disconnected and about to shut down.
        '''
        return
    
    
    
    
        