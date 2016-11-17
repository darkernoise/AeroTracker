'''
Created on Sep 18, 2016

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

class AT_ResultListenerParams(ATParameters):
    '''
    Result listener parameters.
    '''
    
    manager_auth_key = 'password'
    lap_timeout_secs = 8
    race_timeout_secs = 30
    min_lap_y_distance = 10.0
    
    def set_param_value(self, param_name, param_value):
        super().set_param_value(param_name, param_value)
        if (param_name=="MANAGER_AUTH_KEY"):
            if (param_value != ''):
                self.manager_auth_key = param_value
        elif (param_name=="LAP_TIMEOUT_SECS"):
            if (param_value != ''):
                self.lap_timeout_secs = float(param_value)
        elif (param_name=="RACE_TIMEOUT_SECS"):
            if (param_value != ''):
                self.race_timeout_secs = float(param_value)
        elif (param_name=="MIN_LAP_Y_DISTANCE"):
            if (param_value != ''):
                self.min_lap_y_distance = float(param_value)
        return

        