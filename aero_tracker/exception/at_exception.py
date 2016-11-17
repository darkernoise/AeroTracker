'''
Created on Jul 30, 2016

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

class AT_Exception(Exception):
    '''
    Standard PLane Tracker Exception.
    '''
    source = ""
    method = ""
    message = ""
    details = ""

    def __init__(self, source, method, message, details=""):
        '''
        Constructor
        '''
        if (type(source) is str):
            self.source = source
        else:
            self.source = type(source)
        self.method = method
        self.message = message
        self.details = details
        