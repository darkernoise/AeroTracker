'''
Created on May 26, 2016

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

import math
import datetime
import time
from aero_tracker.network.mac_address import MacAddress

class BLE_Packet:
    '''Each BLE Packet is filled with details about the tracked item.
    '''
    
    DELIMITER = "|"
    PACKET_FIELD_CNT = 10
    
    # Advertisment event types
    ADV_IND=0x00
    ADV_DIRECT_IND=0x01
    ADV_SCAN_IND=0x02
    ADV_NONCONN_IND=0x03
    ADV_SCAN_RSP=0x04
    
    
    mac_address = ""
    udid = ""
    major = 0
    minor = 0
    rssi = 0
    tx_power = 0
    adv_type = -1
    packet_number = 0
    sensor_id = ""
    packet_timestamp = None
    _distance = 0.0
    
    ##############################
    # Public Methods
    ##############################
    @staticmethod
    def advTypeToStr(advType):
        if (advType == BLE_Packet.ADV_SCAN_RSP):
            return "ADV_SCAN_RSP"
        elif (advType == BLE_Packet.ADV_SCAN_IND):
            return "ADV_SCAN_IND"
        elif (advType == BLE_Packet.ADV_DIRECT_IND):
            return "ADV_DIRECT_IND"
        elif (advType == BLE_Packet.ADV_NONCONN_IND):
            return "ADV_NONCONN_IND"
        else:
            return "ADV_IND"
    
    @staticmethod
    def objFromCSV(csv):
        vals = csv.split(BLE_Packet.DELIMITER)
        #Check to ensure there are the correct number of values
        if (len(vals) != BLE_Packet.PACKET_FIELD_CNT):
            ex = Exception("Invalid CSV length or incomplete CSV.")
            raise ex
#         mac_address = vals[0][0:2] + ":" + vals[0][2:4] + ":" + vals[0][4:6] + ":" + vals[0][6:8] + ":" + vals[0][8:9] + ":" + vals[0][9:10]
        mac_address = vals[0]
        try:
            pkt = BLE_Packet(mac_address=mac_address, udid=vals[1], major=int(vals[2]), minor=int(vals[3]), rssi=int(vals[5]), \
                          tx_power=int(vals[4]), adv_type=int(vals[6]), packet_number=int(vals[7]), sensor_id=vals[8], \
                          packet_timestamp=float(vals[9]), distance=float(vals[10]))
            return pkt
        except Exception as ex:
            print("Exception in ble_packet.objFromCSV: ", ex)
            raise
            pass
        return
    
    @property
    def target_id(self):
        '''
        Unique ID used to identify a target.
        '''
#         return self.udid
        return self.mac_address
    
    def toCSV(self):
        '''
        CSV format data
        '''
        rslt = MacAddress.unformat_mac_address(self.mac_address) + \
            self.DELIMITER + \
            self.udid + \
            self.DELIMITER + \
            str(self.major) + \
            self.DELIMITER + \
            str(self.minor) + \
            self.DELIMITER + \
            str(self.tx_power) + \
            self.DELIMITER + \
            str(self.rssi) + \
            self.DELIMITER + \
            str(self.adv_type) + \
            self.DELIMITER + \
            str(self.packet_number) + \
            self.DELIMITER + \
            self.sensor_id + \
            self.DELIMITER + \
            str(self.packet_timestamp) + \
            self.DELIMITER + \
            str(self.distance)
        return rslt
    
    @property
    def distance(self):
        '''
        Returns a distance property.
        '''
        return self._distance
    
    
    ##############################
    # Private Methods
    ##############################
    def __init__(self, mac_address="", udid="", major=0, minor=0, rssi=0, tx_power=1, \
                 adv_type=-1, packet_number=0, sensor_id="", packet_timestamp=0.0, distance:float=0.0):
        if (packet_timestamp == 0.0):
            self.packet_timestamp = time.time() #Record the time of the packet creation
        else:
            self.packet_timestamp = packet_timestamp
        self.sensor_id = sensor_id
        self.mac_address = mac_address
        self.udid = udid
        self.major = major
        self.minor = minor
        if (isinstance(rssi, tuple)):
            self.rssi = rssi[0]
        elif (isinstance(rssi, str)):
            self.rssi = int(rssi)
        else:
            self.rssi = rssi
        if (isinstance(tx_power, tuple)):
            self.tx_power = tx_power[0]
        else:
            self.tx_power = tx_power
        self.adv_type = adv_type
        self.packet_number = packet_number
        self._distance = distance
        return
    
    def __str__(self):
        return \
            "SID: " + self.sensor_id + " " \
            "Dist: " + "{0:.2f}".format(self.distance) + " " + \
            "RSSI: " + str(self.rssi) + " " + \
            "TxPwr: " + str(self.tx_power) + " " + \
            "Pkt#: " + str(self.packet_number) + " " + \
            "Mac: " + MacAddress.format_mac_address(self.mac_address) + " " + \
            "UUID: " + self.udid + " " + \
            "Maj: " + str(self.major) + " " + \
            "Min: " + str(self.minor) + " " + \
            "AdvTy : " + BLE_Packet.advTypeToStr(self.adv_type) + " " + \
            "TS: " + datetime.datetime.fromtimestamp(self.packet_timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
            
        
    def __eq__(self, other):
        try:
            if (self.udid != other.udid):
                return False
            if (self.mac_address != other.mac_address):
                return False
            if (self.major != other.major):
                return False
            if (self.minor != other.minor):
                return False
            if (self.rssi != other.rssi):
                return False
            if (self.tx_power != other.tx_power):
                return False
        except:
            return False
        