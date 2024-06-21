

########################################################################
#
#  written by He.Zeng  #add 4 methods 
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


class Line(Shape):
    def __init__(self, layer, points):
        super().__init__(layer=layer)
        self.points = points.compress()
        if len(self.points) < 2:
            raise ValueError("Line must have at least two distinct points")
        self._updateLine()
    
    def _updateLine(self):
        ddot = pya.DBox(self.origin.x - self.width / 2, self.origin.y - self.height / 2, self.origin.x + self.width / 2, self.origin.y + self.height / 2)
        
        # add to Shapes list just for demostration
        if self.shape is not None:
            self.shape =Shape.cell.shapes(self.layer.number).replace(self.shape, ddot)
        else:
            self.shape = Shape.cell.shapes(self.layer.number).insert(ddot)
   
    

    def clone(self, nameMap=None, netMap=None):
        return Line(self.layer, self.points)

    def getNumPoints(self):
        return len(self.points)

    def getPoints(self):
        return self.points

