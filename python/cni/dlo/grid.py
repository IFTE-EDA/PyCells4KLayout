


########################################################################
#
#  written by He.Zeng  #add 11 methods
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


from cni.dlo.snaptype import *



class Grid:
    def __init__(self, xSize, ySize=None, snapType=SnapType.CEIL):
        if xSize <= 0:
            raise ValueError("xSize must be greater than zero")
        if ySize is not None and ySize <= 0:
            raise ValueError("ySize must be greater than zero if specified")
        self._checkSnapType(snapType)
        self.xSize = xSize
        self.ySize = ySize if ySize is not None else xSize
        self.snapType = snapType

    
    def _checkSnapType(self, value):
        if value is not None and not isinstance(value, SnapType):
            raise ValueError(f"The argument '{snapType}' is not a valid SnapType.")
    # already been tested. 
    def getSize(self):
        return self.xSize
    # already been tested. 
    def getSnapType(self):
        return self.snapType            
    # already been tested. 
    def getXSize(self):
        return self.xSize
    # already been tested. 
    def getYSize(self):
        return self.ySize
    # already been tested. 
    def setXSize(self, size):
        if size <= 0:
            raise ValueError("Size value must be greater than zero")
        self.xSize = size
    # already been tested. 
    def setYSize(self, size):
        if size <= 0:
            raise ValueError("Size value must be greater than zero")
        self.ySize = size
    # already been tested. 
    def setSnapType(self, snapType):
        if isinstance(snapType, SnapType):
            self.snapType = snapType
        else:
            raise ValueError(f"The argument '{snapType}' has incorrect type, it should be a member of the SnapType enum.")
    # already been tested. 
    def snap(self, value, snapType=None, mult=1):
        self._checkSnapType(snapType)
        snapType = snapType if snapType is not None else self.snapType    
        result = SnapType.snap(snapType, self.xSize* mult, value)
        return result
    # already been tested. 
    def snapX(self, value, snapType=None, mult=1):
        self._checkSnapType(snapType)
        snapType = snapType if snapType is not None else self.snapType
        return SnapType.snap(snapType, self.xSize* mult, value)
    # already been tested. 
    def snapY(self, value, snapType=None, mult=1):
        self._checkSnapType(snapType)
        snapType = snapType if snapType is not None else self.snapType
        return SnapType.snap(snapType, self.ySize* mult, value)

