
########################################################################
#
#  written and verified by He.Zeng  #add 5 methods 
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

from cni.dlo.layer import Layer




class ShapeFilter:
    #already been tested. 
    def __init__(self, layersOrFilter=None):  
        # layersSet and excludedLayersSet are properties defined by He.Zeng,
        # due to the lack of this part's definition in the PYcell API.
        self.layersSet = set()
        self.excludedLayersSet = set()
        if isinstance(layersOrFilter, Layer):
            self.include(layersOrFilter)
        elif isinstance(layersOrFilter, list):
            for layer in layersOrFilter:
                if isinstance(layer, Layer):
                    self.include(layer)
                else:
                    raise ValueError(f"Invalid type for __init__ method,expected:list of Layers rather than {layersOrFilter}") 
        elif isinstance(layersOrFilter, ShapeFilter):
            self.layersSet = layersOrFilter.layersSet.copy() # set() support copy method
            self.excludedLayersSet = layersOrFilter.excludedLayersSet.copy()
        elif layersOrFilter is not None:
            raise ValueError(f"Invalid input argument for ShapeFilter class, expected:list of Layers or Layer,rather than {layersOrFilter}")
   
   #already been tested.    
    def include(self, layers):
        if isinstance(layers, Layer):
            self.layersSet.add(layers)
        elif isinstance(layers, list):
            for layer in layers:
                if isinstance(layer, Layer):
                    self.layersSet.add(layer)
                else:
                    raise ValueError(f"Invalid type for include method,expected:list of Layers rather than {layers}")  
        else:
            raise ValueError("Invalid type for include method, expected:Layer")  
        return self
    
    #already been tested.      
    def exclude(self, layers):
        if isinstance(layers, Layer):
            if layers in self.layersSet:
                self.layersSet.discard(layers)
            else:
                self.excludedLayersSet.add(layers)
        elif isinstance(layers, list):
            for layer in layers:
                if isinstance(layer, Layer):
                    if layer in self.layersSet:
                        self.layersSet.discard(layer)
                    else:
                         self.excludedLayersSet.add(layer)
                else:
                     raise ValueError(f"Invalid type for include method, expected:list of Layers rather than {layers}") 
        else:
            raise ValueError("Invalid type for include method, expected:Layer of list of Layers")
        return self
    
    #already been tested. 
    def isIncluded(self, layer):
        return layer in self.layersSet

    def excludeTexts(self):
        raise Exception("Not implemented yet!,lack the detail of this method")
        
    #already been tested.  
    def __str__(self):
        included = ' '.join(str(layer) for layer in self.layersSet)
        excluded = ' '.join(str(layer) for layer in self.excludedLayersSet)
        str4included  = (f"include: {included}") if included else ''
        str4excluded = (f"exclude: {excluded}") if excluded else ''
        string = [str4included, str4excluded]         
        return "ShapeFilter(" + " ".join(string) + ")"
    
 
 


