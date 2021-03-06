'''
Created on Aug 14, 2016

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
import typing
from aero_tracker.sensor.sensor_device import SensorDevice
from aero_tracker.trilateration.time_slice import TimeSlice
from aero_tracker.trilateration.raw_data.ts_queue_item import TSQueueItemSensor

class AT_Protocol(object):
    '''
    Defines communication command and response protocols for clients and servers.
    '''
    
    CMD_STATUS_FAIL = 0
    CMD_STATUS_SUCCESS = 1
    CMD_STATUS_WARNING = 4
    
    COMMAND_ID = '&'
    COMMAND_DELIMITER = '#'
    COMMAND_TERMINATOR = '\n'
    
    RESPONSE_DELIMITER = '$'
    RESPONSE_TERMINATOR = '\n'
    
    DATA_DELIMITIER = '|'
    DATA_TERMINATOR = '?'
    LINE_BREAK      = '%'
    ENCODING = 'ascii'
    
    
    @staticmethod
    def raw_data_packet(sensor_id:str, target_id:str, filter_dat:float, raw_dat:float, timestamp:float):
        return target_id + \
            AT_Protocol.DATA_DELIMITIER + \
            str(filter_dat) + \
            AT_Protocol.DATA_DELIMITIER + \
            str(raw_dat) + \
            AT_Protocol.DATA_DELIMITIER + \
            str(timestamp) + \
            AT_Protocol.DATA_TERMINATOR
    
    @staticmethod
    def delimit_data_listeners(data_listeners, delimiter):
        rval = ""
        for lstnr in data_listeners:
            rval += delimiter
            rval += lstnr
        return rval

    @staticmethod
    def format_data_listener(display_name, client_address, port):
        '''
        data listeners in the form[display_name@client_ip:port]
        '''
        return display_name + '@' + client_address + ':' + port
    
    @staticmethod
    def sensor_cluster_id_bytes(target_id:str, cluster_id:str):
        rval = AT_Protocol.COMMAND_ID + \
        AT_Protocol.DATA_DELIMITIER + \
        target_id + \
        AT_Protocol.DATA_DELIMITIER + \
        cluster_id
        rval += AT_Protocol.DATA_TERMINATOR + AT_Protocol.LINE_BREAK
        return rval.encode(AT_Protocol.ENCODING)
    
    @staticmethod
    def bytes_to_sensor_cluster_id(data_bytes:str):
        data_bytes_fltr = data_bytes[0:-1]
        parts = data_bytes_fltr.split(sep=AT_Protocol.DATA_DELIMITIER)
        command_id = parts[0]
        target_id = parts[1]
        cluster_id = parts[2]
        return command_id, target_id, cluster_id
    
    @staticmethod
    def sorted_data_bytes(time_slice:TimeSlice, tsq_sensors:typing.List[TSQueueItemSensor]):
        '''
        Converts sorted data into bytes for transmission.
        '''
        rval = str(time_slice.sort_key)
        for snsr in tsq_sensors:
            for dpkt in snsr.data_pkts:
                rval = rval + AT_Protocol.DATA_DELIMITIER + dpkt.sensor_id + AT_Protocol.DATA_DELIMITIER + str(dpkt.filter_dist)
        rval += AT_Protocol.DATA_TERMINATOR + AT_Protocol.LINE_BREAK
        return rval.encode(AT_Protocol.ENCODING)
    
    @staticmethod
    def bytes_to_sorted_data(data_bytes:str):
        '''
        Converts sorted data bytes back into sorted data elements.
        
        Note: data_bytes is already converted back to a string.
        '''
        time_slice_sort_key = 0.0
        sensor_vals = []
        sensor_id = None
#         last_sensor_id = None
#         last_sensor_index = -1
        
        data_bytes_fltr = data_bytes[0:-1]
        parts = data_bytes_fltr.split(sep=AT_Protocol.DATA_DELIMITIER)
        for i in range(0, len(parts)):
            prt = parts[i]
            if (i == 0):
                time_slice_sort_key = float(prt)
            else:
                if (sensor_id == None):
                    sensor_id = prt
                else:
                    sensor_vals.append([sensor_id, float(prt)])
                    sensor_id = None
        return time_slice_sort_key, sensor_vals
        
        

    def __init__(self, params):
        '''
        Constructor
        '''
        return
    

        