'''
Created on Jun 4, 2016

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
from typing import List
import sys
# from subprocess import call
from subprocess import check_output
from subprocess import CalledProcessError
from aero_tracker.sensor.sensor_device import SensorDevice
from aero_tracker.ble.ble_set_advertising_parameters import BLESetAdvertisingParameters

class DeviceInfo(object):
    '''
    Gets information about a sensor device number.  Also, configures devices for BLE scanning support.
    
    Note: Must be run as root to work.
    
    Run as: python3 -m plane_tracker.sensors.device_info
    '''
    DEVICE_PREFIX = "hci"
    ADV_FREQ_INTERVAL = 0.625 #minimum miliseconds per cycle
    MIN_ADV_FREQ = 50
    
    HCI_LE_Set_Advertising_Data = 0x0008
    HCI_LE_Set_Advertising_Parameters = 0x0006
    
    BLE_ADV_NON_CONNECTABLE = '03'
    BLE_ADV_CONNECTABLE = '00'
    
    _debug_level = 2
    _params = None
    _devices = []
    
    def get_devices(self)->List[SensorDevice]:
        return self._devices
    
    def get_num_devices(self)->int:
        return len(self._devices)
    
    def get_device_by_address(self, mac_address)->SensorDevice:
        for dev in self._devices:
            if (dev.mac_address == mac_address):
                return dev
        return None
    
    def get_device_by_num(self, dev_num)->SensorDevice:
        for dev in self._devices:
            if (dev.device_num == dev_num):
                return dev
        return None

    def __init__(self, params, debug_level=2):
        '''
        Constructor
        '''
        self._params = params
        self._debug_level = debug_level
        self._devices = self._get_system_devices()
        self._init_ble_features()
        return
        
    def _get_system_devices(self)->List[SensorDevice]:
        try:
            rslts = check_output(["hciconfig"]).decode(sys.stdout.encoding).strip()
            devs = self._create_devices(rslts)
                
            
        except CalledProcessError as cpe:
            print("Failed to fetch device info.  Be sure this is run with root priveledges.")
            print(cpe)
            raise cpe
        return devs
    
    def _create_devices(self, raw_rslts):
        devs = []
        lns = str(raw_rslts).split("\n")
        dev_lns = []
        while (len(lns) > 0):
            ln = lns.pop(0).strip(' \t\n\r')
            if (ln[0:len(self.DEVICE_PREFIX)] == self.DEVICE_PREFIX):
                dev_lns = []
                dev_lns.append(ln)
                for i in range(1,5):
                    dev_lns.append(lns.pop(0).strip(' \t\n\r'))
                devs.append(SensorDevice.create_from_data_list(data_list=dev_lns, params=self._params))
            elif (ln == ""):
                pass
        return devs
    
    def _init_ble_features(self):
        for dev in self._devices:
#             #Bring Device Up
#             rslts = check_output(self._device_up(hci_dev=dev.device_name)).decode(sys.stdout.encoding).strip()
#             if (self._params.debug_level >= 2):
#                 print(rslts)
            
            #Disable Advertising
            rslts = check_output(self._le_set_adv_enable(enabled=False, hci_dev=dev.device_name)).decode(sys.stdout.encoding).strip()
            if (self._params.debug_level >= 2):
                print(rslts)
                
            #Set Advertising Parameters
            rslts = check_output(self._le_set_adv_data(dev.device_name)).decode(sys.stdout.encoding).strip()
            if (self._params.debug_level >= 2):
                print(rslts)
                
            #Enable Advertising
            rslts = check_output(self._le_set_adv_enable(enabled=True, hci_dev=dev.device_name)).decode(sys.stdout.encoding).strip()
            if (self._params.debug_level >= 2):
                print(rslts)
                
        return
    
    def _device_down(self, hci_dev):
        rslts = check_output(['hciconfig', '-a', hci_dev, 'down']).decode(sys.stdout.encoding).strip()
        return rslts
    
    def _device_up(self, hci_dev):
        rslts = check_output(['hciconfig', '-a', hci_dev, 'up']).decode(sys.stdout.encoding).strip()
        return rslts
                
    def _get_adv_frequency(self, adv_per_second=100):
        '''
        Currently, advertising is set in 0.625ms increments, which means a 
        second has 1600 possible steps.  The frequency must be a value 
        in one of these step multiples.
        
        '''
        steps = 1000 / self.ADV_FREQ_INTERVAL #dynamic in case frequency changes
        freq = int(steps / adv_per_second)
        
        if (freq < self.MIN_ADV_FREQ):
            freq = self.MIN_ADV_FREQ
        
        return freq
    
    def _le_set_adv_data(self, hci_dev):
        '''
        LE Set Advertising Data Command
        
        Params: 
        Advertising_Data_Length: 0x00 – 0x1F - The number of significant octets in the Advertising_Data.
        Advertising_Data:
        '''
        parms = BLESetAdvertisingParameters(
            adv_int_min_ms=20, 
            adv_int_max_ms=21, 
            adv_type=BLESetAdvertisingParameters.ADV_IND, 
            own_addr_type=BLESetAdvertisingParameters.ADDR_TYPE_PUBLIC, 
            direct_addr_type=BLESetAdvertisingParameters.ADDR_TYPE_PUBLIC)
        params_bytes = parms.get_bytes()
        rval = ['hcitool', '-i', hci_dev, 'cmd', '0x08']
        for byt in params_bytes:
            rval.append(byt)
        return rval
    
    def _le_set_adv_enable(self, enabled, hci_dev):
        if (enabled):
            return ['hcitool', '-i', hci_dev, 'cmd', '0x08', '0x000A', '01']
        return ['hcitool', '-i', hci_dev, 'cmd', '0x08', '0x000A', '00']
        
# #Tester
# from aero_tracker.params.at_sensor_cluster_params import ATSensorClusterParams
#  
# params = ATSensorClusterParams("/etc/popt/aero_tracker/at_sensors.conf")
# di = DeviceInfo(params=params)
# print (di.get_devices())
