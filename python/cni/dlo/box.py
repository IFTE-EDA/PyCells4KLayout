
########################################################################
#
#  written and verified by He.Zeng  #add 91 methods with a new property, 'dbox', The 'dbox' property is used to access methods in the pya.DBox class
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



from cni.constants import *
from cni.dlo.location import *
from cni.dlo.point import *
from cni.dlo.direction import *


from cni.dlo.point import *
from cni.dlo.range111 import *
import pya
import math
import sys


from cni.dlo.snaptype import *
from cni.dlo.transform import *





class Box(object):
    def __init__(self, *args, **kwargs):
        if not args:
            self._left, self.bottom, self._right, self._top = -sys.maxsize+1, -sys.maxsize+1, sys.maxsize-1, sys.maxsize-1
        elif len(args) == 1 and isinstance(args[0], (Box, pya.DBox)):
            self._left, self._bottom, self._right, self._top = args[0].left, args[0].bottom, args[0].right, args[0].top 
        elif len(args) == 2 and isinstance(args[0], Point) and isinstance(args[1], Point):
            # If two CustomPoint arguments are provided, create a Box with lowerLeft and upperRight points
            self._left, self._bottom, self._right, self._top = args[0].x, args[0].y, args[1].x, args[1].y  
        elif len(args) == 4 and all(isinstance(arg, (int, float)) for arg in args):   #this is used in the ihp
            self._left, self._bottom, self._right, self._top = args         
        else:
            raise ValueError("Invalid argument for Box creation")       
    # already been tested.  
    @property
    def left(self):
        return self._left
     
    # already been tested.   
    @left.setter
    def left(self, value):
        self._left = value
     
    # already been tested.   
    @property
    def bottom(self):
        return self._bottom
     
    # already been tested.  
    @bottom.setter
    def bottom(self, value):
        self._bottom = value
    
    # already been tested.        
    @property
    def right(self):
        return self._right
     
     
    @right.setter
    def right(self, value):
        self._right = value
    
    # already been tested.    
    @property
    def top(self):
        return self._top

    # already been tested.
    @top.setter
    def top(self, value):    
        self._top = value
     
    # already been tested.      
    @property
    def dbox(self):
        return pya.DBox(self.left, self.bottom, self.right, self.top)
     
    # already been tested.   
    def __str__(self):
        return f"Box({self._left}, {self._bottom}, {self._right}, {self._top})"
    
    # already been tested.
    def __eq__(self, otherbox):
        if type(self) is not type(otherbox):
             return False
        return (self.left, self.bottom, self.right, self.top) == (otherbox.left, otherbox.bottom, otherbox.right, otherbox.top) 
    # already been tested.
    def __lt__(self, other):
        raise NotImplementedError("The sort method used by ulist[]() does not apply to ulist[Box]")
     
               
    #modify self   already been tested.
    def abut(self, dir, refBox, align=True):
        if refBox.isInverted():
            raise ValueError("Invalid refbox, make sure the passed box is normal,rather than inverted") 
        if dir not in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            raise ValueError("Invalid direction, the accepted directions are NORTH, SOUTH, EAST, and WEST") 
        width, height = self.getWidth(),self.getHeight()
        if align:
            if dir in [Direction.NORTH, Direction.SOUTH]:
                self.left = refBox.getCenterX()- width/2
                self.right = refBox.getCenterX()+ width/2
            elif dir in [Direction.EAST, Direction.WEST]:
                self.bottom =refBox.getCenterY()- height/2
                self.top = refBox.getCenterY()+ height/2

        if dir == Direction.NORTH:
            self.bottom = refBox.top
            self.top = self.bottom + height
        elif dir == Direction.SOUTH:
            self.top = refBox.bottom 
            self.bottom = self.top - height
        elif dir == Direction.EAST:
            self.left = refBox.right
            self.right = self.left + width
        elif dir == Direction.WEST:
            self.right = refBox.left
            self.left = self.right - width
        return Box(self.left, self.bottom, self.right, self.top)
  
    #modify self return self already been tested.
    # there is some error in ducumentation in PyCell Studio, the type of the 'offset' argument should be int or float, not Point.
    def alignEdge(self, dir, refBox, refDir=None, offset=None):  
        if not dir.is1Dimension():
            raise ValueError("Invalid direction, the accepted directions are NORTH, SOUTH, EAST, WEST, EAST_WEST and NORTH_SOUTH") 
        refDir = dir if refDir is None else refDir
        width, height = self.getWidth(),self.getHeight()
        refBoxCenterX,refBoxCenterY = refBox.getCenterX(),refBox.getCenterY()
        offset = offset if isinstance(offset, (int,float)) else 0 
        if dir == Direction.NORTH:    
            if refDir == Direction.NORTH:
                self.top = refBox.top + offset #
                self.bottom = self.top - height
            elif refDir == Direction.SOUTH:
                self.top = refBox.bottom + offset#
                self.bottom = self.top - height
            elif refDir == Direction.NORTH_SOUTH:
                self.top = refBoxCenterY + offset
                self.bottom = refBoxCenterY - height + offset
            else:
                 raise ValueError(f"Incompatible Direction combination for method 'alignEdge':'{dir.name}' and '{refDir}'")
        elif dir == Direction.SOUTH:    
            if refDir == Direction.NORTH:
                self.bottom = refBox.top + offset
                self.top = self.bottom + height #     
            elif refDir == Direction.SOUTH:
                self.bottom = refBox.bottom + offset
                self.top = self.bottom + height # 
            elif refDir == Direction.NORTH_SOUTH:
                self.bottom = refBoxCenterY + offset
                self.top = refBoxCenterY + height+ offset
            else:
                 raise ValueError(f"Incompatible Direction combination for method 'alignEdge':'{dir.name}' and '{refDir}'")
        elif dir == Direction.EAST:
            if refDir == Direction.EAST:
                self.right = refBox.right + offset
                self.left = self.right - width
            elif refDir == Direction.WEST:
                self.right = refBox.left + offset
                self.left = self.right - width
            elif refDir == Direction.EAST_WEST:
                self.right = refBoxCenterX + offset
                self.left =  refBoxCenterX - width + offset
            else:
                raise ValueError(f"Incompatible Direction combination for method 'alignEdge':'{dir.name}' and '{refDir}'")   
        elif dir == Direction.WEST:
            if refDir == Direction.EAST:
                self.left = refBox.right + offset
                self.right = self.left + width
            elif refDir == Direction.WEST:
                self.left = refBox.left + offset
                self.right = self.left + width
            elif refDir == Direction.EAST_WEST:
                self.left =  refBoxCenterX + offset   
                self.right = refBoxCenterX + width + offset
            else:
                raise ValueError(f"Incompatible Direction combination for method 'alignEdge':'{dir.name}' and '{refDir}'")
        elif dir == Direction.NORTH_SOUTH:
            if refDir == Direction.NORTH:
                self.bottom = refBox.top - height/2 + offset
                self.top = refBox.top + height/2 + offset  
            elif refDir == Direction.SOUTH:
                self.bottom = refBox.bottom - height/2 + offset
                self.top = refBox.bottom + height/2 + offset    
            elif refDir == Direction.NORTH_SOUTH:
                self.bottom = refBoxCenterY - height / 2 + offset
                self.top = refBoxCenterY + height / 2 + offset
            else:
                raise ValueError(f"Incompatible Direction combination for method 'alignEdge':'{dir.name}' and '{refDir}'")
        elif dir == Direction.EAST_WEST:
            if refDir == Direction.EAST:
                self.left = refBox.right - width / 2 + offset
                self.right = refBox.right + width / 2 + offset
            elif refDir == Direction.WEST:
                self.left = refBox.left - width / 2 + offset
                self.right = refBox.left + width / 2 + offset
            elif refDir == Direction.EAST_WEST:
                self.left = refBoxCenterX - width / 2 + offset
                self.right = refBoxCenterX + width / 2 + offset
            else:
                raise ValueError(f"Incompatible Direction combination for method 'alignEdge':'{dir.name}' and '{refDir}'")      
        return self
    #already been tested.   
    def alignEdgeToCoord(self, dir, coord):
        if not dir.isPrimary():
            raise ValueError(f"Invalid direction '{dir}', the accepted directions are NORTH, SOUTH, EAST, and WEST") 
        if not isinstance(coord,(int, float)):
            raise ValueError(f"Invalid coord type{coord}") 
        width, height = self.getWidth(),self.getHeight()
        if dir == Direction.NORTH:
            self.top = coord
            self.bottom = self.top - height  
        elif dir == Direction.SOUTH:
            self.bottom = coord
            self.top = self.bottom + height
        elif dir == Direction.EAST:
            self.right = coord
            self.left = self.right - width
        elif dir == Direction.WEST:
            self.left = coord
            self.right = self.left + width  
        return self
    #already been tested.
    def alignEdgeToPoint(self, dir, point):
        if dir in [Direction.NORTH, Direction.SOUTH]:
            self.alignEdgeToCoord(dir, point.y)
        elif dir in [Direction.EAST, Direction.WEST]:
            self.alignEdgeToCoord(dir, point.x)
        else:
            raise ValueError(f"Invalid direction '{dir}', the accepted directions are NORTH, SOUTH, EAST, and WEST") 
        return self
    
    #already been tested.
    def alignLocation(self, loc, refBox, refLoc=None, offset=None):
        if refLoc is None:
            refLoc = loc
        originPoint = self.getLocationPoint(loc)
        refPoint = refBox.getLocationPoint(refLoc)
        self.moveBy(refPoint.x - originPoint.x, refPoint.y - originPoint.y)
        if offset and isinstance(offset, Point):
            self.moveBy(offset.x, offset.y)
        return self   
    #already been tested.
    def alignLocationToPoint(self, loc, pt):
        originPoint = self.getLocationPoint(loc)
        if pt and isinstance(pt, Point):
            self.moveBy(pt.x - originPoint.x, pt.y - originPoint.y)
        return self
        
    #already been tested.
    def centerCenter(self):
        return Point((self.left + self.right) / 2, (self.bottom + self.top) / 2)
    #already been tested.
    def centerLeft(self):
        return Point(self.left, (self.bottom + self.top) / 2)
    #already been tested.
    def centerRight(self):
        return Point(self.right, (self.bottom + self.top) / 2)
    #already been tested.
    def contains(self, box, incEdges = True):
        if incEdges:
            return box.dbox.inside(self.dbox)
        else:
            return self.left < box.left < self.right and self.left < box.right < self.right and self.bottom < box.bottom < self.top and self.bottom < box.top < self.top
    #already been tested.
    def containsPoint(self, p, incEdges = True):
        self.fix()
        if incEdges:
            return self.dbox.contains(p.dpoint)
        else:
            return (self.left < p.x < self.right and self.bottom <p.y < self.top)

    #modify + return self  already been tested.
    def expand(self, coord):#expand(Coord coord) – expands this box by the coord coordinate value in each direction
        self.left -= coord
        self.bottom -= coord
        self.right += coord
        self.top += coord
        return self
    #modify self，return  already been tested.
    def expandDir(self, dir, coord):
        if dir in [Direction.NORTH, Direction.NORTH_WEST, Direction.NORTH_EAST, Direction.NORTH_SOUTH, Direction.ANY]:
            self.top += coord
        if dir in [Direction.SOUTH, Direction.SOUTH_WEST, Direction.SOUTH_EAST, Direction.NORTH_SOUTH, Direction.ANY]:
            self.bottom -= coord
        if dir in [Direction.EAST, Direction.NORTH_EAST, Direction.SOUTH_EAST, Direction.EAST_WEST, Direction.ANY]:
            self.right += coord
        if dir in [Direction.WEST, Direction.NORTH_WEST, Direction.SOUTH_WEST, Direction.EAST_WEST, Direction.ANY]:
            self.left -= coord
        if dir in [Direction.CENTER, Direction.NONE]:
            pass  
        return self

    #modify self  no return already been tested.
    def expandForMinArea(self, dir, minArea, grid = None): #  cntBox.expandForMinWidth(EAST, minWidth, grid)
        areaDiff =  minArea -self.getArea()
        if areaDiff <=0:
            return None
        sqrtValue = round(math.sqrt(minArea), 3)
        width, height = self.getWidth(), self.getHeight()
        
        if dir == Direction.NORTH:
            self.top += areaDiff/width
        elif dir == Direction.SOUTH:
            self.bottom -= areaDiff/width
        elif dir == Direction.EAST:
            self.right += areaDiff/height
        elif dir == Direction.WEST:
            self.left -= areaDiff/height
        elif dir == Direction.NORTH_EAST:
            self.top = self.bottom + sqrtValue
            self.right = self.left + sqrtValue
        elif dir == Direction.NORTH_WEST:
            self.top = self.bottom + sqrtValue
            self.left = self.right - sqrtValue  
        elif dir == Direction.SOUTH_EAST:
            self.bottom = self.top - sqrtValue
            self.right = self.left + sqrtValue 
        elif dir == Direction.SOUTH_WEST:
            self.bottom = self.top - sqrtValue  
            self.left = self.right - sqrtValue   
        elif dir == Direction.EAST_WEST:
            deltaX = (minArea/height - width)/2
            self.left -= deltaX        
            self.right += deltaX        
        elif dir == Direction.NORTH_SOUTH:
            deltaY = (minArea/width - height)/2
            self.bottom -= deltaY      
            self.top += deltaY 
        elif dir == Direction.ANY:   
            self.right += (sqrtValue - width)/2   
            self.left -= (sqrtValue - width)/2
            self.top += (sqrtValue - height)/2
            self.bottom -= (sqrtValue - height)/2  
        elif dir in [Direction.NONE, Direction.CENTER]:
            return None
        if grid:
            self.right = grid.snapX(self.right)
            self.bottom = grid.snapY(self.bottom)
            self.top = grid.snapY(self.top)
            
         

    def _expandHeight(self, dir, minWidth):
        heightDiff = minWidth - self.getHeight()
        if heightDiff > 0:
            if dir in [Direction.NORTH, Direction.NORTH_WEST, Direction.NORTH_EAST]:
                self.top += heightDiff
            elif dir in [Direction.SOUTH, Direction.SOUTH_WEST, Direction.SOUTH_EAST]:
                self.bottom -= heightDiff
            elif dir in [Direction.NORTH_SOUTH,Direction.CENTER, Direction.ANY, Direction.NONE]:
                self.top += heightDiff / 2
                self.bottom -= heightDiff / 2
    
    def _expandWidth(self, dir, minWidth):
        widthDiff = minWidth - self.getWidth()
        if widthDiff > 0:
            if dir in [Direction.EAST, Direction.NORTH_EAST, Direction.SOUTH_EAST]:
                self.right += widthDiff
            elif dir in [Direction.WEST, Direction.NORTH_WEST, Direction.SOUTH_WEST]:
                self.left -= widthDiff
            elif dir in [Direction.EAST_WEST, Direction.CENTER, Direction.ANY, Direction.NONE]:
                self.right += widthDiff / 2
                self.left -= widthDiff / 2


    def expandForMinWidth(self, dir, minWidth, grid = None):
        dirsForHeight = [Direction.NORTH, Direction.SOUTH, Direction.NORTH_SOUTH,Direction.NORTH_WEST, Direction.NORTH_EAST,
                         Direction.SOUTH_WEST, Direction.SOUTH_EAST, Direction.CENTER, Direction.ANY, Direction.NONE]
       
        dirsForWidth = [Direction.EAST, Direction.WEST, Direction.EAST_WEST,Direction.NORTH_EAST, Direction.SOUTH_EAST,
                        Direction.NORTH_WEST, Direction.SOUTH_WEST, Direction.CENTER, Direction.ANY, Direction.NONE]
        if dir in  dirsForHeight:
            if self.getHeight() < minWidth:
                self._expandHeight(dir, minWidth)
        if dir in dirsForWidth:
            if self.getWidth() < minWidth:
                self._expandWidth(dir, minWidth) 
        if dir not in dirsForHeight and dir not in dirsForWidth:
            raise ValueError("Invalid direction, the accepted directions are SOUTH,EAST, WEST, NORTH_WEST, NORTH_EAST, NORTH_SOUTH, SOUTH_EAST, SOUTH_WEST, CENTER, EAST_WEST, ANY, NONE")  
        if grid:
            pass

    def expandToGrid(grid, dir = None):
        raise Exception("Not implemented yet!")
    
    #already been tested
    def fix(self):
        if self.right < self.left:
            originLeft = self.left
            self.left = self.right
            self.right = originLeft  
        if self.top < self.bottom:
            originBottom = self.bottom
            self.bottom = self.top
            self.top = originBottom
        return self
        
    #already been tested
    def getArea(self):
        return self.dbox.area()
    #already been tested
    def getBottom(self):
        return self.bottom
    #already been tested 
    def getCenter(self): 
        return Point((self.left + self.right) / 2, (self.bottom + self.top) / 2)
    #already been tested
    def getCenterX(self):
         return (self.left + self.right) / 2
    #already been tested
    def getCenterY(self):
         return (self.bottom + self.top) / 2
        
    #already been tested
    def getCoord(self,dir):
        if dir not in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST, Direction.NORTH_SOUTH, Direction.EAST_WEST]:
            raise ValueError(f"Invalid direction, {dir}, for Box method 'getCoord'")
        if dir == Direction.NORTH:
            return self.top
        elif dir == Direction.SOUTH:
            return self.bottom
        elif dir == Direction.EAST:
            return self.right
        elif dir == Direction.WEST:
            return self.left
        elif dir == Direction.NORTH_SOUTH:
            return self.getCenterY()
        elif dir == Direction.EAST_WEST:
            return self.getCenterX()
    #already been tested
    def getDimension(self, dir):
        if not isinstance(dir, Direction):
            raise ValueError("Invalid direction type")
        if dir == Direction.NORTH_SOUTH:
            return  self.getHeight()
        elif dir == Direction.EAST_WEST:
            return self.getWidth()
        else:
            raise ValueError(f"Invalid direction, {dir}, for Box method 'getDimension'. Direction must be either NORTH_SOUTH or EAST_WEST.")

    #already been tested
    def getHeight(self):
        return self.top - self.bottom
    #already been tested
    def getLeft():
        return self.left
    #already been tested
    def getLocationPoint(self, dirOrloc):
        if isinstance(dirOrloc, Location):
            if dirOrloc == Location.LOWER_LEFT:
                return self.lowerLeft()
            elif dirOrloc == Location.LOWER_CENTER:
                return self.lowerCenter()  
            elif dirOrloc == Location.LOWER_RIGHT:
                return self.lowerRight()
            elif dirOrloc == Location.CENTER_LEFT:
                return self.centerLeft() 
            elif dirOrloc == Location.CENTER_CENTER:
                return self.centerCenter()
            elif dirOrloc == Location.CENTER_RIGHT:
                return self.centerRight()
            elif dirOrloc == Location.UPPER_LEFT:
                return self.upperLeft() 
            elif dirOrloc == Location.UPPER_CENTER:
                return self.upperCenter() 
            elif dirOrloc == Location.UPPER_RIGHT:
                return self.upperRight()
            else:
                raise ValueError("Invalid location type")
      
        elif isinstance(dirOrloc, Direction):
            if dirOrloc == Direction.NORTH:
                return Point(self.getCenterX(), self.top)
            elif dirOrloc == Direction.SOUTH:
                return Point(self.getCenterX(), self.bottom)
            elif dirOrloc == Direction.EAST:
                return Point(self.right, self.getCenterY())
            elif dirOrloc == Direction.WEST:
                return Point(self.left, self.getCenterY())
            elif dirOrloc == Direction.NORTH_SOUTH:
                return self.centerCenter() 
            elif dirOrloc == Direction.EAST_WEST:
                return self.centerCenter()  
            else:
                raise ValueError("Invalid direction value")
        else:
            raise ValueError("The Argument{dirOrloc} is not type Location or Direction")

    # the return type is pointlist  
    def getPoints(self):
          return [self.lowerLeft(), self.upperLeft(), self.upperRight(), self.lowerRight()]
    
    #already been tested
    def getRange(self, dir):
        if dir == Direction.NORTH_SOUTH:
            return self._yRange
        elif dir == Direction.EAST_WEST:
            return self._xRange
        else:
            raise ValueError("Argument 'dir' must be either NORTH_SOUTH or EAST_WEST for the method 'getRange'")

    #already been tested
    def getRangeX(self):
         return Range(self.left, self.right)
         

    #already been tested
    def getRangeY(self):
        return Range(self.bottom, self.top)
        
    #already been tested
    def getRight(self):
        return self.right

    #create a new Box #already been tested
    def getSpacing(self, dir, refBox):
        if not isinstance(dir, Direction):
            raise ValueError("Invalid direction type for the method 'getSpacing")
        if not isinstance(refBox, Box):
            raise ValueError("refBox must be an instance of Box for the method 'getSpacing")
        if dir == Direction.NORTH:
            return self.bottom - refBox.top
        elif dir == Direction.SOUTH:
            return refBox.bottom - self.top
        elif dir == Direction.EAST:
            return self.left - refBox.right 
        elif dir == Direction.WEST:
            return refBox.left - self.right 
        else:
            raise ValueError("Argument 'dir' must be one of the four primary directions for the method 'getSpacing'")
    #already been tested
    def getTop(self):
        return self.top
    #already been tested
    def getWidth(self):
        return self.right - self.left
    #already been tested
    def hasNoArea(self):
        return self.top == self.bottom or self.right == self.left
    #modify self  #already been tested
    def init(self):
        self.left = 2147483.647
        self.right = 2147483.647
        self.bottom = -2147483.648
        self.top = -2147483.648
        return self
    #already been tested
    def intersect(self, box, dir=Direction.ANY):   #four primary directions (NORTH, SOUTH, East or WEST), or be the NULL or ANY direction,
        if not isinstance(box, Box):
            raise ValueError("box must be an instance of Box")   
        if dir in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST, Direction.NONE, Direction.ANY]:
            if dir == Direction.NONE:
                return self
            if dir == Direction.ANY:
                dBox = self.dbox & box.dbox
                self.left = dBox.left
                self.bottom = dBox.bottom
                self.right = dBox.right
                self.top = dBox.top
                
            elif dir == Direction.NORTH:
                self.top = min(self.top, box.top)
            elif dir == Direction.SOUTH:  
                self.bottom = max(self.bottom, box.bottom)       
            elif dir == Direction.EAST:
                self.right = min(self.right, box.right)
            elif dir == Direction.WEST: 
                self.left = max(self.left, box.left)           
        else:
            raise ValueError("Invalid direction value")
        return self
      
    #already been tested
    def isInverted(self):
        return self._right - self._left < 0 or self._top - self._bottom < 0
    
    #already been tested
    def isNormal(self):
        return self._right - self._left > 0 and self._top - self._bottom  > 0
    
    #already been tested
    def limit(self, point):
        if not isinstance(point, Point):
            raise ValueError("point must be an instance of Point")
        xNew = max(self.left, min(point.x, self.right))
        yNew = max(self.bottom, min(point.y, self.top))
        return Point(xNew, yNew )
    
    #already been tested
    def lowerCenter(self):
        return Point(self.getCenterX(), self.bottom)
    #already been tested
    def lowerLeft(self):  
        return Point(self.left,self.bottom)
    #already been tested
    def lowerRight(self): 
        return Point(self.right, self.bottom)       
    #already been tested
    def merge(self, box, dir=Direction.ANY):
        if not isinstance(box, Box):
            raise ValueError("box must be an instance of Box")
        if dir == Direction.NONE:
            return self
        elif dir == Direction.ANY:  
            self.left = min(self.left, box.left)
            self.bottom = min(self.bottom, box.bottom)
            self.right = max(self.right, box.right)
            self.top = max(self.top, box.top)
        elif dir in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            if dir == Direction.NORTH:
                self.top = max(self.top, box.top)
            elif dir == Direction.SOUTH:
                self.bottom = min(self.bottom, box.bottom)
            elif dir == Direction.EAST:
                self.right = max(self.right, box.right)
            elif dir == Direction.WEST:
                self.left = min(self.left, box.left)
        else:
            raise ValueError("Argument 'dir' must be one of the four primary directions or NONE,ANY direction for the method 'merge")
        return self
    
    #already been tested
    def mergePoint(self, p, incEdges = True):
        if self.containsPoint(p, incEdges):
            return self
        if p.x < self.left:
            self.left = p.x
        elif p.x > self.right:
            self.right = p.x
          
        if p.y < self.bottom:
            self.bottom = p.y
        elif p.y > self.top:
            self.top = p.y
        return self 
    
    #already been tested
    def mirrorX(self, yCoord = 0):
        mirroredTop = yCoord + yCoord - self.bottom
        mirroredBottom = yCoord + yCoord - self.top
        self.top = mirroredTop
        self.bottom = mirroredBottom
        return self 
    #already been tested
    def mirrorY(self, xCoord = 0):
        mirroredLeft = xCoord + xCoord - self.right
        mirroredRight = xCoord + xCoord - self.left
        self.left =  mirroredLeft 
        self.right = mirroredRight
        return self

 
    #already been tested
    def moveBy(self, dx, dy):
        self.left += dx
        self.right += dx
        self.bottom += dy
        self.top += dy
        return self
    #already been tested
    def _getMovetoPoint(self, destination, loc):
        if loc == Location.CENTER_CENTER:
            return destination - self.centerCenter()
        elif loc == Location.LOWER_LEFT: 
            return destination - self.lowerLeft()
        elif loc == Location.CENTER_LEFT:
            return destination - self.centerLeft()
        elif loc == Location.UPPER_LEFT:
            return destination - self.upperLeft()
        elif loc == Location.LOWER_CENTER: 
            return destination - self.lowerCenter()
        elif loc == Location.UPPER_CENTER:
            return destination - self.upperCenter()
        elif loc == Location.LOWER_RIGHT:
            return destination - self.lowerRight()
        elif loc == Location.CENTER_RIGHT:
            return destination - self.centerRight()
        elif loc == Location.UPPER_RIGHT:
            return destination - self.upperRight()
    
    # modify self, return self   already been tested   
    def moveTo(self, destination, loc = Location.CENTER_CENTER):
        point = self._getMovetoPoint(destination, loc)
        self.moveBy(point.x, point.y)
        return self
        
    # modify self, return self  already been tested    
    def moveTowards(self, dir, d):
        if not isinstance(dir, Direction):
            raise ValueError("Invalid direction value")
        if dir in [Direction.EAST_WEST, Direction.NORTH_SOUTH]:
            raise ValueError("Direction must not be opposing (EAST_WEST or NORTH_SOUTH)")
        if dir == Direction.NORTH:
            self.moveBy(0, d)
        elif dir == Direction.SOUTH:
            self.moveBy(0, -d)
        elif dir == Direction.EAST:
            self.moveBy(d, 0)
        elif dir == Direction.WEST:
            self.moveBy(-d, 0)
        elif dir == Direction.NORTH_EAST:
            self.moveBy(d, d)
        elif dir == Direction.NORTH_WEST:
            self.moveBy(-d, d)
        elif dir == Direction.SOUTH_EAST:
            self.moveBy(d, -d)
        elif dir == Direction.SOUTH_WEST:
            self.moveBy(-d, -d)    
        else:
            raise ValueError(f"Invalid direction'{dir}' for method 'moveTowards'")
        return self
    #already been tested
    def overlaps(self, box, incEdges = True):
        if incEdges:
            return self.dbox.touches(box.dbox)
        else:
            return self.dbox.overlaps(box.dbox)

    #already been tested
    def place(self, dir, refBox, distance, align = True):
        if dir not in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            raise ValueError("The argument 'dir' must be one of NORTH, SOUTH, EAST, or WEST")
        if align:
            if dir in [Direction.NORTH, Direction.SOUTH]:
                self.alignLocation(Location.CENTER_CENTER, refBox, Location.CENTER_CENTER)
            elif dir in [Direction.EAST, Direction.WEST]:
                self.alignLocation(Location.CENTER_CENTER, refBox, Location.CENTER_CENTER)
        else:
            if dir == Direction.NORTH:
                self.alignEdgeToCoord(Direction.SOUTH, refBox.top + distance)
            elif dir == Direction.SOUTH:
                self.alignEdgeToCoord(Direction.NORTH, refBox.bottom - distance)
            elif dir == Direction.EAST:
                self.alignEdgeToCoord(Direction.WEST, refBox.right + distance)
            elif dir == Direction.WEST:
                self.alignEdgeToCoord(Direction.EAST, refBox.left - distance)
        return self
 
    #return a new Box  already been tested              
    def removeRegion(self, box):
        if not self.contains(box, incEdges=True):
            raise ValueError("The argument 'box' must be a sub-box within the original box")
        matchCornersNum = sum([self.lowerLeft() == box.lowerLeft(), self.lowerRight() == box.lowerRight(), self.upperLeft() == box.upperLeft(), self.upperRight() == box.upperRight()])
        if  matchCornersNum != 1:
            raise ValueError("The argument 'box' must have exactly one matching corner with the original box")
        if self.lowerLeft() == box.lowerLeft():
            return Box(box.right, box.top, self.right, self.top)
        elif self.lowerRight() == box.lowerRight():
            return Box(self.left, box.top, box.left, self.top)
        elif self.upperLeft() == box.upperLeft():
            return Box(box.right, self.bottom, self.right, box.bottom)
        elif self.upperRight() == box.upperRight():
            return Box(self.left, self.bottom, box.left, box.bottom)
          
    #already been tested
    def rotate90(self, origin=Point(0,0)):    
        r90Dbox = self.dbox.transformed(pya.DTrans.R90)  
        self.set(r90Dbox.left,r90Dbox.bottom,r90Dbox.right,r90Dbox.top)
        self.moveBy(origin.y+origin.x, origin.y-origin.x)
        return self
        
    #already been tested
    def rotate180(self, origin=Point(0,0), mag=1.0):
        r180Dbox = self.dbox.transformed(pya.DTrans.R180)  
        self.set(r180Dbox.left,r180Dbox.bottom,r180Dbox.right,r180Dbox.top)
        self.moveBy(2*origin.x, 2*origin.y)
        return self

    #already been tested
    def rotate270(self, origin=Point(0,0), mag=1.0):
        r270Dbox = self.dbox.transformed(pya.DTrans.R270) 
        self.set(r270Dbox.left,r270Dbox.bottom,r270Dbox.right,r270Dbox.top)
        self.moveBy(origin.x -origin.y, origin.y + origin.x)
        return self
    
    
       
    #already been tested
    def set(self, *args):
        if len(args) == 1 and isinstance(args[0], Box):
            self.left, self.bottom, self.right, self.top = args[0].left, args[0].bottom, args[0].right, args[0].top
        elif len(args) == 2 and all(isinstance(arg, Point) for arg in args):
            lowerLeft, upperRight = args
            self.left, self.bottom, self.right, self.top = lowerLeft.x, lowerLeft.y, upperRight.x, upperRight.y
        elif len(args) == 2 and isinstance(args[0], Box) and isinstance(args[1], Direction):
            if args[1] is None or args[1] == Direction.ANY:
                self.left, self.bottom, self.right, self.top = args[0].left, args[0].bottom, args[0].right, args[0].top
            elif args[1] == Direction.NONE:
                return self
            elif args[1] == Direction.NORTH:
                self.top = args[0].top
            elif args[1] == Direction.SOUTH:
                self.bottom = args[0].bottom
            elif args[1] == Direction.EAST:
                self.right = args[0].right
            elif args[1] == Direction.WEST:
                self.left = args[0].left
            else:
                raise ValueError("Direction must be one of NORTH, SOUTH, EAST, WEST, ANY or NONE")       
        elif len(args) == 4 and all(isinstance(arg, (int, float)) for arg in args):
            self.left, self.bottom, self.right, self.top = args
        else:
            raise ValueError("Invalid arguments for 'set' method")
        return self
    
    #already been tested  
    def setBottom(self,value):
            self.right = value
    
    #already been tested
    def setCenter(self, point):
        dx = point.x - self.getCenterX()
        dy = point.y - self.getCenterY()
        self.moveBy(dx, dy)
    #modify self   already been tested 
    def setCenterX(self, value):
        dx = value - self.getCenterX()
        self.moveBy(dx, 0)
    #already been tested
    def setCenterY(self, value):
        dy = value - self.getCenterY()
        self.moveBy(0, dy)
    #already been tested
    def setCoord(self, dir, coord):
        if not isinstance(dir, Direction):
            raise ValueError("Invalid direction Type for method 'setCoord'")
        if dir == Direction.NORTH:
            self.top = coord
        elif dir == Direction.SOUTH:
            self.bottom = coord
        elif dir == Direction.EAST:
            self.right = coord
        elif dir == Direction.WEST:
            self.left = coord
        else:
            raise ValueError("Direction must be one of NORTH, SOUTH, EAST, or WEST")
        return self
    #already been tested
    def setDimension(self, coord, dir):
        if not isinstance(dir, Direction):
            raise ValueError("Argument 'dir' must be an instance of the Direction for the method 'setDimension'")
        centerX, centerY = self.getCenterX(), self.getCenterY()
        
        if dir in [Direction.EAST, Direction.NORTH_EAST, Direction.SOUTH_EAST]:
            self.right = self.left + coord
        if dir in [Direction.WEST, Direction.NORTH_WEST, Direction.SOUTH_WEST]:
            self.left = self.right - coord   
        if dir in [Direction.NORTH, Direction.NORTH_EAST, Direction.NORTH_WEST]:
            self.top = self.bottom + coord
        if dir in [Direction.SOUTH, Direction.SOUTH_EAST, Direction.SOUTH_WEST]:
            self.bottom = self.top - coord
        if dir in [Direction.NORTH_SOUTH, Direction.ANY]:
            self.top = centerY + coord / 2
            self.bottom = centerY - coord / 2
        if dir in [Direction.EAST_WEST, Direction.ANY]:
            self.right = centerX + coord / 2
            self.left = centerX - coord / 2
        if dir == Direction.NONE:
            return self
        return self
    
    #already been tested
    def setHeight(self, height):
        if height <= 0:
            raise ValueError("Invalid height: width must be positive") 
        centerY = self.getCenterY()
        self.top = centerY + height/2
        self.bottom = centerY - height/2
        return self
       
    def setLocationPoint(self, loc, point):
        originPoint = self.getLocationPoint(loc)
        dx = point.x - originPoint.x
        dy = point.y - originPoint.y
        self.moveBy(dx, dy)
    #already been tested
    def setRange(self, dir, range):
        if dir == Direction.NORTH_SOUTH:
            self.bottom, self.top = range.left, range.right
        elif dir == Direction.EAST_WEST:
            self.left, self.right = range.left, range.right
        else:
            raise ValueError("Argument 'dir' must be either NORTH_SOUTH or EAST_WEST for method ''")
        return self
    #already been tested
    def setRangeX(self, range):
        self.left, self.right = range.left, range.right
        return self
    #already been tested 
    def setRangeY(self, range):
        self.bottom, self.top = range.left, range.right
        return self 
    #already been tested
    def setRight(self,value):
        self.right = value
    #already been tested
    def setTop(self,value):
        self.top = value

    #already been tested
    def setWidth(self, width):
        if width <= 0:
            raise ValueError("Invalid width: width must be positive") 
        centerX = self.getCenterX()    
        self.right = centerX + width/2
        self.left = centerX - width/2
        return self

        
    def snap(self, grid, snapType=None):
        
        self.left = grid.snapX(self.left)
        self.bottom = grid.snapY(self.bottom)
        
        
    def snapX(self, grid, snapType = None):
        
        self.left = grid.snapX(self.left)
        
    def snapY(self, grid, snapType = None):
       
        self.bottom = grid.snapY(self.bottom)

    def snapTowards(self, grid, dir):
        if dir not in [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH]:
           raise ValueError("Invalid direction: dir must be a half-line direction")
        if dir in [Direction.EAST, Direction.WEST]:
            snapType = SnapType.CEIL if dir == Direction.EAST else SnapType.FLOOR
            return self.snapX(grid, snapType)
        elif dir in [Direction.NORTH, Direction.SOUTH]:
            snapType = SnapType.CEIL if dir == Direction.NORTH else SnapType.FLOOR
            return self.snapY(grid, snapType)
       
    #modify self and return self  
    #already tested
    def transform(self, trans): 
  
        if trans.orientation.value == Orientation.R0.value:
            return self.moveBy(trans.offset.x, trans.offset.y )  
        elif trans.orientation.value == Orientation.R90.value: 
             return self.rotate90(Point()).moveBy(trans.offset.x, trans.offset.y)       
        elif trans.orientation.value == Orientation.R180.value:
            return self.rotate180(Point()).moveBy(trans.offset.x, trans.offset.y)
        elif trans.orientation.value == Orientation.R270.value:
            return self.rotate270(Point()).moveBy(trans.offset.x, trans.offset.y)
        elif trans.orientation.value == Orientation.MX.value:  
             return self.mirrorX().moveBy(trans.offset.x, trans.offset.y)
        elif trans.orientation.value == Orientation.MY.value:  
             return self.mirrorY().moveBy(trans.offset.x, trans.offset.y)    
        elif trans.orientation.value == Orientation.MXR90.value:  
             return self.mirrorX().rotate90(Point()).moveBy(trans.offset.x, trans.offset.y)
        elif trans.orientation.value == Orientation.MYR90.value:  
             return self.mirrorY().rotate90(Point()).moveBy(trans.offset.x, trans.offset.y)  
        else:
            raise ValueError(f"Invalid orientation")
        
    #already been tested
    def upperCenter(self):
        return Point(self.getCenterX(), self.top) 
    #already been tested
    def upperLeft(self):
        return Point(self.left, self.top)
    #already been tested
    def upperRight(self):
        return Point(self.right, self.top)

