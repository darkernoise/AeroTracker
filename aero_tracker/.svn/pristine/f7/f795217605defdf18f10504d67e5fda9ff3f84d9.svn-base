'''
Created on Jun 15, 2016

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

class SphereCoordinates(object):
    '''
    Coordinates of a sphere in 3D space.
    '''
    X = 0
    Y = 0
    Z = 0
    R = 0 #Radius
    D = 0 #Differential rate of reading
    Name = ""
    _vect_distance = None
    
    @staticmethod
    def from_vector(v, Differential=0, Name=""):
        return SphereCoordinates(v[0], v[1], v[2], np.linalg.norm(v), Differential, Name)
    
    def get_coordinates_list(self):
        lst = []
        lst.append(self.X)
        lst.append(self.Y)
        lst.append(self.Z)
        return lst
    
    def get_coordinates_array(self):
        return np.array([self.X, self.Y, self.Z])
    
    def get_vector_distance(self):
        if (self._vect_distance == None):
            self._vect_distance = np.sqrt(np.square(self.X) + np.square(self.Y) + np.square(self.Z))
        return self._vect_distance 

    def __init__(self, X, Y, Z, Radius, Differential=0, Name=""):
        '''
        Constructor
        '''
        self.X = X
        self.Y = Y
        self.Z = Z
        self.R = Radius
        self.D = Differential
        self.Name = Name
        