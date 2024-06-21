
########################################################################
#
#  written by He.Zeng  #add 15 methods
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




from cni.dlo.ellipse import *
importlib.invalidate_caches()
importlib.reload(cni.dlo.ellipse)
from cni.dlo.ellipse import *
from cni.dlo.box import *

class Donut(Shape):
    def __init__(self, layer, center, radius, holeRadius, startAngle=0.0, endAngle=360.0, numPoints=300):
        super().__init__(layer=layer, bbox = None)
        self.center = center
        self.radius = radius
        self.holeRadius = holeRadius
        self.startAngle = startAngle
        self.endAngle = endAngle
        self.numPoints = numPoints
        Donut._checkRadius(holeRadius,radius)
        Ellipse.checkAngles(startAngle, endAngle)
  
        self._updateDonut()
        
    
    def _updateDonut(self):
      
        outerPoints = Ellipse.createEllipseDpoints(self.center.x, self.center.y, self.radius, self.radius, self.startAngle, self.endAngle, self.numPoints, donutFlag = True, arcIntersectedBox = None)
        innerPoints = Ellipse.createEllipseDpoints(self.center.x, self.center.y, self.holeRadius, self.holeRadius, self.startAngle, self.endAngle, self.numPoints, donutFlag = True, arcIntersectedBox = None)[::-1]
        ddonut = pya.DPolygon(outerPoints + innerPoints)
        
        if self.shape is not None:
            self.shape = Shape.cell.shapes(self.layer.number).replace(self.shape, ddonut)
        else:
            self.shape = Shape.cell.shapes(self.layer.number).insert(ddonut)
      
    @staticmethod
    def _checkRadius(holeRadius, radius):
         if holeRadius >= radius:
            raise ValueError("Hole radius must be less than outer radius.")
            
    def clone(self, nameMap=None, netMap=None):
         return Donut(self.layer, self.center, self.radius, self.holeRadius, self.startAngle, self.endAngle)
        
    def getCenter(self):
        return self.center
    
    def getEndAngle(self):
        return self.endAngle
    
    def getHoleBBox(self):
        return Box(self.center.x - self.holeRadius, self.center.y - self.holeRadius, self.center.x + self.holeRadius, self.center.y + self.holeRadius)
    
    def getHoleRadius(self):
        return self.holeRadius
    
    def getRadius(self):
        return self.radius
    
    def getStartAngle(self):
        return self.startAngle
    
    def setAngles(self, startAngle, endAngle):
        Ellipse.checkAngles(startAngle, endAngle)
        self.startAngle = startAngle
        self.endAngle = endAngle
        self._updateDonut()
    def setCenter(self, center):
        self.center = center
        self._updateDonut()
        
    def setHoleRadius(self, holeRadius):
        Donut._checkRadius(holeRadius,self.radius)
        self.holeRadius = holeRadius
        self._updateDonut()
    
    def setRadius(self, radius):
        Donut._checkRadius(self.holeRadius,radius)
        self.radius = radius
        self._updateDonut()
    
    def setStartAngle(self, angle):
        self.startAngle = angle
        self._updateDonut()
    
    def setEndAngle(self, angle):
        self.endAngle = angle  
        self._updateDonut()


  