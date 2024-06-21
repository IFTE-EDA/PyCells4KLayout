
########################################################################
#
# written and verified by He.Zeng  #add 12 methods
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



from cni.dlo.point import *
from cni.ulist import *
from math import cos, sin, atan, atan2, pi
import copy




class PointList(ulist[Point]):
    def __init__(self, points=None):
        super().__init__(points if points is not None else []) #Pass the itemtype to the ulist class
        #self._pointlist = self
        
    #already been tested.
    def __str__(self):
        if not self:
           return "PointList()"
        else:
            #the name ptList is orignal form PyCell API
            ptList = self.compress() 
            return f"PointList([{', '.join(str(point) for point in ptList)}])"

    
    #already been tested.   
    def __eq__(self, other):
        if not isinstance(other, (list, PointList)):
            return False
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if self[i] != other[i]:
                return False
        return True 
        
    def __len__(self):
        return super().__len__()
        
             
    #modify self  #already been tested.
    def addOffsets(self, begin=0, end=0):
        if len(self) < 2:
            raise ValueError("PointList must contain at least two points to add offsets")
      
        beginXDistance = self[1].x - self[0].x
        beginYDistance = self[1].y - self[0].y 
        endXDistance = self[-1].x - self[-2].x
        endYDistance = self[-1].y - self[-2].y     
        if  beginXDistance == 0 and  beginYDistance == 0:
            raise ValueError("The first two points are identical")     
        if  endXDistance == 0 and  endYDistance == 0:
            raise ValueError("The first two points are identical")          
        if beginXDistance == 0 and  endXDistance == 0:
            self[0].y -= begin if beginYDistance > 0 else -begin
            self[-1].y += end if endYDistance > 0 else -end
            return 
        if beginXDistance == 0 and  endYDistance == 0: 
            self[0].y -= begin if beginYDistance > 0 else -begin  
            self[-1].x += end if endXDistance > 0 else -end
            return          
        if beginYDistance ==0 and endXDistance == 0:
            self[0].x -= begin if  beginXDistance > 0 else -begin
            self[-1].y += end if endXDistance > 0 else -end
            return        
        if beginYDistance ==0 and endYDistance == 0:
            self[0].x -= begin if beginXDistance > 0 else -begin
            self[-1].x += end if endXDistance > 0 else -end
            return

        beginAngle = atan(beginYDistance/beginXDistance)
        beginXExtension = begin*cos(beginAngle)
        beginYExtension = begin*sin(beginAngle)
        self[0].x += beginXExtension if  beginXDistance <= 0 else -beginXExtension
        if beginXDistance > 0:
            self[0].y -= beginYExtension
        else:
            self[0].y += beginYExtension
        self[0].x = round(self[0].x, 3)
        self[0].y = round(self[0].y, 3)

        endAngle = atan(endYDistance/endXDistance)      
        endXExtension = end*cos( endAngle)
        endYExtension = end*sin( endAngle)
        self[-1].x -= endXExtension if  endXDistance <= 0 else -endXExtension
        if endXDistance > 0:
            self[-1].y += endYExtension
        else:
            self[-1].y -= endYExtension
        self[-1].x = round(self[-1].x, 3)
        self[-1].y = round(self[-1].y, 3)
    
    #already been tested.
    def hasExtraPoints(self, isClosed=True):
        if len(self) < 3:
            return False   
        for i in range(len(self) - 2):
            if Point.areColinearPoints(self[i], self[i + 1], self[i + 2]):
                return True
        if isClosed and len(self) >= 3:
            if Point.areColinearPoints(self[-2], self[-1], self[0]) or Point.areColinearPoints(self[-1], self[0], self[1]):
                return True
        return False
    
   
    
    #already been tested.  
    # modify self and return self
    def compress(self, isClosed=True):
        if len(self) < 3:
            return self  
        compPtList = [self[0]]
        for i in range(1, len(self) - 1):
            if not Point.areColinearPoints(self[i - 1], self[i], self[i + 1]):
                compPtList.append(self[i])
        compPtList.append(self[-1])
        if Point.areColinearPoints(compPtList[0], compPtList[-2],compPtList[-1]):
            compPtList.pop()
        if Point.areColinearPoints(compPtList[-1], compPtList[0],compPtList[1]): 
            compPtList.pop(0)
        if isClosed and compPtList[0] == compPtList[-1]:
            compPtList.pop()   
        self.clear()  
        self.extend(compPtList)  
        return self
      
    def compress_oa(self):
        raise Exception("Not implemented yet!")
        
    def containsPoint(self, point, incEdges=True):
        compressedList = self.compress()
        if len(compressedList) < 3:  
            return False   
        if incEdges:
            for i in range(len(compressedList) - 1):
                if Point.areColinearPoints(compressedList[i], compressedList[i + 1], point):
                    return True 
            
    def copy(self):
         return PointList(self[:])

    def deepcopy(self):
        return copy.deepcopy(self)   
     
    #return a new pointlist object 
    def genJustifyPoints(self, justify, sep):
        if justify not in [Direction.EAST, Direction.WEST, Direction.EAST_WEST]:
           raise ValueError(f"Invalid justify direction '{justify}'.")
        if len(self) < 2:
            raise ValueError("PointList must contain at least two points to add offsets.")   
        if not self == self.compress():
            raise ValueError("Coincident or colinear points detected.")
        
        newPointList = PointList()
        for i in range(len(self)-1):
            deltaX = self[i+1].x - self[i].x
            deltaY = self[i+1].y - self[i].y
            angle = atan2(deltaY, deltaX)
            offsetX = sep * cos(angle + pi / 2)
            offsetY = sep * sin(angle + pi / 2)
            
            if justify == Direction.EAST:
                new_x = self[i].x - offsetX
                new_y = self[i].y - offsetY
                
            elif justify == Direction.WEST:
                new_x = self[i].x + offsetX
                new_y = self[i].y + offsetY
          
            newPointList.append(Point(new_x, new_y))
        if justify == Direction.EAST:
            newPointList.append(Point(self[-1].x - offsetX, self[-1].y - offsetY))
        elif justify == Direction.WEST:
            newPointList.append(Point(self[-1].x + offsetX, self[-1].y + offsetY))
        return newPointList
        
    def getBBox(self):
        minX = maxX = 0
        minY = maxY = 0
        for point in self:
            minX = min(minX, point.x)
            minY = min(minY, point.y)
            maxX = max(maxX, point.x)
            maxY = max(maxY, point.y)
        return Box(minX, minY, maxX, maxY)
      
