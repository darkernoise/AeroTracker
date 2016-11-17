'''
Created on Sep 5, 2016

@author: Joel Blackthorne
'''

import numpy as np
import typing

class AT_Statistics(object):
    '''
    Optimized statistical calculations for data processing.
    '''

    @staticmethod
    def mad(dat_array):
        '''
        Median Average Deviation
        
        Returns:
            * Median value of array
            * MAD calculated value
            * Sorted NP type array
        '''
        if (isinstance(obj=dat_array, class_or_tuple=typing.List)):
            dat_array = np.array(dat_array) #convert to numpy array
        np.sort(dat_array)
        med = np.median(dat_array)
        calc_array = (dat_array - med)
        mad_val = np.average(a=calc_array)
        return med, mad_val, dat_array
    