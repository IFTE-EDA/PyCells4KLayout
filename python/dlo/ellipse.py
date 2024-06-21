


########################################################################
#
# written by He Zeng  #add 5 method 
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
from cni.dlo.pointlist import *
from cni.dlo.point import *
import math


class Ellipse(Shape):
  
    def __init__(self, layer, box, startAngle=0.0, endAngle=360.0, numPoints = 128, donutFlag=False, arcIntersectedBox=None): 
        
        super().__init__(layer=layer, bbox = box.fix())
        self.startAngle = startAngle % 360
        self.endAngle = 360 if endAngle % 360 == 0 and endAngle != 0 else endAngle % 360
        Ellipse.checkAngles(self.startAngle, self.endAngle) 
        self.centerX, self.centerY = box.getCenterX(), box.getCenterY()
        self.radiusX, self.radiusY = box.getWidth() / 2, box.getHeight() / 2
        self.numPoints = numPoints
        self.donutFlag = donutFlag
        self.arcIntersectedBox = arcIntersectedBox
        self.dEllipse = None 
        self._updateEllipse()
    
    def _updateEllipse(self):

        points = Ellipse.createEllipseDpoints(self.centerX, self.centerY,self.radiusX, self.radiusY, self.startAngle, self.endAngle, self.numPoints, self.donutFlag, self.arcIntersectedBox)
        self.dEllipse = pya.DPolygon(points)
        self.dEllipse.compress(True) #
        if self.shape is not None:
            self.shape = Shape.cell.shapes(self.layer.number).replace(self.shape, self.dEllipse) 
        else:
            self.shape =Shape.cell.shapes(self.layer.number).insert(self.dEllipse)
    
    @staticmethod    
    def createEllipseDpoints(centerX, centerY, radiusX, radiusY, startAngle, endAngle, numPoints, donutFlag, arcIntersectedBox):

        startRad =  math.radians(startAngle)
        endRad =  math.radians(endAngle)
        dTheta = (endRad - startRad) / (numPoints - 1)
         
        points = [] if donutFlag else [pya.DPoint(centerX, centerY)]
        for i in range(numPoints): 
            theta = startRad + i * dTheta
            x = centerX + radiusX * math.cos(theta)
            y = centerY + radiusY * math.sin(theta)
          
            if arcIntersectedBox is not None:
                if arcIntersectedBox.containsPoint(Point(x, y), incEdges=True):
                    points.append(pya.DPoint(x, y))
            else:
                points.append(pya.DPoint(x, y)) 
        return points
         
    def clone(self):  #def clone(self, nameMap=NameMapper(), netMap=NameMapper()):
        return Ellipse(self.layer, self.box, self.startAngle, self.endAngle)
    
 
    @staticmethod
    def checkAngles(startAngle, endAngle):
        if startAngle >= endAngle:
            raise ValueError("Invalid angles, startAngle must be less than endAngle ")  
        newStartAngle = startAngle % 360
        newEndAngle = endAngle % 360
        angleDiff = (newEndAngle - newStartAngle) % 360
        if angleDiff > 360:
            raise ValueError("Invalid angles, the angle difference must be less than or equal to 360")
    
    def genPolygonPoints(self, box, numPoints, gridSize):
        points = [self.bbox.getCenter()]
        for i in range(numPoints):
            angle = 2 * math.pi * i / numPoints
            x = self.centerX + self.radiusX * math.cos(angle)
            y = self.centerY + self.radiusY * math.sin(angle)
            x = round(x / gridSize) * gridSize
            y = round(y / gridSize) * gridSize
            points.append(Point(x, y))
           
            
        p1 = PointList(points).compress()
        #print(f"Number of points after compression: {len(p1)}")  
        return p1
       
    def getStartAngle(self):
        return self.startAngle

    def getEndAngle(self):
        return self.endAngle
    
    def setAngles(self, startAngle, endAngle):
        Ellipse.checkAngles(startAngle, endAngle)
        self.startAngle = startAngle % 360
        self.endAngle = endAngle % 360
        self._updateEllipse()
       
    def setBBox(self, box):
        if not box.isNormal():
            raise ValueError("Invalid bounding box")
        self.bbox = box
        self._updateEllipse()
    

