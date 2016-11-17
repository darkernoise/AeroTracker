'''
Created on Sep 13, 2016

@author: Joel Blackthorne
'''

class BLESetAdvertisingParameters(object):
    '''
    The LE_Set_Advertising_Parameters command is used by the Host to set the
    advertising parameters.
    The Advertising_Interval_Min shall be less than or equal to the
    Advertising_Interval_Max. The Advertising_Interval_Min and
    Advertising_Interval_Max should not be the same value to enable the Control-
    ler to determine the best advertising interval given other activities.
    For directed advertising, when Advertising_Type is 0x01 (ADV_DIRECT_IND),
    the Advertising_Interval_Min and Advertising_Interval_Max parameters are not
    used and shall be ignored.
    The Advertising_Type is used to determine the packet type that is used for
    advertising when advertising is enabled.
    The Advertising_Interval_Min and Advertising_Interval_Max shall not be set to
    less than 0x00A0 (100 ms) if the Advertising_Type is set to 0x02
    (ADV_SCAN_IND) or 0x03 (ADV_NONCONN_IND). The Own_Address_Type
    determines if the advertising packets are identified with the Public Device
    Address of the device, or a Random Device Address as written by the
    LE_Set_Random_Address command.
    If directed advertising is performed, then the Direct_Address_Type and
    Direct_Address shall be valid, otherwise they shall be ignored by the Controller
    and not used.
    The Advertising_Channel_Map is a bit field that indicates the advertising chan-
    nels that shall be used when transmitting advertising packets. At least one
    channel bit shall be set in the Advertising_Channel_Map parameter.
    The Advertising_Filter_Policy parameter shall be ignored when directed adver-
    tising is enabled.
    '''
    
    # Advertisement Types
    ADV_IND=0x00
    ADV_DIRECT_IND=0x01
    ADV_SCAN_IND=0x02
    ADV_NONCONN_IND=0x03
    ADV_SCAN_RSP=0x04
    
    ADDR_TYPE_PUBLIC = 0x00
    ADDR_TYPE_RANDOM = 0x01
    
    ADV_CHANNEL_MAP_37 = 0x01
    ADV_CHANNEL_MAP_38 = 0x02
    ADV_CHANNEL_MAP_39 = 0x04
    ADV_CHANNEL_MAP_ALL = 0x07
    
    _adv_int_min = 0 #Advertising_Interval_Min
    _adv_int_max = 0 #Advertising_Interval_Max
    _adv_type = 0 #Advertising Type
    _own_addr_type = 0 #Own Address Type
    _direct_addr_type = 0 #Direct Address Type
    _direct_addr = 0 #Direct Address
    _adv_channel_map = 0 #Advertising Channel Map
    _adv_filter_policy = 0 #Advertising filter policy
    
    def get_bytes(self):
        adv_min = self._be_hex_pad2(self._adv_int_min)
        adv_max = self._be_hex_pad2(self._adv_int_max)
        
        rval = adv_min
        self._pair_append(val=adv_max, dat_list=rval)
        rval.append(self._be_hex_pad1(self._adv_type))
        rval.append(self._be_hex_pad1(self._own_addr_type))
        rval.append(self._be_hex_pad1(self._direct_addr_type))
        self._pair_append(val=self._hex_address(addr=self._direct_addr), dat_list=rval)
        rval.append(self._be_hex_pad1(self._adv_channel_map))
        rval.append(self._be_hex_pad1(self._adv_filter_policy))
        return rval
    
    def _pair_append(self, val, dat_list):
        if (type(val) is list):
            for itm in val:
                dat_list.append(itm)
        elif (type(val) is str):
            sval = str(val)
            cnt = len(sval)
            i = 0
            while (i < cnt):
                pair = sval[i:i+2]
                dat_list.append(pair)
                i += 2
        return
    
    def _be_hex_pad1(self, val):
        return "%0.2X" % val
    
    def _be_hex_pad2(self, val):
        '''
        Big Endian hex padding
        '''
        str = "%0.4X" % val
        return [str[2:4], str[0:2]] #Result is big endian
    
    def _hex_address(self, addr):
        return "%0.12X" % addr

    def __init__(self, adv_int_min_ms=1000, 
        adv_int_max_ms=1024, 
        adv_type=0x00, 
        own_addr_type=0x00, 
        direct_addr_type=0x00, 
        direct_addr=0x000000000000, 
        adv_channel_map=0x07, 
        adv_filter_policy=0x00):
        '''
        Constructor
        '''
        self._adv_int_min = adv_int_min_ms
        self._adv_int_max = adv_int_max_ms
        self._adv_type = adv_type
        self._own_addr_type = own_addr_type
        self._direct_addr_type = direct_addr_type
        self._direct_addr = direct_addr
        self._adv_channel_map = adv_channel_map
        self._adv_filter_policy = adv_filter_policy
        return
        
# #Tester
# obj = BLESetAdvertisingParameters(adv_int_min_ms=20, 
#         adv_int_max_ms=20, 
#         adv_type=0x00, 
#         own_addr_type=0x00, 
#         direct_addr_type=0x00, 
#         direct_addr=0x185E0F90C2D3, 
#         adv_channel_map=0x07, 
#         adv_filter_policy=0x00)
# print(obj.get_bytes())
        