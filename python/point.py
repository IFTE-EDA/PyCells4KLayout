########################################################################
#
# written and verified by He.Zeng  #add 32 methods
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
from cni.dlo.snaptype import *
from cni.dlo.direction import *
from cni.dlo.grid import *
from cni.dlo.transform import *
import math


class Point():

    def __init__(self, *args):
        if len(args) == 0:
            self._x = 0
            self._y = 0
        elif len(args) == 1 and isinstance(args[0], pya.Point):
            #dbu default 0.001
            self._x = args[0].to_dtype(0.001).x
            self._y = args[0].to_dtype(0.001).y
        elif len(args) == 1 and isinstance(args[0], pya.Point):
            self._x = args[0].x
            self._y = args[0].y
        elif len(args) == 2 and all(isinstance(arg, (int, float)) for arg in args):
            self._x = args[0]
            self._y = args[1]
        else:
            raise ValueError("Invalid arguments for construct the Point class")
        
        self.dpoint = pya.DPoint(self._x, self._y)

    #already been tested. 
    def __str__(self):
        return f"Point({self.x}, {self.y})"
        
  
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
   
    #already been tested. 
    def __eq__(self, otherpoint):
        if not isinstance(otherpoint, Point):
            return False
        return abs(self.x - otherpoint.x) < 1e-12 and abs(self.y - otherpoint.y) < 1e-12
        
    #already been tested.      
    def __add__(self, otherpoint):
        return Point(self.x + otherpoint.x, self.y + otherpoint.y)

    #already been tested.      
    def __sub__(self, otherpoint):
        return Point(self.x - otherpoint.x, self.y - otherpoint.y)
    
    #already been tested.      
    def __lt__(self, otherpoint):
        raise NotImplementedError("The sort method used by ulist[]() does not apply to ulist[Point]")
     
    #new added by He.Zeng, not exist in original Point class  
    @classmethod
    def isInstPoint(cls, p):
        if not type(p) is Point:
            raise ValueError("The parameter is not a Point object.")

    #already been tested. 
    #Code source: https://www.geeksforgeeks.org/program-check-three-points-collinear/
    @classmethod
    def areColinearPoints(cls, p1, p2, p3, tolerance=1e-9):   
         area = (p1.getX() * p2.getY() + p2.getX() * p3.getY() + p3.getX() * p1.getY()) - (p1.getX() * p3.getY() + p2.getX() * p1.getY() + p3.getX() * p2.getY())
         return abs(area) < tolerance
    
    #already been tested.     
    def copy(self):
         return Point(self.x, self.y)
    #already been tested.  
    def getCoord(self, dir):
        if dir == Direction.EAST_WEST:
            return self.x
        elif dir == Direction.NORTH_SOUTH:
            return self.y
        else:
            raise TypeError("Invalid direction, argument 'dir' should be one of  EAST_WEST or NORTH_SOUTH")
    #already been tested.         
    def getSpacing(self, dir, refPoint):
        if dir not in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            raise ValueError("Invalid direction, the accepted argument 'dir' should be one of NORTH,SOUTH,EAST and WEST")
        if dir == Direction.EAST:
            return self.x - refPoint.x
        elif dir == Direction.WEST:
            return refPoint.x - self.x
        elif dir == Direction.NORTH:
            return self.y - refPoint.y
        else: 
            return refPoint.y - self.y     
    #already been tested.   
    def getX(self):
        return self.x
    #already been tested.   
    def getY(self):
        return self.y
        
    @staticmethod
    def invalid():
        return Point(2147483.647, 2147483.647)
    
    #already been tested.  
    def isBetween(self, pointA, pointB):
        if self.getX() == pointA.getX()== pointB.getX():
            return min(pointA.getY(), pointB.getY()) <= self.getY() <= max(pointA.getY(), pointB.getY())
        elif self.getY() == pointA.getY() == pointB.getY():
            return min(pointA.getX(), pointB.getX()) <= self.getX() <= max(pointA.getX(), pointB.getX())
        return False
    
    #already been tested. 
    def isValid(self):
         return self.x < Point.invalid().x and self.y < Point.invalid().y
      
    #already been tested.  
    def place(self, dir, refPoint, distance, align=True):
        if dir not in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            raise ValueError("Invalid direction, the accepted directions are NORTH,SOUTH,EAST and WEST")
        if align:
            if dir in [Direction.NORTH, Direction.SOUTH]: 
                self.x = refPoint.x
            else:
                self.y = refPoint.y

        if dir == Direction.NORTH:
            self.y = refPoint.y + distance
        elif dir == Direction.SOUTH:
            self.y = refPoint.y - distance
        elif dir == Direction.EAST:
            self.x = refPoint.x + distance
        elif dir == Direction.WEST:
            self.x = refPoint.x - distance        
    #already been tested. 
    def set(self, *args):
        if len(args) == 1 and isinstance(args[0], Point):
            self.x = args[0].x
            self.y = args[0].y
        elif len(args) == 2 and all(isinstance(arg, (int, float)) for arg in args) : 
            self.x, self.y = args
        else:
            raise ValueError("Invalid arguments for the set method. Accepted arguments are either a Point object or two coordinate values.")
    #already been tested. 
    def setCoord(self, dir, coord):
        if dir not in [Direction.EAST_WEST,Direction.NORTH_SOUTH]:
            raise ValueError(f"Invalid direction {dir}, the accepted directions are EAST_WEST, NORTH_SOUTH")
        if dir == Direction.EAST_WEST:
            self.x = coord
        elif dir == Direction.NORTH_SOUTH:
            self.y = coord
    #already been tested. 
    def setX(self, value):
        self.x = value

    #already been tested. 
    def setY(self, value):
        self.y = value

        
    def snap(self, grid, snapType=None):
        self.x = SnapType.snap(snapType, grid.getXSize(), self.x)
        self.y = SnapType.snap(snapType, grid.getYSize(), self.y)
      
    def snapX(self, grid, snapType=None):
        self.x = SnapType.snap(snapType, grid.getXSize(), self.x)

    def snapY(self, grid, snapType=None):
        self.y = SnapType.snap(snapType, grid.getYSize(), self.y)

    def snapTowards(self, grid, dir):
        if dir not in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            raise ValueError("Invalid direction for snapTowards")
        if dir in [Direction.EAST, Direction.WEST]:
            self.snapX(grid)
        else:
            self.snapY(grid)
    
    #already been tested. 
    def toDiagAxes(self):
        euclidianDistance = math.sqrt(self.x ** 2 + self.y ** 2)
        angle = math.atan2(self.y, self.x) - math.radians(45)
        diagX = round(euclidianDistance * math.cos(angle) * math.sqrt(2), 3)
        diagY = round(euclidianDistance * math.sin(angle) * math.sqrt(2), 3)
        return Point(diagX, diagY)
    #already been tested. 
    def toOrthogAxes(self):
        distance = math.sqrt(self.x  ** 2 + self.y  ** 2)/ math.sqrt(2)
        angle = math.atan2(self.y, self.x) + math.radians(45)
        orthogonalX = round(distance * math.cos(angle),10)
        orthogonalY = round(distance * math.sin(angle),10)
        return Point(orthogonalX, orthogonalY)

    #modify self  already been tested. 
    def transform(self, trans):
        tempx = self.x
        if trans.orientation == Orientation.R0:
            self.x = round((self.x + trans.xOffset) * trans.mag, 3)
            self.y = round((self.y + trans.yOffset) * trans.mag, 3)
        
        if trans.orientation == Orientation.R90:
            self.x = round((trans.xOffset - self.y) * trans.mag, 3)
            self.y = round((tempx + trans.yOffset) * trans.mag, 3)
   
        if trans.orientation == Orientation.R180:
            self.x = round((trans.xOffset - self.x)*trans.mag, 3)
            self.y = round((trans.yOffset - self.y)*trans.mag, 3)
        
        if trans.orientation == Orientation.R270:
            self.x = round((trans.xOffset + self.y) * trans.mag, 3)
            self.y = round((trans.yOffset - tempx) * trans.mag, 3)
        
        if trans.orientation == Orientation.MX:
            self.x = round((trans.xOffset + self.x)*trans.mag, 3)
            self.y = round((trans.yOffset - self.y)*trans.mag, 3)
          
        if trans.orientation == Orientation.MY:
            self.x = round((trans.xOffset - self.x)*trans.mag, 3)
            self.y = round((trans.yOffset + self.y)*trans.mag, 3)
        
        if trans.orientation == Orientation.MXR90:
            self.x = round((trans.xOffset + self.y)*trans.mag, 3)
            self.y = round((trans.yOffset + tempx)*trans.mag, 3)
            
        if trans.orientation == Orientation.MYR90:
            self.x = round((trans.xOffset - self.y)*trans.mag, 3)
            self.y = round((trans.yOffset - tempx)*trans.mag, 3) 
        
        return self  
     
    #already been tested.    
    @property
    def x(self):
        return self._x
     
    #already been tested.    
    @x.setter
    def x(self, value):
        self._x = value
        self.dpoint = pya.DPoint(self._x, self._y)
    
    #already been tested. 
    @property
    def y(self):
        return self._y
    
    #already been tested. 
    @y.setter
    def y(self, value):
        self._y = value
        self.dpoint = pya.DPoint(self._x, self._y)

