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

import datetime
import os

class TargetDataLogger(object):
    '''
    Writes the filtered sensor target data to a log file for debugging purposes.
    '''
    SEPERATOR = '|'
    TERMINATOR = '\n'

    _log_directory = "/var/log/"
    _file_name = "target_log.log"
    _fl = None
    _max_write_lines = 1000
    _cnt = 0
    _closed = True
    
    def write(self, data_filered, data_raw, rssi, timestamp):
        if (not self._closed):
            ts = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            ln = str(data_filered) + \
                self.SEPERATOR + \
                str(data_raw) + \
                self.SEPERATOR + \
                str(rssi) + \
                self.SEPERATOR + \
                ts + \
                self.TERMINATOR
            self._fl.write(ln)
            self._cnt += 1
            if (self._cnt >= self._max_write_lines):
                self.close()
        return
    
    def close(self):
        try:
            self._fl.close()
            self._closed = True
        except:
            pass
        return

    def __init__(self, log_directory, file_name, max_write_lines=1000):
        '''
        Constructor
        '''
        self._log_directory = log_directory
        self._check_directory(log_directory)
        self._file_name = file_name
        self._fl = open(self._get_full_file_path(directory=self._log_directory, file_name=self._file_name), 'w')
        self._max_write_lines = max_write_lines
        self._closed = False
        return
    
    def __del__(self):
        self.close()
        return
    
    def _check_directory(self, log_directory):
        if (not os.path.isdir(log_directory)):
            os.makedirs(log_directory)
        return
    
    def _get_full_file_path(self, directory, file_name):
        #TODO - Make platform independent
        return directory + file_name
        