########################################################################
#
#  written and verified by He.Zeng  #add 6 methods 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################

from enum import Enum
import math

class SnapType(Enum):
    CEIL = "ceil"
    FLOOR = "floor"
    ROUND = "round"
    TRUNC = "trunc"
    ROUND_CEIL = "round_ceil"


    #already been tested. 
    @staticmethod
    def ceil(size, value):
        return math.ceil(value / size) * size
        
    #already been tested. 
    @staticmethod
    def floor(size, value):
        return math.floor(value / size) * size
        
    #already been tested. 
    @staticmethod
    def round(size, value):
        return round(value / size) * size
   
    #already been tested.   
    @staticmethod 
    def round_ceil(size, value):
        if value % size == 0: 
            return value
        ceilValue = SnapType.ceil(size, value)
        floorValue = SnapType.floor(size, value)
        if abs(ceilValue - value) == abs(value - floorValue): 
            return max(ceil_val, floor_val)
        else:
            return ceilValue if abs(ceilValue - value) < abs(value - floorValue) else floorValue
    
    #already been tested.   
    @staticmethod
    def trunc(size, value):
        return math.trunc(value / size) * size
     
    #already been tested. 
    @staticmethod
    def snap(snaptype, size, value):
        if snaptype.value == SnapType.CEIL.value:
            return SnapType.ceil(size, value)
        elif snaptype.value == SnapType.FLOOR.value:
            return SnapType.floor(size, value)
        elif snaptype.value == SnapType.ROUND.value:
            return SnapType.round(size, value)
        elif snaptype.value == SnapType.TRUNC.value:
            return SnapType.trunc(size, value)
        elif snaptype.value == SnapType.ROUND_CEIL.value:
            return SnapType.round_ceil(size, value)
        


