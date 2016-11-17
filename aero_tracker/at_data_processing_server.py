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
import traceback
import typing
from aero_tracker.log.at_logging import AT_Logging
from aero_tracker.exception.at_exception import AT_Exception
from aero_tracker.params.at_data_proc_server_params import AT_DataProcServerParams
from aero_tracker.server.data_proc.at_data_proc_server_worker import AT_DataProcServerWorker
from aero_tracker.server.directory.at_directory_mp_manager import AT_DirectoryMPManager

from aero_tracker.server.at_daemon_base import AT_DaemonBase

class AT_DataProcessingServer(AT_DaemonBase):
    '''
    Receives remote connections from sensor cluster which then send all pre-filtered sensor data to
    this node for trilateration, final filtering, and storage.
    
    Note: Run from the command line: python3.5 -m aero_tracker.at_data_processing_server start
    '''
    ##############################
    # Constants
    ##############################
    CONF_FILE = "/etc/popt/aero_tracker/at_data_proc_server.conf"
    DAEMON_NAME = "Aero Tracker Data Processing Server"
    
    ##############################
    # Variables
    ##############################
    _workers = typing.List
    
    ##############################
    # Public Methods
    ##############################
    
    def run(self):
        self.log.log2(msg1=self.DAEMON_NAME, msg2='Started', caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)  
        try:    
            #Get instance of the directory store from the manager
            AT_DirectoryMPManager.register_client_methods()
            manager =  AT_DirectoryMPManager(address=(self._params.server_name, self._params.port), \
                authkey=bytearray(self._params.MANAGER_AUTH_KEY,'ascii'))
            manager_connected = False
            while (not manager_connected):
                try:
                    manager.connect()
                    manager_connected = True
                except Exception as exi:
                    self.log.log2(msg1='Could not connect to Directory Server. Retrying...', msg2=str(exi), caller=self, msgty=AT_Logging.MSG_TYPE_WARNING)
                    time.sleep(1)
            dir_store = manager.get_instance()
            
            for i in range(0, self.params.NUM_PROC_SERVERS):
                #Start data processing server
                wrkr = AT_DataProcServerWorker(dir_store=dir_store, params=self._params, worker_num=i)
                wrkr.start()
                self._workers.append(wrkr)
      
            while (self.is_running):
                time.sleep(1)
        except Exception as ex:
            traceback.print_stack(f=None, limit=None, file=None)
            self.log.log3(msg1=self.DAEMON_NAME,msg2='exception in', msg3=str(ex), caller=self, msgty=AT_Logging.MSG_TYPE_ERROR)
            self.log.print_traceback(ex=ex, caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
            
        self.log.log(msg1='Stopped', caller=self, msgty=AT_Logging.MSG_TYPE_INFO)
        return 

    def load_parameters(self):
        return AT_Logging(self._params)
    
    def stop(self):
        self._stop_workers()
        super().stop()
        return
    
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self._params = AT_DataProcServerParams(self.CONF_FILE)
        self._workers = []
        return
    
    def _stop_workers(self):
        self.log.log(msg1='Issuing stop command to child workers', caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
        for wrkr in self._workers:
            wrkr.stop()
        return
    
##############################
# Program
##############################

#pydevd.settrace('192.168.0.150');

daemon = AT_DataProcessingServer();

def signalHandler(arg1, arg2):
    print(AT_DataProcessingServer.DAEMON_NAME, "signalHandler called to shutdown process")
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
        