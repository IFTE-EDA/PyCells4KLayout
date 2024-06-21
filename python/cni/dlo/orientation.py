########################################################################
#
#  written by He.Zeng  #add 2 methods and a dictionary
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


import pya

from enum import Enum

class Orientation(Enum):
    R0 = 0
    R90 = 1
    R180 = 2
    R270 = 3
    MY = 4  
    MX = 5
    MYR90= 6
    MXR90= 7 
    
    # already been tested.  
    def concat(self, otherorient):
        if type(self) is not type(otherorient):
            raise TypeError("The passed argument must be an instance of Orientation")
        if self == Orientation.R0 or otherorient == Orientation.R0:
            return Orientation(self.value + otherorient.value)
        if self.value < 4 and otherorient.value < 4:
            newValue = (self.value + otherorient.value) % 4
            return Orientation(newValue)
        orientConcatMapping = {
            (Orientation.R90, Orientation.MY): Orientation.MXR90,
            (Orientation.R90, Orientation.MX): Orientation.MYR90,
            (Orientation.R90, Orientation.MYR90): Orientation.MY,
            (Orientation.R90, Orientation.MXR90): Orientation.MX,

            (Orientation.R180, Orientation.MY): Orientation.MX,
            (Orientation.R180, Orientation.MX): Orientation.MY,
            (Orientation.R180, Orientation.MYR90): Orientation.MXR90,
            (Orientation.R180, Orientation.MXR90): Orientation.MYR90,

            (Orientation.R270, Orientation.MY): Orientation.MYR90,
            (Orientation.R270, Orientation.MX): Orientation.MXR90,
            (Orientation.R270, Orientation.MYR90): Orientation.MX,
            (Orientation.R270, Orientation.MXR90): Orientation.MY,

            (Orientation.MX, Orientation.R90): Orientation.MXR90,
            (Orientation.MX, Orientation.R180): Orientation.MY,
            (Orientation.MX, Orientation.R270): Orientation.MYR90,
            (Orientation.MX, Orientation.MY): Orientation.R180,
            (Orientation.MX, Orientation.MX): Orientation.R0,
            (Orientation.MX, Orientation.MYR90): Orientation.R270,
            (Orientation.MX, Orientation.MXR90): Orientation.R90,

            (Orientation.MY, Orientation.R90): Orientation.MYR90,
            (Orientation.MY, Orientation.R180): Orientation.MX,
            (Orientation.MY, Orientation.R270): Orientation.MXR90,
            (Orientation.MY, Orientation.MY): Orientation.R0,
            (Orientation.MY, Orientation.MX): Orientation.R180,
            (Orientation.MY, Orientation.MYR90): Orientation.R90,
            (Orientation.MY, Orientation.MXR90): Orientation.R270,

            (Orientation.MYR90, Orientation.R90): Orientation.MX,
            (Orientation.MYR90, Orientation.R180): Orientation.MXR90,
            (Orientation.MYR90, Orientation.R270): Orientation.MY,
            (Orientation.MYR90, Orientation.MY): Orientation.R270,
            (Orientation.MYR90, Orientation.MX): Orientation.R90,
            (Orientation.MYR90, Orientation.MYR90): Orientation.R0,
            (Orientation.MYR90, Orientation.MXR90): Orientation.R180,

            (Orientation.MXR90, Orientation.R90): Orientation.MY,
            (Orientation.MXR90, Orientation.R180): Orientation.MYR90,
            (Orientation.MXR90, Orientation.R270): Orientation.MX,
            (Orientation.MXR90, Orientation.MY): Orientation.R90,
            (Orientation.MXR90, Orientation.MX): Orientation.R270,
            (Orientation.MXR90, Orientation.MYR90): Orientation.R180,
            (Orientation.MXR90, Orientation.MXR90): Orientation.R0}
        return orientConcatMapping.get((self, otherorient))

    # already been tested.  
    def getRelativeOrient(self, otherorient):
        if not isinstance(otherorient, Orientation):
            raise TypeError("The passed argument must be an instance of Orientation")
        if self == Orientation.R0:
            return otherorient
        if otherorient == Orientation.R0:
            return self    
        if self.value == otherorient.value:
            return Orientation.R0
        if self.value < 4 and otherorient.value < 4:
            newValue = (otherorient.value - self.value ) % 4
            return Orientation(newValue)
        orientRelativeMapping = {
            (Orientation.R90, Orientation.MY): Orientation.MXR90,
            (Orientation.R90, Orientation.MX): Orientation.MYR90,
            (Orientation.R90, Orientation.MYR90): Orientation.MX,
            (Orientation.R90, Orientation.MXR90): Orientation.MY,
        
            (Orientation.R180, Orientation.MY): Orientation.MX,
            (Orientation.R180, Orientation.MX): Orientation.MY,
            (Orientation.R180, Orientation.MYR90): Orientation.MXR90,
            (Orientation.R180, Orientation.MXR90): Orientation.MYR90,
        
            (Orientation.R270, Orientation.MY): Orientation.MYR90,
            (Orientation.R270, Orientation.MX): Orientation.MXR90,
            (Orientation.R270, Orientation.MYR90): Orientation.MY,
            (Orientation.R270, Orientation.MXR90): Orientation.MX,
            
            (Orientation.MX, Orientation.R90): Orientation.MXR90,
            (Orientation.MX, Orientation.R180): Orientation.MY,
            (Orientation.MX, Orientation.R270): Orientation.MYR90,
            (Orientation.MX, Orientation.MY): Orientation.R180,
            (Orientation.MX, Orientation.MYR90): Orientation.R270,
            (Orientation.MX, Orientation.MXR90): Orientation.R90,
        
            (Orientation.MY, Orientation.R90): Orientation.MYR90,
            (Orientation.MY, Orientation.R180): Orientation.MX,
            (Orientation.MY, Orientation.R270): Orientation.MXR90,
            (Orientation.MY, Orientation.MX): Orientation.R180,
            (Orientation.MY, Orientation.MYR90): Orientation.R90,
            (Orientation.MY, Orientation.MXR90): Orientation.R270,
        
            (Orientation.MYR90, Orientation.R90): Orientation.MX,
            (Orientation.MYR90, Orientation.R180): Orientation.MXR90,
            (Orientation.MYR90, Orientation.R270): Orientation.MY,
            (Orientation.MYR90, Orientation.MX): Orientation.R90,
            (Orientation.MYR90, Orientation.MY): Orientation.R270,
            (Orientation.MYR90, Orientation.MXR90): Orientation.R180,
        
            (Orientation.MXR90, Orientation.R90): Orientation.MY,
            (Orientation.MXR90, Orientation.R180): Orientation.MYR90,
            (Orientation.MXR90, Orientation.R270): Orientation.MX,
            (Orientation.MXR90, Orientation.MY): Orientation.R90,
            (Orientation.MXR90, Orientation.MX): Orientation.R270,
            (Orientation.MXR90, Orientation.MYR90): Orientation.R180}
        return orientRelativeMapping.get((self, otherorient))

orientMapping = {
    Orientation.R0.value: pya.DTrans.R0,
    Orientation.R90.value: pya.DTrans.R90,
    Orientation.R180.value: pya.DTrans.R180,
    Orientation.R270.value: pya.DTrans.R270,
    Orientation.MY.value: pya.DTrans.M90,
    Orientation.MX.value: pya.DTrans.M0,
    Orientation.MYR90.value:pya.DTrans.R90 * pya.DTrans.M90,
    Orientation.MXR90.value: pya.DTrans.R90 * pya.DTrans.M0}
   
R0 = Orientation.R0
R90 = Orientation.R90
R180 = Orientation.R180
R270 = Orientation.R270
MY = Orientation.MY
MX = Orientation.MX
MYR90 = Orientation.MYR90
MXR90 = Orientation.MXR90  



