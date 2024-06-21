
########################################################################
#
#  written by He Zeng  #add 7 methods 
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


from enum import Enum,EnumMeta
from cni.dlo.transform import *

class NoInit4Location(EnumMeta):
    def __call__(cls, *args, **kwargs):
        raise TypeError("Cannot instantiate 'Location'")

class Location(Enum, metaclass=NoInit4Location):
    LOWER_LEFT = "LOWER_LEFT"
    CENTER_LEFT = "CENTER_LEFT"
    UPPER_LEFT = "UPPER_LEFT"
    LOWER_CENTER = "LOWER_CENTER"
    CENTER_CENTER = "CENTER_CENTER"
    UPPER_CENTER = "UPPER_CENTER"
    LOWER_RIGHT = "LOWER_RIGHT"
    CENTER_RIGHT = "CENTER_RIGHT"
    UPPER_RIGHT = "UPPER_RIGHT"
  
    def __str__(self): 
        return f"Location.{self.value}"
        
    # already been tested.
    def mirrorX(self):
        mXMapping = {Location.LOWER_LEFT: Location.UPPER_LEFT, Location.UPPER_LEFT: Location.LOWER_LEFT,
                    Location.LOWER_CENTER: Location.UPPER_CENTER, Location.UPPER_CENTER: Location.LOWER_CENTER,
                    Location.LOWER_RIGHT: Location.UPPER_RIGHT, Location.UPPER_RIGHT: Location.LOWER_RIGHT}
        return mXMapping.get(self, self) 

    # already been tested.
    def mirrorY(self):
        mYMapping = {Location.LOWER_LEFT: Location.LOWER_RIGHT, Location.LOWER_RIGHT: Location.LOWER_LEFT,
                    Location.CENTER_LEFT: Location.CENTER_RIGHT, Location.CENTER_RIGHT: Location.CENTER_LEFT,
                    Location.UPPER_LEFT: Location.UPPER_RIGHT, Location.UPPER_RIGHT: Location.UPPER_LEFT}
        return mYMapping.get(self, self)

    # already been tested.
    def rotate90(self):
        r90Mapping = {Location.LOWER_LEFT: Location.LOWER_RIGHT, Location.CENTER_LEFT: Location.LOWER_CENTER,
                      Location.UPPER_LEFT: Location.LOWER_LEFT, Location.LOWER_CENTER: Location.CENTER_RIGHT,
                      Location.UPPER_CENTER: Location.CENTER_LEFT, Location.LOWER_RIGHT: Location.UPPER_RIGHT, 
                      Location.CENTER_RIGHT: Location.UPPER_CENTER, Location.UPPER_RIGHT: Location.UPPER_LEFT}
        return r90Mapping.get(self, self) 
    
    # already been tested.
    def rotate180(self):
        r180Mapping = {Location.LOWER_LEFT: Location.UPPER_RIGHT, Location.CENTER_LEFT: Location.CENTER_RIGHT,
                       Location.UPPER_LEFT: Location.LOWER_RIGHT, Location.LOWER_CENTER: Location.UPPER_CENTER,
                       Location.UPPER_CENTER: Location.LOWER_CENTER, Location.LOWER_RIGHT: Location.UPPER_LEFT,
                        Location.CENTER_RIGHT: Location.CENTER_LEFT, Location.UPPER_RIGHT: Location.LOWER_LEFT}
        return r180Mapping.get(self, self)
    # already been tested.
    def rotate270(self):
        r270mapping = {Location.LOWER_LEFT: Location.UPPER_LEFT, Location.CENTER_LEFT: Location.UPPER_CENTER,
                        Location.UPPER_LEFT: Location.UPPER_RIGHT, Location.LOWER_CENTER: Location.CENTER_LEFT,
                        Location.UPPER_CENTER: Location.CENTER_RIGHT, Location.LOWER_RIGHT: Location.LOWER_LEFT, 
                        Location.CENTER_RIGHT: Location.LOWER_CENTER, Location.UPPER_RIGHT: Location.LOWER_RIGHT}
        return r270mapping.get(self, self)
    # already been tested.
    def transform(self, trans):
        if not isinstance(trans, Transform):
            raise ValueError(f"Invalid transform '{trans}', the argument passed in must be an object of Transform")
        if trans.orientation == Orientation.R90:
            return self.rotate90()
        elif trans.orientation == Orientation.R180:
            return self.rotate180()
        elif trans.orientation == Orientation.R270:
            return self.rotate270()
        elif trans.orientation == Orientation.MX:
            return self.mirrorX()
        elif trans.orientation == Orientation.MY:
            return self.mirrorY()
        elif trans.orientation == Orientation.MYR90:
            return self.mirrorY().rotate90()  
        elif trans.orientation == Orientation.MXR90: 
            return self.mirrorX().rotate90()  
  

LOWER_LEFT = Location.LOWER_LEFT
CENTER_LEFT = Location.CENTER_LEFT
UPPER_LEFT = Location.UPPER_LEFT
LOWER_CENTER = Location.LOWER_CENTER
CENTER_CENTER = Location.CENTER_CENTER
UPPER_CENTER = Location.UPPER_CENTER
LOWER_RIGHT = Location.LOWER_RIGHT
CENTER_RIGHT = Location.CENTER_RIGHT
UPPER_RIGHT = Location.UPPER_RIGHT



