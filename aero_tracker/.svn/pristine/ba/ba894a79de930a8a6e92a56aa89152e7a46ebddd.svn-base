'''
Created on Aug 27, 2016

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

from multiprocessing.managers import BaseManager

class AT_DataProcWorkerMPManager(BaseManager):
    '''
    Multi-process memory manager for a data processing server worker, which covers a single
    target.  This modules allows the separate processes to receiving target sensor
    data to queue and sort the data all in one place. 
    '''

    @staticmethod
    def register_client_methods():
        AT_DataProcWorkerMPManager.register(typeid='get_pipe_pool')
        return
    
        