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

from aero_tracker.params.at_parameters import ATParameters

class AT_ActivityMonitorParams(ATParameters):
    '''
    Parameterse object for the Aero Tracker Activity Monitor.
    '''
    
    client_display_name = 'AeroTracker Data Monitor'
    manager_auth_key = 'password'
    
    def set_param_value(self, param_name, param_value):
        super().set_param_value(param_name, param_value)
        if (param_name=="CLIENT_DISPLAY_NAME"):
            if (param_value != ''):
                self.client_display_name = param_value
        elif (param_name=="MANAGER_AUTH_KEY"):
            if (param_value != ''):
                self.manager_auth_key = param_value
        return