

########################################################################
#
#  written by He.Zeng   #add 19 methods
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

import pya
from cni.dlo.polygon import *
from cni.dlo.box import *

class Grouping:
    # already been tested.  
    def __init__(self, name="", components=None):
        self.name = name if name else "Grouping_0"
        if components is not None:
            if isinstance(components, list):
                self._components = components
            else:
                self._components = [components]  
        else:
            self._components = []
    
    # already been tested.  
    def clone(self):   
        clonedComponents =[]
        for item in self._components:
            clonedComponents.append(item.clone())
        return Grouping(self.name, clonedComponents)
        
    #already tested for Rect and Polygon objects
    # these method: fgXor,fgOr,fgAnd, fgNot, use the regionToGroup function to convert to a Grouping object.
    def fgXor(self, comp, resultLayer):
        totalRegion = pya.Region()
        for groupComp in self.getComps(): 
            dRegion = pya.Region(groupComp.shape.polygon)
            totalRegion.insert(dRegion)
        if isinstance(comp, list) and not comp:
            comRegion =pya.Region()
        else:
            comRegion = pya.Region(comp.shape.polygon)
        xorRegion = totalRegion.xor(comRegion)
        return xorRegion

    # already been tested.   
    def fgOr(self, comp, resultLayer):
        totalRegion = pya.Region()
        for groupComp in self.getComps(): 
            dRegion = pya.Region(groupComp.shape.polygon)
            totalRegion.insert(dRegion)
        if isinstance(comp, list) and not comp:
            comRegion =pya.Region()
        else:
            comRegion = pya.Region(comp.shape.polygon)
        orRegion = totalRegion.or_(comRegion)
        return orRegion  
        
    # already been tested.      
    def fgNot(self, comp, resultLayer):
        totalRegion = pya.Region()
        for groupComp in self.getComps(): 
            dRegion = pya.Region(groupComp.shape.polygon)
            totalRegion.insert(dRegion)
        if isinstance(comp, list) and not comp:
            comRegion =pya.Region()
        else:
            comRegion = pya.Region(comp.shape.polygon)
        notRegion = totalRegion.not_(comRegion)
        return notRegion  

    # already been tested.  
    def fgAnd(self, comp, resultLayer):
        totalRegion = pya.Region()
        for groupComp in self.getComps(): 
            dRegion = pya.Region(groupComp.shape.polygon)
            totalRegion.insert(dRegion)
        if isinstance(comp, list) and not comp:
            comRegion =pya.Region()
        else:
            comRegion = pya.Region(comp.shape.polygon)
        andRegion = totalRegion.and_(comRegion)
        return andRegion     
        
    # already been tested.   
    def __iter__(self):
        return iter(self._components)
    
    # already been tested.   
    def destroy(self):  
        for item in self.getComps():
            item.shape.delete()
       
    
    def add(self, component):
        if isinstance(component, list):
            self._components.extend(component)
        else:
            self._components.append(component)

    def remove(self, component):
        self._components.remove(component)


    # already been tested.   
    def rotate90(self, origin=Point()):
        for component in self._components:
            component.rotate90(origin)
        return self  
    
    # already been tested.    
    def rotate180(self, origin=Point()):
        for component in self._components:
            component.rotate180(origin)
        return self 
        
    # already been tested.   
    def rotate270(self, origin=Point()):
        for component in self._components:
            component.rotate270(origin)  
        return self
        
    # already been tested.   
    def transform(self, trans):
        for component in self._components:
            component.transform(trans)  
        return self
            
            
    def moveBy(self, dx, dy):
        for component in self._components:
            component.moveBy(dx, dy)
        return self
      
 
    @property
    def bbox(self):
        totalRegion = pya.Region()
        for groupComp in self.getComps(): 
            dRegion = pya.Region(groupComp.shape.polygon)
            totalRegion.insert(dRegion) 
        dbox =  totalRegion.bbox().to_dtype(0.001)
        return Box(dbox)

    # already been tested.   
    def getComp(self, index):
        if index < 0 or index >= len(self._components):
            raise IndexError("Component index out of range")
        return self._components[index]

    # already been tested.   
    def getName(self):
        return self.name
     
    # already been tested.   
    def getComps(self):   
        return self._components[:] 
         
       