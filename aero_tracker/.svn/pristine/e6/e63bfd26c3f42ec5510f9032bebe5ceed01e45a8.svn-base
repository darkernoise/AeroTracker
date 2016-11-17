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

from aero_tracker.client.result_listener_base import ResultListenerBase
from aero_tracker.client.at_result_data_listener_handler import AT_ResultDataListenerHandler

class AT_ResultDataListener(ResultListenerBase):
    '''
    Starts a socket server to listen for result data
    '''
    
    _listener_name = ''
    
    @property
    def listener_name(self)->str:
        return self._listener_name
    
    @property
    def handler_class(self):
        return AT_ResultDataListenerHandler

    def __init__(self, params, listener_name, rslt_queue, log_file,
        event_on_new_lap, event_on_data, event_on_cut, event_on_turn_apex):
        '''
        Constructor
        '''
        self._listener_name = listener_name
        super().__init__(params=params, rslt_queue=rslt_queue, log_file=log_file)
        return
        
        