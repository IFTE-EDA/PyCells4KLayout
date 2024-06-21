
########################################################################
#
# written  by He.Zeng  #add 24 methods
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


from cni.point import *
from cni.shape import *
from cni.layer import *




class Segment():
       
    def __init__(self, *args, **kwargs):
        if not args:
            self._head = Point(0,0)
            self._tail = Point(0,0)
        elif len(args) == 1 and isinstance(args[0], Segment):
            self._head = arg[0].head
            self._tail = arg[0].tail 
        elif len(args) == 2 and all(isinstance(arg, Point) for arg in args): 
            self._head, self._tail = args
        else:
            raise ValueError("Invalid argument for segment creation")
            
        self.dSegment = None 
        self.shape = None
        self._updateSegment()  

    def _updateSegment(self): #just using for display segment in klayout
        self.dSegment = pya.DEdge(self.head.x, self.head.x,self.tail.x, self.tail.y)
        
        # hier add the Layer('Metal4') for a  visual comprision, 
        if self.shape is not None:
            self.shape = Shape.cell.shapes(Layer('Metal4').number).replace(self.shape, self.dSegment)
        else:
            self.shape = Shape.cell.shapes(Layer('Metal4').number).insert(self.dSegment)  #self.layer.number
        
    @property
    def head(self):
        return self._head  
    @head.setter
    def head(self, value):
        self._head = value 
    @property
    def tail(self):
        return self._tail
    @head.setter
    def head(self, value):
        self._tail = value 
        
    def addOffsets(self, begin=0, end=0):
        if not isinstance(begin, (int, float)) or not isinstance(end, (int, float)):
            raise ValueError("begin and end Offset values must be numeric")
        self.head = Point(self.head.x + begin, self.head.y + begin) if begin >= 0 else self.head
        self.tail = Point(self.tail.x + begin, self.tail.y + begin) if begin >= 0 else self.tail
        if self.head == self.tail and (begin != 0 or end != 0):
            raise ValueError("Cannot modify a coincident segment with two non-zero offsets")
            
    
    def contains(self, segment, incEnds=True):      
        if incEnds:
            return self.dSegment.contains(segment.head.point) and self.dSegment.contains(segment.tail.point)
        else:
            return self.dSegment.contains_excl(segment.head.point) and self.dSegment.contains_excl(segment.tail.point)
          
    def containsPoint(self, point, incEnds=True): 
        if incEnds:
            return self.dSegment.contains(point.point)
        else:  
            return self.dSegment.contains_excl(point.point)
  

    def extrapIntersect(self, other_segment):
        pass
        
        
    def genJustifySegment(self, justify, sep):
    
        if self.head == self.tail:
            raise ValueError("the modified segment cannot be a degenerate segment.")
        
        if justify not in [Direction.EAST, Direction.WEST, Direction.EAST_WEST]:
            raise ValueError("the supported directions must be one of EAST, WEST, or EAST_WEST.")
        
        
        if justify == Direction.EAST:
            offset = sep
        elif justify == Direction.WEST:
            offset = -sep
        elif justify == Direction.EAST_WEST:
            offset = sep
        return Segment(Point(self.head.x + offset, self.head.y), Point(self.tail.x + offset, self._tail.y ))
        
    def getDeltaX(self):
        return self.tail.x - self.head.x
    
    def getDeltaY(self):
        return self.tail.y - self.head.y
    
    def getDir(self):
        dx = self.getDeltaX()
        dy = self.getDeltaY()

        if dx == 0 and dy == 0:
            return Direction.NONE
        elif dx > 0 and dy == 0:
            return Direction.EAST
        elif dx < 0 and dy == 0:
            return Direction.WEST
        elif dx == 0 and dy > 0:
            return Direction.NORTH
        elif dx == 0 and dy < 0:
            return Direction.SOUTH
        elif dx > 0 and dy > 0:
            return Direction.NORTH_EAST
        elif dx < 0 and dy > 0:
            return Direction.NORTH_WEST
        elif dx > 0 and dy < 0:
            return Direction.SOUTH_EAST
        elif dx < 0 and dy < 0:
            return Direction.SOUTH_WEST
    
    def getHead(self):
        return self.head
    
    def getPosition(self, position):
        if position < 0 or position > 1:
            raise ValueError("the passed argument must be between 0 and 1")
        if position == 0:
            return  self.head
        elif position == 1:
            return self.tail
        return Point( self.head.x + position * (self.tail.x - self.head.x), self.head.y + position * (self.tail.y - self.head.y))
    
    def getTail(self):
        return self.tail
    
    def hasIntersection(self, segment, incEnds=True, incParallel=True):

        raise Exception("Not implemented yet!")
    
    def intersect(self, segment):
        raise Exception("Not implemented yet!")
    
    
    def isCoincident(self):
        return self.head == self.tail
    
    def isHorizontal(self):
        return self.getDeltaY() == 0
    
    def isOrthogonal(self):
        return self.isHorizontal() or self.isVertical()
    
    def isParallel(self, segment):

        return self.dSegment.is_parallel(segment.dSegment)
    
    def isVertical(self):
        return self.getDeltaX() == 0
    
    def moveBy(self, dx, dy):
        self.head = Point(self.head.x + dx, self.head.y + dy)
        self.tail = Point(self.tail.x + dx, self.tail.y + dy)
    
    def reverse(self):
        self.head, self.tail = self.tail, self.head
    
    def set(self, head, tail):
        self.head = head
        self.tail = tail
    
    def setHead(self, head):
        self.head = head
    
    def setTail(self, tail):
        self.tail = tail
    
    def transform(self, trans):
        raise Exception("Not implemented yet!")

