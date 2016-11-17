'''
Created on May 28, 2016

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

from multiprocessing.connection import Connection
from aero_tracker.ble.ble_scanner import BLEScanner
from aero_tracker.ble.ble_packet import BLE_Packet
from aero_tracker.sensor.sensor_device import SensorDevice
# from aero_tracker.target.tx_item import TX_Item
from aero_tracker.target.tx_item_list import TX_Item_List
from aero_tracker.target.at_target import AT_Target
from aero_tracker.common.at_process_base import AT_ProcessBase
from aero_tracker.log.at_logging import AT_Logging
from aero_tracker.network.at_protocol import AT_Protocol

class AT_Sensor(AT_ProcessBase):
    '''
    Aero Tracker Sensor class is a multi-process component which runs for each separate sensor.
    '''
    SENSOR_READ_CNT = 1
    PACKET_STATUS_CNT = 1000
    PROCESS_NAME = "PT_Sensor"
    LINE_TERM = "\n"
    
    _parent = None
    _device_number = 0
    _host_name = ""
    _port = ""
    _TX_List = None #List of all transmitting devices to listen for
    _TX_List_Chagned = True
    _sensor = None #Type SensorDevice
    _packets_sent = 0
    _packet_status_cnt = 0
    _targets = []
    _dir_store = None
    __bleScanner1 = None
    _pipe_connection = Connection
    
    @property
    def sensor_id(self):
        return self._sensor.sensor_id
    
    def run_clycle(self):
        '''
        Executes within the while is_running loop.
        '''
        if (not self.is_running):
            return
        returned_list = self.__bleScanner1.getEvents(sensor_id=self.sensor_id, 
            num_events=self.SENSOR_READ_CNT, tx_list=self._get_tx_list())
        ble_pkt = BLE_Packet
        for ble_pkt in returned_list:
            self.thread_lock.acquire()
            self._enqueue(ble_pkt=ble_pkt)
            self.thread_lock.release()                
        return
    
    def before_close(self):
        '''
        Executes before the run cycle exists.
        '''
        for trgt in self._targets:
            try:
                trgt.stop() #Signal to close the open socket
            except:
                pass
        return
    
    def finally_hander(self):
        '''
        Executed in a finally block in the exception handler.
        '''
        self.before_close()
        return
    
    def __init__(self, parent, 
                 sensor:SensorDevice, \
                 host_name:str, 
                 port:int, \
                 dir_store,
                 pipe_connection:Connection,
                 tx_power_adv_ind, tx_power_adv_scan_rsp, params):
        '''
        Constructor
        '''
        super().__init__(params)
        #Set this as a daemonic process
        self.daemon = True
        self._sensor = sensor
        self._parent = parent
        self._host_name = host_name
        self._port = port
        self._pipe_connection = pipe_connection
        self._dir_store = dir_store
        self._set_sensor_in_dir_store(sensor=sensor, dir_store=dir_store)
        self.__bleScanner1 = BLEScanner(sensor.sensor_id, sensor.device_num, tx_power_adv_ind, tx_power_adv_scan_rsp);
        return
    
    def _set_sensor_in_dir_store(self, sensor:SensorDevice, dir_store):
        '''
        Saves information about the sensor device into the directory store so that this can be 
        used by later components during trilateration and calculation.
        '''
        dir_store.add_sensor(sensor)
        return
    
    def _get_tx_list(self):
        '''
        Gets a list of all transmitters to listen for.
        '''
        #TODO
        #For now, this is hard-coded by means of a Static Transmitters file
        if (self._TX_List_Chagned):
            self._TX_List = TX_Item_List()
            self._TX_List_Chagned = False
        return self._TX_List
    
    def _enqueue(self, ble_pkt):
        tgt = self._get_target(ble_pkt)
        tgt.enqueue(ble_pkt)
        return
    
    def _get_unique_target_id(self, ble_pkt):
        #TODO
        return ble_pkt.target_id
    
    def _get_target(self, ble_pkt)->AT_Target:
        tgt_id = self._get_unique_target_id(ble_pkt)
        for tgt in self._targets:
            if (tgt_id == tgt.get_target_id()):
                return tgt
        #Create missing target
        tgt = AT_Target(log=self.log, 
            sensor=self._sensor, 
            target_id=tgt_id, 
            dir_store=self._dir_store, 
            pipe_connection=self._pipe_connection,
            params=self._params)
        self._targets.append(tgt)
        return tgt
    
    def stop(self):
#         self.before_close()
        try:
            super().stop()
        except:
            pass
        
        return
        