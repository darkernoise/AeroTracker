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

import time
import signal
import sys
from aero_tracker.log.at_logging import AT_Logging
from aero_tracker.server.at_daemon_base import AT_DaemonBase
from aero_tracker.params.at_activity_monitor_params import AT_ActivityMonitorParams
from aero_tracker.monitor.activity_monitor import ActivityMonitor

class AT_ActivityMonitorDaemon(AT_DaemonBase):
    '''
    Client tool that displays system activity to the standard output console.
    
    Note: Run from the command line: python3.5 -m aero_tracker.at_activity_monitor_daemon start
    '''
    
    CONF_FILE = "/etc/popt/aero_tracker/at_activity_monitor.conf"
    DAEMON_NAME = "Aero Tracker Activity Monitor"
    LOG_FILE = '/var/log/aerotracker/at_activity.log'
    
    @property
    def daemon_name(self):
        ':rtype list(str)'
        return self.DAEMON_NAME
    
    @property
    def debug_level(self):
        'rtype int'
        if (self.params != None):
            return self.params.debug_level
        return super().debug_level
    
    def run(self):   
        self.log.log(msg1='Run called', caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
        mon = ActivityMonitor(self.params)
        #note, the monitor is not being run in thread mode, but instead directly here.
        while (self.is_running):
            try:
                mon.execute_direct()
                self.log.log(msg1='Monitor running again', caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
            except Exception as ex:
                self.log.log2(msg1='Exception:', msg2=str(ex), caller=self, msgty=AT_Logging.MSG_TYPE_ERROR)
                time.sleep(1) 
#         mon.stop()  
        return 
    
    def load_parameters(self):
        return AT_ActivityMonitorParams(self.CONF_FILE)

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(log_file=self.LOG_FILE)
        return
        

##############################
# Program
##############################

#pydevd.settrace('192.168.0.150');

obj = AT_ActivityMonitorDaemon();

def signalHandler(arg1, arg2):
    print("signalHandler")
    obj.cleanUp();
    sys.exit();
    return

signal.signal(signal.SIGINT, signalHandler);
signal.signal(signal.SIGTERM, signalHandler);

try:
    print(sys.argv)    
    for arg in sys.argv:
        if arg == "start" or arg == "" or arg == "--verbosity":
            obj.start();
        elif arg == "stop":
            obj.stop();
        elif arg.startswith('/var/popt/'):
            pass
        else:
            print("Unknown command line parameter: " + arg)
except KeyboardInterrupt:
    print("KeyboardInterrupt detected")
    obj.cleanUp();