########################################################################
#
# written and verified by He.Zeng  #add 20 methods
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

from cni.dlo.shape import *
import math


import importlib
importlib.invalidate_caches()
import cni.dlo.pointlist
importlib.reload(cni.dlo.pointlist)
from cni.dlo.pointlist import *
from cni.dlo.point import *
from cni.dlo.orientation import *
from cni.dlo.location import *

class Polygon(Shape):
    def __init__(self, layerid, points):
        
        super().__init__(layer = layerid)
        self._checkPtList(points)
        ptList = PointList(points)
        #self._checkPoints(ptList)
        #compPtList = ptList.compress()
        compPtList = ptList.compress()
        self._checkPoints(compPtList)
        self._checkLength(compPtList)
        self.ptList = compPtList
        self._updatePolygon()
        self._desPolygon = False
        
    def _checkPtList(self, inputList):
        if not isinstance(inputList, list):
            raise TypeError(f"List of 'Point' objects is expected")
        '''
        for item in inputList:
            if not isinstance(item, Point):
                raise TypeError("List of 'Point' objects is expected")
        '''
    def _checkPoints(self, plist):
        if plist.hasExtraPoints():
            #pass
            raise ValueError("Points for polygon contains coincident or collinear vertices.") 
    def _checkLength(self, plist):
        if len(plist)<3:
            raise ValueError("The points of a polygon require at least three non-overlapping vertices")
        
    def _updatePolygon(self):
        dpts = []
        for pt in self.ptList:
            dpts.append(pya.DPoint(pt.x, pt.y))  
        self.dPolygon = pya.DPolygon(dpts)
        if self.shape is not None:
            #self.shape.dpolygon=self.dPolygon
            self.shape = Shape.cell.shapes(self.layer.number).replace(self.shape, self.dPolygon)  
        else:
            self.shape =Shape.cell.shapes(self.layer.number).insert(self.dPolygon)
    
    # already been tested.        
    def __str__(self):
        if self._desPolygon:
            return f"Polygon: is deleted"
        else:
            pointStr = ', '.join(str(point) for point in self.ptList)
            return f"Polygon({self.layer}, PointList([{pointStr}]))"
   
    # already been tested.       
    def fgXor(self, comp, resultLayer, filter1=ShapeFilter(), filter2=None, grid=None):
        dregion = pya.Region(comp.shape.polygon)
        nregion = pya.Region(self.shape.polygon).xor(dregion)
        return nregion
        
    # already been tested.     
    def fgOr(self, comp, resultLayer, filter1=ShapeFilter(), filter2=None, grid=None):
        dregion = pya.Region(comp.shape.polygon)  
        nregion = pya.Region(self.shape.polygon).or_(dregion)  
        return nregion   
        
    # already been tested.   
    def fgAnd(self, comp, resultLayer, filter1=ShapeFilter(), filter2=None, grid=None):
        dregion = pya.Region(comp.shape.polygon)  
        nregion = pya.Region(self.shape.polygon).and_(dregion) 
        return nregion  
    # already been tested.    
    def fgNot(self, comp, resultLayer, filter1=ShapeFilter(), filter2=None, grid=None):

        dregion = pya.Region(comp.shape.polygon)  
        nregion = pya.Region(self.shape.polygon).not_(dregion)  
       
        return nregion  




    # transform  return self modify self  
    #already tested      
    def transform(self, trans):
        nptList = [] 
        for pt in self.ptList:
            #already tested
            if trans.orientation.value ==Orientation.R0.value:
                npt = Point(pt.x, pt.y) + trans.offset
                
            elif trans.orientation.value ==Orientation.R90.value:
                npt = Point(- pt.y, pt.x) + trans.offset
                
            elif trans.orientation.value ==Orientation.R180.value: 
                npt = Point(- pt.x, -pt.y) + trans.offset
 
            elif trans.orientation.value ==Orientation.R270.value:
                npt = Point(pt.y, -pt.x) + trans.offset
                
            elif trans.orientation.value ==Orientation.MX.value: 

                npt = Point(pt.x, -pt.y)+ trans.offset
            elif trans.orientation.value == Orientation.MY.value: 
                npt = Point(-pt.x, pt.y)+ trans.offset
            elif trans.orientation.value == Orientation.MXR90.value: 

                npt = Point(pt.y, pt.x)+ trans.offset
            elif trans.orientation.value == Orientation.MYR90.value:   
                npt = Point(-pt.y, pt.x)+ trans.offset
                
            nptList.append(npt)    
        self.setPoints(nptList)
        return self
    # already been tested.     
    def rotate90(self, origin = None):
        r90ptList = [] 
        for pt in self.ptList:
            r90ptList.append(pt.transform(Transform(origin.x + origin.y, origin.y -origin.x, Orientation.R90)))
        self.setPoints(r90ptList)
        return self
 
    # already been tested.       
    def rotate180(self, origin=Point(0,0)):
        r180ptList = [] 
        for pt in self.ptList:
             r180ptList.append(pt.transform(Transform(2*origin.x, 2*origin.y, Orientation.R180)))
        self.setPoints(r180ptList)
        return self

    # already been tested.    
    def rotate270(self, origin=Point(0,0), mag=1.0):
        r270ptList = [] 
        for pt in self.ptList:
             r270ptList.append(pt.transform(Transform(origin.x -origin.y, origin.y + origin.x, Orientation.R270)))
        self.setPoints(r270ptList)
        return self
    
    # already been tested.            
    @property
    def bbox(self):
        return Box(self.shape.dbbox())
        
   
    def moveTo(self, destination, loc = Location.CENTER_CENTER):
        
        point = self._getMovetoPoint(destination, loc)
        self.moveBy(point.x, point.y)
        return self
    
    def _getMovetoPoint(self, destination, loc):
        if loc == Location.CENTER_CENTER:
            return destination - self.bbox.centerCenter()
        elif loc == Location.LOWER_LEFT: 
            return destination - self.bbox.lowerLeft()
        elif loc == Location.CENTER_LEFT:
            return destination - self.bbox.centerLeft()
        elif loc == Location.UPPER_LEFT:
            return destination - self.bbox.upperLeft()
        elif loc == Location.LOWER_CENTER: 
            return destination - self.bbox.lowerCenter()
        elif loc == Location.UPPER_CENTER:
            return destination - self.bbox.upperCenter()
        elif loc == Location.LOWER_RIGHT:
            return destination - self.bbox.lowerRight()
        elif loc == Location.CENTER_RIGHT:
            return destination - self.bbox.centerRight()
        elif loc == Location.UPPER_RIGHT:
            return destination - self.bbox.upperRight()



    # already been tested.    
    def moveBy(self, dx, dy):
        moveByptList = [] 
        for pt in self.ptList:
             moveByptList.append(pt+Point(dx,dy))
        self.setPoints(moveByptList)
        return self

    # already been tested.       
    def destroy(self):  
        self.shape.delete()
        #self.shape._destroyed():
        self.destroyed = True
        
    # already been tested.    
    def clone(self, nameMap=None, netMap=None):
        return Polygon(self.layer, self.ptList)
        

    def getEdgeLength(self, index):
        if index < 0 or index >= len(self.points) - 1:
            raise IndexError("Index out of bounds")
        p1 = self.points[index]         #Each segment has three point locations
        p2 = self.points[index + 1]
        return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

    # already been tested.         
    def getNumPoints(self):
        return len(self.ptList)

    # already been tested.  return a new PointList object
    def getPoints(self):
        return PointList(self.ptList)

    def isOrthogonal(self):
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i + 1]
            if not (p1.x == p2.x or p1.y == p2.y):
                return False
        return True

    # already been tested.  No reutrn
    def setPoints(self, other):
        self._checkPtList(other)
        nPtList = PointList(other)
        self._checkPoints(nPtList)
        ncompPtList = nPtList.compress()
        self._checkLength(ncompPtList)
        self.ptList = ncompPtList
        self._updatePolygon()
        

        
        
        
