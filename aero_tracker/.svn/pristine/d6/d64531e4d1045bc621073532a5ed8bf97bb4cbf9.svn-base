'''
Created on Aug 26, 2016

@author: Joel Blackthorne

Lists all nearby bluetooth devices.
'''

import bluetooth

nearby_devices = bluetooth.discover_devices(lookup_names = False)
for bdaddr in nearby_devices:
    print("addr: ", bdaddr)