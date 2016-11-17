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


class ATParameters(object):
    '''
    Basic parameters read from flat file.
    '''
    param_file = ""
    debug_level = 0
    server_name = "localhost"
    port = 0
    pid_file = ""
    
    def set_param_value(self, param_name, param_value):
        if (param_name == "DEBUG_LEVEL"):
            self.debug_level = int(param_value)
        elif (param_name == "SERVER_NAME"):
            self.server_name = param_value
        elif (param_name == "PORT"):
            self.port = int(param_value)
        elif (param_name == "PID_FILE"):
            self.pid_file = param_value
        return
    
    def param_value_to_array(self, param_value):
        rvals = param_value.split(",")
        for i in range(0, len(rvals)):
            rvals[i] = rvals[i].strip(' \t\n\r')
        return rvals

    def __init__(self, param_file):
        '''
        Constructor
        '''
        self.paramFile = param_file
        
        fl = open(param_file, "r");
        params_raw = fl.read();
        params_list = params_raw.split("\n");
        for param_line in params_list:
            if (len(param_line) == 0):
                pass
            elif (param_line[0] == "#"):
                pass
            else:
                param_pair = param_line.split("=");
                num_items = len(param_pair);
                if (num_items == 2):
                    param_name = param_pair[0].strip();
                    param_value = param_pair[1].strip();
                    self.set_param_value(param_name, param_value)
                    
        return