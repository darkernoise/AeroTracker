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

from aero_tracker.params.at_parameters import ATParameters

class AT_DataProcServerParams(ATParameters):
    '''
    Plane Tracker Server specific parameters
    '''
    QUEUE_SIZE_DIFFERENTIAL = 20
    DIFFERENTIAL_MAX_PCT = 200
    QUEUE_SIZE_SMOOTHING = 100
    TRIANGULATIONS_PER_SECOND = 40
    MAX_TIME_SLICE_DEVIATION = 0.2
    MAX_TIME_SLICE_DIFF = 0.3
    DB_SERVER = "127.0.0.1"
    DB_SCHEMA = "plane_tracker"
    DB_USER = "user"
    DB_PASS = "password"
    NUM_PROC_SERVERS = 1 #Number of data processing server processes to spawn
    MANAGER_AUTH_KEY = 'password'
    PROC_SERVER_NAME = 'Data Server 1'
    ONLY_LOG_SENSOR = None
    TIME_SLICE_QUEUE_BUFFER = 20
    SECONDARY_FILTER_BUFFER = 100
    SECONDARY_FILTER_WINDOW = 21
    PRINT_PREFILTERED_RESULTS = False
    PRINT_FILTERED_RESULTS = False
    NUM_SENSOR_CLUSTERS = 1
    
    @property
    def manager_auth_key(self):
        return self.MANAGER_AUTH_KEY

    def set_param_value(self, param_name, param_value):
        super().set_param_value(param_name, param_value)
        if (param_name=="QUEUE_SIZE_DIFFERENTIAL"):
            self.QUEUE_SIZE_DIFFERENTIAL = int(param_value)
        elif (param_name=="DIFFERENTIAL_MAX_PCT"):
            self.DIFFERENTIAL_MAX_PCT = int(param_value)
        elif (param_name=="QUEUE_SIZE_SMOOTHING"):
            self.QUEUE_SIZE_SMOOTHING = int(param_value)
        elif (param_name=="TRIANGULATIONS_PER_SECOND"):
            self.TRIANGULATIONS_PER_SECOND = int(param_value)
        elif (param_name=="MAX_TIME_SLICE_DEVIATION"):
            self.MAX_TIME_SLICE_DEVIATION = float(param_value)
        elif (param_name=="MAX_TIME_SLICE_DIFF"):
            self.MAX_TIME_SLICE_DIFF = float(param_value)
        elif (param_name=="DB_SERVER"):
            self.DB_SERVER = param_value
        elif (param_name=="DB_SCHEMA"):
            self.DB_SCHEMA = param_value
        elif (param_name=="DB_USER"):
            self.DB_USER = param_value
        elif (param_name=="DB_PASS"):
            self.DB_PASS = param_value
        elif (param_name=="NUM_PROC_SERVERS"):
            self.NUM_PROC_SERVERS = int(param_value)
        elif (param_name=="NUM_SENSOR_CLUSTERS"):
            self.NUM_SENSOR_CLUSTERS = int(param_value)
        elif (param_name=="MANAGER_AUTH_KEY"):
            self.MANAGER_AUTH_KEY = param_value
        elif (param_name=="PROC_SERVER_NAME"):
            self.PROC_SERVER_NAME = param_value
        elif (param_name=="ONLY_LOG_SENSOR"):
            self.ONLY_LOG_SENSOR = param_value
        elif (param_name=="TIME_SLICE_QUEUE_BUFFER"):
            self.TIME_SLICE_QUEUE_BUFFER = int(param_value)
        elif (param_name=="SECONDARY_FILTER_BUFFER"):
            self.SECONDARY_FILTER_BUFFER = int(param_value)
        elif (param_name=="PRINT_PREFILTERED_RESULTS"):
            if (param_value == '1'):
                self.PRINT_PREFILTERED_RESULTS = True
            else:
                self.PRINT_PREFILTERED_RESULTS = False
        elif (param_name=="PRINT_FILTERED_RESULTS"):
            if (param_value == '1'):
                self.PRINT_FILTERED_RESULTS = True
            else:
                self.PRINT_FILTERED_RESULTS = False
        return
    
    