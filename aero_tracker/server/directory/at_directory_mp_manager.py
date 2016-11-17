'''
Created on Aug 16, 2016

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

class AT_DirectoryMPManager(BaseManager):
    '''
    Multiprocessing Manager to load custom types for directory services.
    '''

    @staticmethod
    def register_client_methods():
        AT_DirectoryMPManager.register(typeid='get_instance')
        return