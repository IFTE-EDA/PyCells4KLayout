########################################################################
#
# written by He.Zeng  #add 36 methods
# Note: The 'Range' class may cause naming conflicts with the 'range' function used in 'for' loops (e.g., 'for in range(8)') in KLayout
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



import sys
from cni.dlo.direction import *
from cni.dlo.gapstyle import *
class Range:
    def __init__(self, *args):
        if len(args) == 0:
            self._left = sys.maxsize
            self._right = -sys.maxsize - 1
        elif len(args) == 1 and isinstance(args[0], Range):
            self._left = args[0].left
            self._right = args[0].right
        elif len(args) == 2:
            self._left = args[0]
            self._right = args[1]
        else:
            raise ValueError("Invalid arguments")
            
    def __str__(self):
        return f"Range({self.left}, {self.right})"

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        self._right = value

 
    # already been tested.       
    def alignEdge(self, dir, refRange, refDir=None, offset=0):
        if dir not in [Direction.EAST, Direction.WEST, Direction.EAST_WEST]:
            raise ValueError("Invalid direction, the supported directions are: WEST, EAST, EAST_WEST")
        wdith = self.getWidth()
        if refDir is None or refDir == dir:
            if dir == Direction.EAST:
                self.right = refRange.right + offset
                self.left =  self.right -wdith    
            elif dir == Direction.WEST:
                self.left = refRange.left - offset
                self.right = self.left + wdith
            elif dir == Direction.EAST_WEST:
                self.left = refRange.left - offset / 2
                self.right = refRange.right + offset / 2
        return self
     
    # already been tested.                 
    def alignEdgeToCoord(self, dir, coord): 
        if dir == Direction.EAST:
            distance = coord - self.right
            self.moveBy(distance)
        elif dir == Direction.WEST:
            distance = coord - self.left
            self.moveBy(distance)
        elif dir == Direction.EAST_WEST:
            distance = coord - self.getCenter()
            self.moveBy(distance)
        else:
            raise ValueError("Invalid direction, the supported directions are: WEST, EAST, EAST_WEST")
        return self
              
    def compareTrueCenter(self):    
        raise ValueError("unimplemented yet")
    
    # already been tested.            
    def contains(self, range, incEnds=True):
        if incEnds:
            return self.left <= range.left and self.right >= range.right
        else:
            return self.left < range.left and self.right > range.right

    # already been tested.       
    def containsCoord(self, coord, incEnds=True):
        if incEnds:
            return self.left <= coord <= self.right
        else:
            return self.left < coord < self.right
    # already been tested.       
    def expand(self, expand):
        self.left -= expand
        self.right += expand
        return self
    
    def expandDir(self, dir, coord):
        if dir == Direction.EAST:
            self.right += coord
        elif dir == Direction.WEST:
            self.left -= coord
        elif dir == Direction.EAST_WEST:
            self.expand(coord)
        else:
            raise ValueError("Invalid direction, the supported directions are: WEST, EAST, EAST_WEST")
        return self


    def fix(self):
        if self.left > self.right:
            tempValue = self.left
            self.left = self.right
            self.right = tempValue
        return self
     
 
    
    def getCoord(self, direction):
        if direction == Direction.WEST:
            return self.left
        elif direction == Direction.EAST:
            return self.right
        elif direction == Direction.EAST_WEST:
            return (self.left + self.right) / 2
        else:
            raise ValueError("Invalid direction")

    def getCenter(self):
        return (self.left + self.right) / 2
        
    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def getWidth(self):
        return self.right - self.left
        
    def hasNoWidth(self):
        return (self.getWidth() == 0)
        
    def init(self):
        self.left = sys.maxsize
        self.right = -sys.maxsize - 1
        return self
  
    def intersect(self, range, dir=None):
        self.fix()
        range.fix()
        intersectLeft, intersectRight = max(self.left, range.left), min(self.right, range.right)
        if dir == Direction.WEST:
            intersectRight = self.right
        elif dir == Direction.EAST:
            intersectLeft = self.left
        elif dir == Direction.EAST_WEST:
            pass
        elif dir is not None:
            raise ValueError("Invalid direction, the supported directions are:WEST, EAST, EAST_WEST or omit the 'dir' parameter")

        return Range(intersectLeft, intersectRight).fix()
   
    def isInverted(self):
        return self.right < self.left

    def isNormal(self):
        return self.right > self.left
        
    def limit(self, coord):
        if coord < self.left:
            return self.left
        elif coord > self.right:
            return self.right
        else:
            return coord
 
    def merge(self, range, dir=None):
        self.fix()
        range.fix()
        mergedLeft, mergedRight = min(self.left, range.left), max(self.right, range.right)
        self. _adjustSelfCoord(mergedLeft, mergedRight, dir)
        return self

    def mergeCoord(self, coord):
        self.fix()  
        self.left = coord if coord < self.left else self.left
        self.right = coord if coord > self.right else self.right
        return self


    def moveBy(self, coord):
        self.left += coord
        self.right += coord
        
    def overlaps(self, range, incEnds=True):
        self.fix()
        range.fix()
        if incEnds:
            return not (self.right < range.left or self.left > range.right)
        else:
            return not (self.right <= range.left or self.left >= range.right)
            
    def removeRegion(self, range):
        self.fix()
        range.fix()
        if self.contains(range, incEnds=True):
            if range.left == self.left:
                self.left = range.right
            elif range.right == self.right:
                self.right = range.left
            else:
                raise ValueError("the passed range does not matches a left or right coordinate of current range")
        else:
            raise ValueError("the passed range must be a sub-range and align with either the left or right coordinate of the current range")
    
    def set(self, *args, **kwargs):
        self.fix()
        dir = kwargs.get('dir', None)
        
        if len(args) == 1 and isinstance(args[0], Range):
            args[0].fix() 
            self. _adjustSelfCoord(args[0].left, args[0].right, dir)
            
        elif len(args) == 2:
            if all(isinstance(arg, (int, float)) for arg in args):
                self.left, self.right = args[0], args[1]
            elif isinstance(args[0], Range) and isinstance(args[1], Direction): 
                args[0].fix()  
                self. _adjustSelfCoord(args[0].left, args[0].right, args[1])
            else:
                raise ValueError("Invalid argument types for set method.")
        else:
            raise ValueError("Invalid number of arguments for set method.")
        return self
     
    def _adjustSelfCoord(self, left, right, dir):
            if dir == Direction.WEST:
                self.left = left
            elif dir == Direction.EAST:
                self.right = right  
            elif dir == Direction.EAST_WEST or dir is None:
                self.left = left
                self.right = right  
            elif dir is not None:
                raise ValueError("Invalid direction, the supported directions are: WEST, EAST, EAST_WEST, or omit the 'dir' parameter") 
                 
    def setCenter(self, coord):
        width = self.getWidth()
        self.left = coord - width / 2
        self.right = coord + width / 2

    def setCoord(self, dir, coord):
        if dir == Direction.WEST:
            self.left = coord
        elif dir == Direction.EAST:
            self.right = coord
        else:
            raise ValueError("Invalid direction, the supported directions are: WEST, EAST")
            
    def setDimension(self, coord, dir=None):
        if dir is None or dir == Direction.EAST_WEST:
            center = self.getCenter()
            self.left, self.right = center - coord / 2, center + coord / 2
        elif dir == Direction.EAST:
            self.left = self.right - coord
        elif dir == Direction.WEST:
            self.right = self.left + coord
       
        else:
            raise ValueError("Invalid direction, the supported directions are: WEST, EAST, EAST_WEST")       
            
    def setLeft(self, value):
        self.left = value

    def setRight(self, value):
        self.right = value
        
    def setWidth(self, width): 
        self.left =  self.left - width / 2
        self.right = self.right + width / 2
        
        


