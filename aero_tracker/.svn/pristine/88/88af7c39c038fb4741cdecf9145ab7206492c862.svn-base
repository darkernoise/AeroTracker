'''
Created on Sep 14, 2016

@author: Joel Blackthorne
'''

import sys

class LogDataSort(object):
    '''
    Sort the log data so that it can be loaded into a spreadsheet.
    
    Note: Run from the command line: python3.5 -m aero_tracker.data.log_data_sort <file name>
    '''
    
    WRITE_SENSOR_DB = False
    WRITE_LAP_NUM = True

    _source_file = ''
    BASE_ID = 'NP_BASE'
    SENSOR_A = 'NP_SE_A'
    SENSOR_B = 'NP_SE_B'
    SENSOR_C = 'NP_SE_C'
    SENSOR_D = 'NP_SE_D'
    SENSOR_E = 'NP_SE_E'
    SEPARATOR = ','
    _last_timestamp = 0.0
    _lap_num = 0

    def __init__(self, source_file):
        '''
        Constructor
        '''
        if (source_file == None):
            raise Exception('Source file parameter is missing')
        
        self._source_file = source_file
        self._process_file(source_file)
        
        return
    
    def _process_file(self, source_file):
        fl = open(source_file, "r");
        out_fl = open(source_file + ".sorted", "w")
        try:
            dat_raw = fl.read();
            dat_list = dat_raw.split("\n");
            for raw_line in dat_list:
                dat_line = raw_line
                if (len(dat_line) > 0):
                    sub_list = dat_line.split(': ')
                    if (len(sub_list) == 2):
                        dat_line = sub_list[1]
                
                if (len(dat_line) == 0):
                    pass
                elif (dat_line[0] == "#"):
                    pass
                elif (dat_line[0] == " "):
                    pass
                elif (dat_line[0] == "/"):
                    pass
                elif (dat_line[0:4] == "Data"):
                    pass
                elif (dat_line[0:6] == "Thread"):
                    pass
                elif (dat_line[0:4] == "DHCP"):
                    pass
                elif (dat_line[0:5] == "bound"):
                    pass
                elif (dat_line.find('socket') > 0):
                    pass
                else:
                    dat_vals = dat_line.split(",");
                    if (len(dat_vals) < 4):
                        pass
                    else:
                        self._process_dat_vals(dat_vals, out_fl)
        except Exception as ex:
            print(ex)
            fl.close()
            out_fl.close()
        return
    
    def _process_dat_vals(self, dat_vals, out_fl):
        #TimeStamp
        ts = dat_vals[0].replace('[','')
        if (ts.find('start') > 0):
            tst_vals = ts.split(': ')
            if (len(tst_vals) > 1):
                ts = tst_vals[1]

        if (self.WRITE_LAP_NUM):                
            try:
                tsf = float(ts)
                if ((tsf - self._last_timestamp) > 5):
                    #new lap
                    self._lap_num += 1
                self._last_timestamp = tsf
                out_fl.write(str(self._lap_num) + self.SEPARATOR)
            except:
                pass
        
                
        out_fl.write(ts + self.SEPARATOR)
        #XYZ
        out_fl.write(dat_vals[1].replace('[','') + self.SEPARATOR)
        out_fl.write(dat_vals[2] + self.SEPARATOR)
        
        z_val = dat_vals[3].replace(']','')
        tst_vals = z_val.split('Thread')
        if (len(tst_vals) > 1):
            z_val = tst_vals[0]
        out_fl.write(z_val)
        if (self.WRITE_SENSOR_DB):
            out_fl.write(self.SEPARATOR)
            out_fl.write(self.BASE_ID + self.SEPARATOR)
            out_fl.write(self._get_sensor_vals(sensor_id=self.BASE_ID, start_inx=4, dat_vals=dat_vals) + self.SEPARATOR)
            out_fl.write(self.SENSOR_A + self.SEPARATOR)
            out_fl.write(self._get_sensor_vals(sensor_id=self.SENSOR_A, start_inx=4, dat_vals=dat_vals) + self.SEPARATOR)
            out_fl.write(self.SENSOR_B + self.SEPARATOR)
            out_fl.write(self._get_sensor_vals(sensor_id=self.SENSOR_B, start_inx=4, dat_vals=dat_vals) + self.SEPARATOR)
            out_fl.write(self.SENSOR_C + self.SEPARATOR)
            out_fl.write(self._get_sensor_vals(sensor_id=self.SENSOR_C, start_inx=4, dat_vals=dat_vals) + self.SEPARATOR)
            out_fl.write(self.SENSOR_D + self.SEPARATOR)
            out_fl.write(self._get_sensor_vals(sensor_id=self.SENSOR_D, start_inx=4, dat_vals=dat_vals) + self.SEPARATOR)
            out_fl.write(self.SENSOR_E + self.SEPARATOR)
            out_fl.write(self._get_sensor_vals(sensor_id=self.SENSOR_E, start_inx=4, dat_vals=dat_vals) + self.SEPARATOR)
        out_fl.write('\n')
        return
    
    def _get_sensor_vals(self, sensor_id, start_inx, dat_vals):
        i = start_inx
        while (i < len(dat_vals)):
            if (dat_vals[i].strip() == sensor_id):
                return (dat_vals[i + 1]).strip()
            i += 1
        return ''
    
#Tester
if (len(sys.argv) == 2) or (len(sys.argv) == 5):
    obj = LogDataSort(sys.argv[len(sys.argv) - 1])
    print('Sorting complete')
    
else:
#     obj = LogDataSort('/home/midian/Documents/20161015 Golden Triangle/daemon.log')
    print('Pass the file name to sort as a parameter')

        
        