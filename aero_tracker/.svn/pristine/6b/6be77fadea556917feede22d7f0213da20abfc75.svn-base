'''
Created on Oct 29, 2016

@author: Joel Blackthorne
'''
import time
from aero_tracker.trilateration.time_slice import TimeSlice
from aero_tracker.network.at_sensor_data_packet import AT_SensorDataPacket
from aero_tracker.network.at_protocol import AT_Protocol
from aero_tracker.trilateration.raw_data.ts_queue_item import TSQueueItemSensor

#Tester
ts = TimeSlice(time_val=time.time(), sec_div=40)
tsq_sensors = []
target_id = 'target12123'
sensor_id = 'NP_SNSR_A'
dpkt = AT_SensorDataPacket(cluster_id='NP', sensor_id=sensor_id, target_id=target_id, 
    filter_dist=12.233, raw_dist=13.22, rssi=-32.2, timestamp=time.time())
snsrA = TSQueueItemSensor(sensor_id=sensor_id, data_pkt=dpkt)
sensor_id = 'NP_SNSR_B'
dpkt = AT_SensorDataPacket(cluster_id='NP', sensor_id=sensor_id, target_id=target_id, 
    filter_dist=12.233, raw_dist=13.22, rssi=-32.2, timestamp=time.time())
snsrB = TSQueueItemSensor(sensor_id=sensor_id, data_pkt=dpkt)
tsq_sensors.append(snsrA)
tsq_sensors.append(snsrB)

sorted_bytes=AT_Protocol.sorted_data_bytes(target_id=target_id, time_slice=ts, tsq_sensors=tsq_sensors)

tst_target_id, time_slice_sort_key, sensor_vals = AT_Protocol.bytes_to_sorted_data(data_bytes=sorted_bytes)

print(tst_target_id + ' : ' + str(time_slice_sort_key))
