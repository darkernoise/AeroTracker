'''
Created on Sep 7, 2016

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
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from aero_tracker.sensor.sensor_calibration_matrix import SensorCalibrationMatrix
from aero_tracker.params.at_activity_monitor_params import AT_ActivityMonitorParams
from aero_tracker.server.directory.at_directory_server_client import AT_DirectoryServerClient
from aero_tracker.log.at_logging import AT_Logging

class SensorCalibrationGUI(object):
    '''
    Visually graphs the sensor calibration per sensor.
    
    start with the command: python3.5 -m aero_tracker.gui.sensor_calibration_gui.py
    '''
    GUI_CONF_FILE = "/etc/popt/aero_tracker/at_sensors.conf"
    
#     _axis = None
    _figure_num = 0
    _figure = None
    _colors = None
    _params = None
    _calib_matrix = None
    _subplot_num = 0
    _log = None
    
    def show(self, sensor_id=None):
        dirsvr_client = AT_DirectoryServerClient(server_name=self._params.server_name, 
            port=self._params.port, auth_key=self._params.manager_auth_key, log=self._log)
        dir_store = dirsvr_client.get_dirctory_store()
        sensor_ids = dir_store.get_calibrated_sensor_ids()
        
        if (sensor_id == None):
            
            num_cols, num_rows = self._get_num_columns_rows(len(sensor_ids))
            for snsr_id in sensor_ids:
                self.draw_sensor_calib(sensor_id=snsr_id,num_cols=num_cols, num_rows=num_rows, dir_store=dir_store)
        else:
            self.draw_sensor_calib(sensor_id=sensor_id, num_cols=1, num_rows=1, dir_store=dir_store)
#         pyplot.gcf().set_size_inches(8, 10)
        
        if (len(sensor_ids) > 0):
            pyplot.tight_layout(pad=0.5, w_pad=0.1, h_pad=0.3)
            pyplot.show()
        return
    
    def get_subplot_num(self):
        self._subplot_num += 1
        return self._subplot_num
    
    def get_figure_num(self):
        self._figure_num += 1
        return self._figure_num
    
    def _get_num_columns_rows(self, num_plots):
        num_cols = 1
        num_rows = 1
        if (num_plots == 2):
            num_cols = 2
        elif (num_plots <= 4):
            num_cols = 2
            num_rows = 2
        elif (num_plots <= 6):
            num_cols = 3
            num_rows = 2
        elif (num_plots <= 9):
            num_cols = 3
            num_rows = 3
        elif (num_plots <= 12):
            num_cols = 3
            num_rows = 4
        elif (num_plots <= 16):
            num_cols = 4
            num_rows = 4
        return num_cols, num_rows
    
    def __init__(self):
        '''
        Constructor
        '''
        self._params = AT_ActivityMonitorParams(self.GUI_CONF_FILE)
        self._log = AT_Logging(self._params)
        num_colors=6
        #Setup color cycle for drawn objects
        self._colors = iter(pyplot.cm.rainbow(np.linspace(0,1,num_colors)))  # @UndefinedVariable
        return
    
    def draw_sensor_calib(self, sensor_id, num_cols, num_rows, dir_store):
        calib_data = dir_store.get_sensor_calib_data(sensor_id)
        dist = []
        rssi = []
        
        for itm in calib_data[1]: # [rssi,distance]
            rssi.append(itm[0])
            dist.append(itm[1])
        pyplot.figure(1, figsize=(18,12), dpi=80)
        pyplot.subplot(num_rows, num_cols, self.get_subplot_num())
        axis = pyplot.gca()
        axis.set_xlabel('Distance')
        axis.set_ylabel('RSSI')
        
#         axis.xcorr(x, y, usevlines=True, maxlags=50, normed=True, lw=2)
        axis.grid(True)
        pyplot.title(sensor_id)
        pyplot.plot(dist, rssi, color=self._get_next_color(),lw=2, marker='o') #window=pyplot.window_hanning)
        return
        
    def _get_next_color(self):
        return next(self._colors)
    

#GUI Application
obj = SensorCalibrationGUI()
obj.show()

