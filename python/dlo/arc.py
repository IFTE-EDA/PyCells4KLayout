

########################################################################
#
# written by He Zeng  #add 8 methods
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


import math
from cni.dlo.shape import *
from cni.dlo.ellipse import *
from cni.dlo.box import *
import importlib
importlib.invalidate_caches()
importlib.reload(cni.dlo.ellipse)

importlib.invalidate_caches()
importlib.reload(cni.dlo.box)


class Arc(Shape):
    def __init__(self, layer, box, startRadian=0.0, endRadian=0.0, arcBox=None):
        super().__init__(layer = layer, bbox = box.fix())
        self.startRadian = startRadian
        self.endRadian = endRadian
        self.arcBox = arcBox
        self.ellipse = None
        Arc._checkRadian(startRadian, endRadian)
        self._updateArc()
        
    @staticmethod
    def _checkRadian(startRadian, endRadian):
        if startRadian > endRadian or (endRadian - startRadian) > math.pi:
            raise ValueError("Invalid start and end radians") 
              
    def _updateArc(self):
        startAngle = math.degrees(self.startRadian) % 360
        endAngle = math.degrees(self.endRadian) % 360
        
        if self.arcBox:
            intersectedBox = self.bbox.intersect(self.arcBox)
            if not intersectedBox.isNormal():
                raise ValueError("The intersection of box and arcBox is empty.")
            
            self.ellipse = Ellipse(self.layer, self.bbox, 0, 360, 1000, False, intersectedBox)
        else:
            if self.ellipse is None:
                self.ellipse = Ellipse(self.layer, self.bbox, startAngle, endAngle, 1000, False, None)
            else:
                self.ellipse.setAngles(startAngle, endAngle)
      
   
    
    def clone(self, nameMap=None, netMap=None):
        return Arc(self.layer, self.bbox, self.startRadian, self.endRadian, self.arcBox)
    
    def getEllipseBBox(self):
        return self.bbox
    
    def getStartAngle(self):
        return self.startRadian
    
    def getStopAngle(self):
        return self.endRadian
    
    def setEllipseBBox(self, box):
        if not box.isNormal():
            raise ValueError("Invalid ellipse bbox.")
        self.bbox = box
    
    def setStartAngle(self, radian):
        self._checkRadian(radian, self.endRadian)
        self.startRadian = radian
        self._updateArc()
        
    def setStopAngle(self, radian):
        self._checkRadian(self.startRadian, radian)
        self.endRadian = radian
        self._updateArc()
        ellipse = Ellipse(layer, box, startAngle, endAngle)
        self.set_shape(ellipse.shape) 
        
