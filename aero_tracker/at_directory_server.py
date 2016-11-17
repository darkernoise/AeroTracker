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

import signal
import sys
import time
import threading
# import socket
# import multiprocessing as mp
from aero_tracker.log.at_logging import AT_Logging
from aero_tracker.params.at_directory_server_params import AT_DirectoryServerParams
from aero_tracker.server.directory.at_directory_mp_manager_server import AT_DirectoryMPManagerServer
from aero_tracker.server.at_daemon_base import AT_DaemonBase

class AT_Directory_Server(AT_DaemonBase):
    '''
    Server which acts as a central directory server for remote sensor clusters.  Remote sensor clusters 
    contact this server to request a data processing server and port for each target being tracked.
    
    Note: Run from the command line: python3 -m aero_tracker.at_directory_server start
    '''
    ##############################
    # Constants
    ##############################
    CONF_FILE = "/etc/popt/aero_tracker/at_directory_server.conf"
    DAEMON_NAME = "Aero Tracker Directory Server"
    LOG_FILE = '/var/log/aerotracker/at_directory.log'
    
    
    ##############################
    # Variables
    ##############################
    _queue_manager = None
    _socket = None
    _mp_manager_server = None
    
    ##############################
    # Public Methods
    ##############################
    
#     @staticmethod
#     def connection_handle(manager_port, connection, address, dir_store, params):
#         req_hndl = AT_DirectoryServerHandler(manager_port, params)
#         req_hndl.handle(connection, address, dir_store)
#         return
    
    def run(self):   
        try:
            self._print_info()
            
            self.log.log(msg1='Starting Manager', caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
            self._mp_manager_server.start()
            while (self.is_running):
                try:
                    time.sleep(1)
                except Exception as ex2:
                    self.log.log3(msg1=self.DAEMON_NAME,msg2='exception in', msg3=str(ex2), caller=self)
                time.sleep(1)
                
            
        except Exception as ex:
            self.log.log3(msg1=self.DAEMON_NAME,msg2='exception in', msg3=str(ex), caller=self)
            
        try:
            self._mp_manager_server.stop()
        except:
            pass
            
        self.log.log2(msg1=self.DAEMON_NAME, msg2='Shutting Down', caller=self, msgty=AT_Logging.MSG_TYPE_INFO)
        self._mp_manager_server.stop()
        self.stop()
        return 

    def load_parameters(self):
        return AT_Logging(self._params)
    
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(log_file=self.LOG_FILE)
        self._params = AT_DirectoryServerParams(self.CONF_FILE)
        AT_Directory_Server.lock = threading.RLock()
        self._mp_manager_server = AT_DirectoryMPManagerServer(self._params)
        return
    
##############################
# Program
##############################

#pydevd.settrace('192.168.0.150');

daemon = AT_Directory_Server();

def signalHandler(arg1, arg2):
    print(AT_Directory_Server.DAEMON_NAME, "signalHandler called to shutdown process")
    daemon.cleanUp();
    sys.exit();
    return

signal.signal(signal.SIGINT, signalHandler);
signal.signal(signal.SIGTERM, signalHandler);

try:
    print(sys.argv)    
    for arg in sys.argv:
        if arg == "start" or arg == "" or arg == "--verbosity":
            daemon.start();
            time.sleep(1)
        elif arg == "stop":
            daemon.stop();
        elif arg.startswith('/var/popt/'):
            pass
        else:
            print("Unknown command line parameter: " + arg)
except KeyboardInterrupt:
    print("KeyboardInterrupt detected")
    daemon.cleanUp();
        