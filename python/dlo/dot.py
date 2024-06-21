
########################################################################
#
#  written by He.Zeng  #add 8 methods 
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



from cni.shape import *
from cni.point import *

class Dot(Shape):
    def __init__(self, layer, origin, width=0, height=0):
        super().__init__(layer=layer, bbox=None)  # Assuming Shape's __init__ takes a layer and an optional bbox
        self.origin = origin
        self.width = width
        self.height = height
        self._updateDot()  
        
    def _updateDot(self):
        ddot = pya.DBox(self.origin.x - self.width / 2, self.origin.y - self.height / 2, self.origin.x + self.width / 2, self.origin.y + self.height / 2)
        if self.shape is not None:
            self.shape =Shape.cell.shapes(self.layer.number).replace(self.shape, ddot)
        else:
            self.shape=Shape.cell.shapes(self.layer.number).insert(ddot)
            

    def clone(self, nameMap=None, netMap=None):
        return Dot(self.layer, self.origin, self.width, self.height)
    
    def getHeight(self):
        return self.height
    
    def getOrigin(self):
        return self.origin
    
    def getWidth(self):
        return self.width
    
    def setHeight(self, height):
        self.height = height
        self._updateDot()
    
    def setOrigin(self, origin):
        self.origin = origin
        self._updateDot()
    
    def setWidth(self, width):
        self.width = width
        self._updateDot()