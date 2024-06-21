########################################################################
#
#  written by He Zeng  #add 21 methods
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

class NoInit4Direction(EnumMeta):
    def __call__(cls, *args, **kwargs):
        raise TypeError("Cannot instantiate 'Direction'")

class Direction(Enum, metaclass=NoInit4Direction):
    EAST = 0
    NORTH = 2
    WEST = 4
    SOUTH = 6
    NORTH_EAST = 1
    NORTH_WEST = 3
    SOUTH_WEST = 5
    SOUTH_EAST = 7
    CENTER = 8
    EAST_WEST = 9
    NORTH_SOUTH = 10
    ANY = 11 
    NONE = 12
    
    # already been tested.
    def containsComponent(self, dir):
        if dir not in [Direction.CENTER, Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            raise ValueError(f"Invalid argument'{dir}' for this 'containsComponent' method")
        if dir.value ==0:
            return self.value in [0,1,7,9,11]      
        if dir.value ==2:
            return self.value in [1,2,3,10,11]
        if dir.value ==4:
            return self.value in [3,4,5,9,11]
        if dir.value ==6:
            return self.value in [5,6,7,10,11]
        if dir.value ==8:
            return self.value in [8,11]
    # already been tested.
    def extend(self):
        if self == Direction.NORTH or self == Direction.SOUTH:
            return Direction.NORTH_SOUTH
        elif self == Direction.EAST or self == Direction.WEST:
            return Direction.EAST_WEST
        else:
            raise ValueError(f"Invalid direction '{self.name}', the direction for 'extend' method should be one of Direction.NORTH, Direction.SOUTH,  Direction.EAST, Direction.WEST")
    
    def getJustifiedDir(self, justify):
        if justify not in [Direction.EAST, Direction.WEST]:
            raise ValueError(f"Invalid argument '{justify.name}', the parameter passed to the method should be either Direction.EAST or Direction.WEST")
        if not self.isPrimary():
            raise ValueError(f"Invalid direction '{self.name}', it should be one of [Direction.NORTH, Direction.SOUTH,  Direction.EAST, Direction.WEST]")
        if justify == Direction.EAST: 
            return self.rotate270()    
        elif justify == Direction.WEST:     
             return self.rotate90() 
                    
    # already been tested.   
    @staticmethod
    def getMembers():
        return list(Direction)
        
    # already been tested.
    def getPrimaryDirs(self):
        if self in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            return [self]
        elif self == Direction.NORTH_SOUTH:
            return [Direction.NORTH, Direction.SOUTH]
        elif self == Direction.EAST_WEST:
            return [Direction.EAST, Direction.WEST]
        elif self == Direction.SOUTH_EAST:
            return [Direction.EAST, Direction.SOUTH]
        elif self == Direction.SOUTH_WEST:
            return [Direction.WEST, Direction.SOUTH]
        elif self == Direction.NORTH_EAST:
            return [Direction.EAST, Direction.NORTH]
        elif self == Direction.NORTH_WEST:
            return [Direction.WEST, Direction.NORTH]
        elif self == Direction.ANY:
            return [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
        elif self == Direction.NONE or self == Direction.CENTER:
            return None
        else:
            raise ValueError(f"Invalid direction '{self.name}' for this 'getPrimaryDirs' method ")
    # already been tested.
    def is1Dimension(self):
        return self in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST, Direction.EAST_WEST, Direction.NORTH_SOUTH]
    # already been tested.
    def isHalfLine(self):
        return self in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST, Direction.NORTH_EAST, Direction.NORTH_WEST, Direction.SOUTH_EAST, Direction.SOUTH_WEST]
    # already been tested.
    def isFullLine(self):
        return self in [Direction.EAST_WEST, Direction.NORTH_SOUTH]
    # already been tested.
    def isPrimary(self):
        return self in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
    # already been tested.
    def isXDir(self):
        return self in [Direction.EAST, Direction.WEST, Direction.EAST_WEST]
    # already been tested.
    def isYDir(self):
        return self in [Direction.NORTH, Direction.SOUTH, Direction.NORTH_SOUTH]
    # already been tested.
    def mapXDirToYDir(self):
        xToYmapping = {Direction.EAST: Direction.NORTH, Direction.WEST: Direction.SOUTH,  Direction.EAST_WEST: Direction.NORTH_SOUTH}
        if self.isXDir():
            return xToYmapping[self]
        else:
             raise ValueError(f"Invalid direction '{self.name}', this 'mapXDirToYDir' method is only applicable for the X-axis.")  
    # already been tested.
    def mapYDirToXDir(self):
        yToXmapping = {Direction.NORTH: Direction.EAST, Direction.SOUTH: Direction.WEST, Direction.NORTH_SOUTH: Direction.EAST_WEST}
        if self.isYDir():
            return yToXmapping[self]
        else:
            raise ValueError(f"Invalid direction '{self.name}', this 'mapYDirToXDir' method is only applicable for the Y-axis.")

    # already been tested.
    def mirrorX(self):
        if self.value in range(8, 13):
            return self
        mirrorXmapping = {Direction.EAST: Direction.EAST, Direction.WEST: Direction.WEST,Direction.NORTH: Direction.SOUTH,Direction.SOUTH: Direction.NORTH, 
                          Direction.NORTH_EAST: Direction.SOUTH_EAST, Direction.NORTH_WEST: Direction.SOUTH_WEST, Direction.SOUTH_EAST: Direction.NORTH_EAST,
                          Direction.SOUTH_WEST: Direction.NORTH_WEST}
        if self in mirrorXmapping:
            return mirrorXmapping[self]
        else:
            raise ValueError(f"Invalid direction '{self.name}' for this 'mirrorX' method ")
    
    
    # already been tested.    
    def mirrorY(self):
        if self.value in range(8, 13):
            return self
        mirrorYmapping = {Direction.EAST: Direction.WEST ,Direction.WEST: Direction.EAST, Direction.NORTH: Direction.NORTH, Direction.SOUTH: Direction.SOUTH,
                          Direction.NORTH_EAST: Direction.NORTH_WEST, Direction.NORTH_WEST: Direction.NORTH_EAST, Direction.SOUTH_EAST: Direction.SOUTH_WEST,
                          Direction.SOUTH_WEST: Direction.SOUTH_EAST}
        if self in mirrorYmapping:
            return mirrorYmapping[self]
        else:
   
            raise ValueError(f"Invalid direction '{self.name}' for this 'mirrorY' method")
    # already been tested.
    def opposite(self):
        if not self.isHalfLine():
            raise ValueError(f"Invalid direction '{self.name}', this 'opposite' method is only applicable to half-line directions.")
        oppositeValue = (self.value + 4) % 8
        for member in Direction.__members__.values():
            if member.value == oppositeValue:
                return member
    # already been tested.      
    def perpendicular(self):
        if self.isXDir():
           return Direction.NORTH_SOUTH
        elif self.isYDir():
            return Direction.EAST_WEST 
        else:
            raise ValueError(f"Invalid direction '{self.name}', this 'perpendicular' method is only applicable to X-axis or Y-axis.")
    # already been tested.  
    def rotate90(self):
        if not self.isHalfLine():
            raise ValueError(f"Invalid direction '{self.name}', this 'rotate90' method is only applicable to half-line directions.")
        r90value = (self.value + 2) % 8
        for member in Direction.__members__.values():
            if member.value == r90value:
                return member
    # already been tested.  
    def rotate180(self):
        if not self.isHalfLine():
            raise ValueError(f"Invalid direction '{self.name}', this 'rotate180' method is only applicable to half-line directions.")
        r180value = (self.value + 4) % 8
        for member in Direction.__members__.values():
            if member.value == r180value:
                return member
    # already been tested. 
    def rotate270(self):
        if not self.isHalfLine():
            raise ValueError(f"Invalid direction '{self.name}', this 'rotate270' method is only applicable to half-line directions.")
        r270value = (self.value + 6) % 8
        for member in Direction.__members__.values():
            if member.value == r270value:
                return member
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
   
                
NORTH = Direction.NORTH
SOUTH = Direction.SOUTH
EAST = Direction.EAST
WEST = Direction.WEST
NORTH_WEST = Direction.NORTH_WEST
NORTH_EAST = Direction.NORTH_EAST
NORTH_SOUTH = Direction.NORTH_SOUTH
SOUTH_EAST = Direction.SOUTH_EAST
SOUTH_WEST = Direction.SOUTH_WEST
CENTER = Direction.CENTER
EAST_WEST = Direction.EAST_WEST
ANY = Direction.ANY
NONE = Direction.NONE


