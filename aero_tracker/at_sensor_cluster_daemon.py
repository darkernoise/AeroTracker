'''
Created on May 23, 2016

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
import bluetooth
from aero_tracker.params.at_sensor_cluster_params import ATSensorClusterParams
from aero_tracker.sensor.at_sensor import AT_Sensor
from aero_tracker.server.at_daemon_base import AT_DaemonBase
from aero_tracker.server.directory.at_directory_mp_manager import AT_DirectoryMPManager
from aero_tracker.log.at_logging import AT_Logging
from aero_tracker.network.at_pipe_pool import AT_PipePool
from aero_tracker.data.at_data_sorter import AT_DataSorter

class ATSensorClusterDaemon(AT_DaemonBase):
    '''
    Aero Tracker Sensor Cluster Daemon.
    
    Note: Run from the command line: python3 -m aero_tracker.at_sensor_cluster_daemon start
    '''
    
    CONF_FILE = "/etc/popt/aero_tracker/at_sensors.conf"
    DAEMON_NAME = "Aero Tracker Sensor Daemon"
    LOG_FILE = '/var/log/aerotracker/at_sensor.log'
    DATA_SORTER_LOG_FILE = '/var/log/aerotracker/at_datasort.log'
    
    __sensors = []
    _dir_store = None
    _data_sorter = AT_DataSorter
    _pipe_pool = AT_PipePool
    
    @property
    def daemon_name(self):
        ':rtype list(str)'
        '''
        Name of the daemon.
        '''
        return self.DAEMON_NAME
    
    @property
    def cluster_id(self):
        return self.params.sensorClusterID
    
    @staticmethod
    def list_devices(self):
        nearby_devices = bluetooth.discover_devices(lookup_names = False)
        for bdaddr in nearby_devices:
            print("addr: ", bdaddr)
        return
    
    @property
    def data_sorter_log_file(self):
        return self.DATA_SORTER_LOG_FILE
    
    def run(self):   
        if (self._params.debug_level >= 1):
            print("Starting ", self.DAEMON_NAME)
            self._print_info()
        for sensor in self.__sensors:
            sensor.start()
        
        while (self.is_running):
            time.sleep(1)
        
        return 
    
    #Server stop signaled
    def stop(self):
        super().stop()
        self._run = False;
        self.log.log2(msg1=self.daemon_name, msg2='stop requested', caller=self, msgty=AT_Logging.MSG_TYPE_INFO)
        for sensor in self.__sensors:
            sensor.stop()
            try:
                sensor.terminate()
            except:
                pass
        self.cleanUp()
        return
    
    def cleanUp(self):
        super().cleanUp()
        return

    def load_parameters(self):
        #Redefine to return an instance of the parameters object.
        #Example: return AT_Logging(self._params)
        return ATSensorClusterParams(self.CONF_FILE)

    def __init__(self, default_debug_level=2):
        '''
        Constructor
        '''
        super().__init__(default_debug_level=default_debug_level,log_file=self.LOG_FILE)
        self._data_sorter = AT_DataSorter(params=self.params, log_file=self.data_sorter_log_file)
#         start the data sorter and pipe pool
        self._data_sorter.start()
        self._pipe_pool = self._data_sorter.pipe_pool
        self._createSensors()
        return
    
    def _createSensors(self):
        dir_store = self._get_directory_store()
        self._print_list_data_proc_srvrs()
        self.__sensors = []
        for i in range(0, self._params.num_sensors):
            sensor = self._params.get_sensor_by_index(i) # sensor = SensorDevice:
            sensor_process = AT_Sensor(parent=self, sensor=sensor, \
                host_name=self._params.server_name, 
                port=self._params.port, \
                dir_store=dir_store, \
                pipe_connection=self._pipe_pool.get_child_pipe(pipe_index=i),
                tx_power_adv_ind=self._params.tx_power_adv_ind, \
                tx_power_adv_scan_rsp=self._params.tx_power_adv_scan_rsp, \
                params=self._params)
            self.__sensors.append(sensor_process)
        return
    
    def _get_directory_store(self):
        #Get instance of the directory store from the manager
        manager_connected = False
        AT_DirectoryMPManager.register_client_methods()
        manager =  AT_DirectoryMPManager(address=(self._params.server_name, self._params.port), \
            authkey=bytearray(self._params.manager_auth_key,'ascii'))
        while (not manager_connected):
            try:
                manager.connect()
                manager_connected = True
            except Exception as ex:
                self.log.log2(msg1='Unable to connect to Directory Server Manager at:', \
                    msg2=self._params.server_name + ':' + str(self._params.port), caller=self, msgty=AT_Logging.MSG_TYPE_WARNING)
            
        self._dir_store = manager.get_instance()
        return self._dir_store
    
    def _print_list_data_proc_srvrs(self):
        proc_srvrs = self._dir_store.get_data_proc_srvrs()
        self.log.log2(msg1='Num Data Proc Srvrs:', msg2=str(len(proc_srvrs)), caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
        for proc_addr in proc_srvrs:
            self.log.log2(msg1='Proc Srvr:', msg2=proc_addr.address + ':' + str(proc_addr.port), caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
        return
    

##############################
# Program
##############################

#pydevd.settrace('192.168.0.150');

daemon = ATSensorClusterDaemon();

def signalHandler(arg1, arg2):
    print("signalHandler")
    daemon.stop()
    sys.exit();
    return

signal.signal(signal.SIGINT, signalHandler);
signal.signal(signal.SIGTERM, signalHandler);

try:
    print(sys.argv)    
    for arg in sys.argv:
        if arg == "start" or arg == "" or arg == "--verbosity":
            daemon.start();
        elif arg == "list":
            ATSensorClusterDaemon.list_devices()
        elif arg == "stop":
            daemon.stop();
        elif arg.startswith('/var/popt/'):
            pass
        else:
            print("Unknown command line parameter: " + arg)
except KeyboardInterrupt:
    print("KeyboardInterrupt detected")
    daemon.cleanUp();