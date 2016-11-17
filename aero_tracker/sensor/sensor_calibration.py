'''
Created on Sep 4, 2016

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

import numpy as np
import scipy.stats
from aero_tracker.params.at_sensor_cluster_params import ATSensorClusterParams
from aero_tracker.ble.ble_scanner import BLEScanner
from aero_tracker.target.tx_item_list import TX_Item_List
from aero_tracker.sensor.sensor_calibration_result import SensorCalibrationResult

class SensorCalibration(object):
    '''
    Executes a sensor calibration procedure for the system.  This is a command line application 
    with an interactive run cycle designed to calibrate the sensors in a setup environment. The 
    interactive procedure is:
    
    * Ask user to setup calibration stand and sensor in the field
    * Prompt for a X,Y,Z coordinate being tested
    * Asks the user to wait for a test cycle
    * Shows the calibration results and asks the user to re-test or accept the results.
    * Once accepted, the values are written to a calibration file to save. 
    
    Note: Run from the command line: python3.5 -m aero_tracker.sensor.sensor_calibration
    '''
    CONF_FILE = "/etc/popt/aero_tracker/at_sensors.conf"
    CALIBRATION_FILE = '/etc/popt/aero_tracker/at_sensor_calibration.dat'
    CALIBRATION_CYCLES = 2
    SEPERATOR = '|'
    MEDIAN_NOISE_CUT = 0.3 #Cut off 30% lowest and highest
    
    @property
    def params(self):
        return self._params
    
    _params = None
    __sensors = []
    _TX_List = None #List of all transmitting devices to listen for
    _TX_List_Chagned = True
    _ble_scanners = []
    
    def calibrate(self):
        done = False
        input('Place the calibration stand at a new X,Y,Z coordinate and press any Enter to start')
        ovrw = (input('Do you wish to Overwrite or Append to existing calibration? (O or A)')).upper()
        fl = None
        try:
            if (ovrw == 'A'):
                fl = open(self.CALIBRATION_FILE, 'a')
            else:
                fl = open(self.CALIBRATION_FILE, 'w')
            while (not done):
                xyz = input('Enter the coordinate in the format X,Y,Z and press enter')
                if (self._validate_xyz(xyz=xyz)):
                    rslts = self._run_sensor_test_cycle(xyz)
                    calc_rslts = self._calc_results_per_sensor(xyz, rslts)
                    srslt = self._rslt_str(calc_rslts)
                    print(srslt)
                    ans = (input('Do you wish to accept the result or repeat test? (A or R)')).upper()
                    if (ans == 'A'):
                        fl.write(srslt + '\n')
                    ans = (input('Would you like to enter another calibration point? (Y or N)')).upper()
                    if (ans != 'Y'):
                        done = True
                    else:
                        done = False
        except Exception as ex:
            print('Critical error: ', ex)
        fl.close()
        return

    def __init__(self):
        '''
        Constructor
        '''
        self._params = ATSensorClusterParams(self.CONF_FILE)
        self._setup_ble_scanners()
        return
    
    
    def _rslt_str(self, calc_rslts):
        rval = ''
        for i in range(0, len(calc_rslts)):
            if (i == 0):
                rval = '[' + calc_rslts[0] + ']'
            else:
                rval += self.SEPERATOR
                sc_rslt = calc_rslts[i] #type SensorCalibrationResult
                rval += sc_rslt.sensor_id
                rval += self.SEPERATOR
                rval += str(sc_rslt.rssi)
        return rval
    
    def _calc_results_per_sensor(self, xyz, rslts):
        rval = []
        xyz_parts = xyz.split(',')
        rval.append(xyz)
        for i in range(0, len(rslts)):
            snsr_rslts = rslts[i]
            avg_rssi = self._average_rslts(snsr_rslts)
            snsr = self.params.get_sensor_by_index(i)
            rval.append(SensorCalibrationResult(sensor_id=snsr.sensor_id, X=xyz_parts[0], Y=xyz_parts[1], Z=xyz_parts[2], rssi=avg_rssi))
        return rval
    
    def _average_rslts(self, snsr_rslts):
        '''
        Calculates median average deviation.
        '''
        if (len(snsr_rslts) == 0):
            raise Exception('No valid results found')
        rssi_vals = np.array(snsr_rslts)
        rval = scipy.stats.trim_mean(a=rssi_vals, proportiontocut=self.MEDIAN_NOISE_CUT)
        return rval
    
    def _setup_ble_scanners(self):
        self._ble_sensors = []
        for i in range(0, self.params.num_sensors):
            snsr = self.params.get_sensor_by_index(i) #type SensorDevice
            self._ble_scanners.append(BLEScanner(sensor_id=snsr.sensor_id, \
                device_number=snsr.device_num, 
                defTXPower_AdvInd=0, defTXPower_AdvScanResp=0));
        return
    
    def _run_sensor_test_cycle(self, xyz):
        rslts = []
        print('Running sensor test. Please wait...')
        try:
            for i in range(0, self.CALIBRATION_CYCLES):
                self._run_sensor_test(xyz, rslts)
        except Exception as ex:
            print('Exception: ', ex)
            raise ex
        return rslts
        
    
    def _run_sensor_test(self, xyz, rslts):
        for i in range(0, self.params.num_sensors):
            scanner = self._ble_scanners[i]
            snsr = self.params.get_sensor_by_index(i)
            returned_list = scanner.getEvents(sensor_id=snsr.sensor_id, num_events=10, tx_list=self._get_tx_list())
            if (len(returned_list) == 0):
                raise Exception('Calibration sensor could not be read')
            if (len(rslts) <= i):
                rslts.append([])
            for ble_pkt in returned_list:
                rslts[i].append(ble_pkt.rssi)
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
    
    def _validate_xyz(self, xyz):
        try:
            parts = xyz.split(',')
            if (len(parts) != 3):
                print('You entered: ', xyz, ' which is invalid.')
                print('Value entered must be in the form of X,Y,Z (with "," (comma) separating the values)')
                return False
            return True
        except Exception as ex:
            print('You entered: ', xyz, ' which is invalid.')
            print('Value entered must be in the form of X,Y,Z (with "," (comma) separating the values)')
            return False
        return
    
    
##############################
# Program
##############################        
#Main program
obj = SensorCalibration()
obj.calibrate()


