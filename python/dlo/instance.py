

########################################################################
#
#  written by He.Zeng  #add 12 methods 
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

from cni.attrtype import *
from cni.dlo.orientation import *
from cni.dlo.transform import *
import importlib
importlib.invalidate_caches()
import cni.dlo.transform
importlib.reload(cni.dlo.transform)
import pya
from cni.dlo.shape import *
from cni.dlo.paramarray import *
from cni.dlo.point import *

class Instance(Shape):
    
    instNum = 0
    instNames = set()
    
    # already been tested. 
    def __init__(self, dloName, params=None, nodeSpec=None, name="", trans=None, checkParams=False,dcell=None):  #append(Instance('resistor_unit', unitParams, ['PLUS'+str(i), 'MINUS'+str(i)], name))
       
        super().__init__()
      
        self.lytech = Layer.tech
        self._name = name
        self.dloName = dloName
        self.params = params if params is not None else {}
        self.nodeSpec = nodeSpec
        self.trans = trans if trans is not None else Transform()
        self.checkParams = checkParams
        self.attrType = None 
        self.dcell = Shape.cell
        self.master = "PyCellLib"
        self.dinstance = None
        if name:
            self.setName(name)
        else:
            self.name = f"I__{Instance.instNum}"
            Instance.instNum += 1

        if trans:
            self.origin = Point(trans.offset.x, trans.offset.y)
            self.orient = orientMapping.get(trans.orientation.value, pya.DTrans.R0)

        else:
            self.origin =Point()
            self.orient = pya.DTrans.R0

        parts = dloName.split('/')
        self.libName = parts[0] if parts else None
        self.cellName = parts[1] if len(parts) > 1 else None 
        self._updateInstance()
        
    def _updateInstance(self):
        lib = pya.Library.library_by_name(self.libName) if self.libName else pya.Library.library_by_name("Basic")
        layout = lib.layout()
        if not layout.has_cell(self.cellName):
            #raise ValueError(f"Cell {cellName} not found in library {libName}")
            print(f"Cell {cellName} not found in library {libName}")
        cell = layout.cell(self.cellName)   
        self.dparamdeclaration = layout.pcell_declaration(self.cellName) 
        tr = pya.DTrans(self.orient, pya.DVector(self.origin.x, self.origin.y))
        self.dcellinst = pya.DCellInstArray(cell, tr)     
        if self.dinstance is None:
            self.dinstance = Shape.cell.insert(self.dcellinst) 
        else:
            Shape.cell.replace(self.dinstance, self.dcellinst)
    
    # already been tested. 
    def setParams(self, params, checkParams=False):
        if checkParams:
            paramSet = self.getParams()
            for param in params.iteritems():
                if param[0] not in paramSet:
                    raise ValueError(f"Parameter {param[0]} is not a valid PCell parameter.")
                paramType = type(paramSet[param[0]])
                if not isinstance(param[1], type(paramType)):
                    raise ValueError(f"Parameter {param[0]} has an invalid type. Expected {expected_type}, got {type(param[1])}.")
        
        for name, value in params.iteritems():   
            self.dinstance.change_pcell_parameter(name, value)
    
    # already been tested. 
    def setOrientation(self, orient):
        norient = orientMapping.get(orient.value, pya.DTrans.R0)
        self.orient= norient
        self.dinstance.dtrans = norient
       
    
    # already been tested.                  
    def getOrigin(self):
        return self.origin
        
    # already been tested.     
    def setOrigin(self, other):
        self.origin.x = other.x
        self.origin.y = other.y
        ntr = pya.DTrans(self.orient, pya.DVector(other.x, other.y))
        self.dinstance.dtrans = ntr

    
    
    # already been tested.                    
    @property
    def name(self):
        return self._name

    # already been tested.    
    @name.setter
    def name(self, value):
        if value in Instance.instNames:
            raise ValueError(f"The instance with name '{value}' is already exists in DLoGen.")
        self._name = value
        Instance.instNames.add(value)
        
    # already been tested.       
    def getName(self):
        return self._name
     
    # already been tested.    
    def setName(self,value):
        self._name = value
        
    def getComps(self):
        pass
  
    def getRect1(self): 
        pass
           
    def getBBOx(self, shape_filter=None):
        if shape_filter is None:
            return Box(self.dinstance.bbox())
        else:
            bbox = pya.DBox(0, 0, 0, 0)
            for filterlayer in shape_filter.layersSet:
                layerIndex = self.disntance.layout().layer(filterlayer.number, filterlayer.purposeName)
                
                layerDBox = self.dinstance.dbbox(layerIndex)
                bbox += layerDBox
            return Box(bbox)
    
    def destroy(self):
        self.dinstance.delete() 
       
    @staticmethod
    def find(name):
        pass

    def getComps(self):
        pass

    def getRect1(self): 
        pass
        
    def getComps(self):
        pass
  
    def getRect1(self): 
        pass
       
    def getParams(self, params=None, all=True):
        if self.dparamdeclaration:
            paramArray = ParamArray()
            for param in self.dparamdeclaration.get_parameters():
                name = param.name
                value = param.default 
                paramArray[name] = value
            return paramArray
        else:
            print(f"No parameter declaration found for cell {cellName}")
            return None
  