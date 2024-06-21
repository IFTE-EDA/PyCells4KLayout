
########################################################################
#
#  written by He Zeng  #add 9 methods
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
from cni.dlo.pathstyle import *
from cni.dlo.pointlist import *
from cni.dlo.shape import *

class Path(Shape):
    def __init__(self, layer, width, points, style=PathStyle.TRUNCATE, beginExt=0, endExt=0):
        self.layer = layer
        self.width = width
        self._points = PointList(points).compress() 
        self.style = style
        self.beginExt =beginExt
        self.endExt = endExt  
        self.dpath = None
        if len(self._points) < 2:
            raise ValueError("Path must have at least two distinct points")
        self.updatePin()
        
    def updatePin(self):
        dPoints = [pya.DPoint(pt.x, pt.y) for pt in self.points]
        tempDpath = pya.DPath(dPoints, self.width, self.beginExt, self.endExt)
        if self.dpath is not None:
            self.dpath = Shape.cell.shapes(self.layer.number).replace(self.dpath, tempDpath)
        else:
            self.dpath = Shape.cell.shapes(self.layer.number).insert(tempDpath)

    def clone(self, nameMap=None, netMap=None):
        return Path(self.layer, self.width, self.points, self.style)

    def getBeginExt(self):
        if self.style == PathStyle.VARIABLE:
            return self.end_ext
        return 0
            
    def setBeginExt(self, beginExtNew):
        if self.style != PathStyle.VARIABLE:
            raise ValueError("Non-zero begin extension can only be set for VARIABLE path style")
        if self.beginExt != beginExtNew:
            self.beginExt = beginExtNew
            self.updatePin()
      
    def getEndExt(self):
        if self.style == PathStyle.VARIABLE:
            return self.end_ext
        return 0
    def setEndExt(self, endExtNew):
        if self.style != PathStyle.VARIABLE:
            raise ValueError("Non-zero begin extension can only be set for VARIABLE path style")
        if self.endExt != endExtNew:
            self.endExtt = endExtNew
            self.updatePin()
    def setWidth(self, new_width):
        if self.width != new_width:
            self.width = new_width
            self.updatePin()
    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, newPoints):
        self._points = PointList(newPoints).compress()  
        self.updatePin()

    def getBoundary(self, usePathOrder=False):
        pass
      
