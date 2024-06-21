########################################################################
#
# Copyright 2023 IHP PDK Authors
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
# CHANGELOG: based on https://github.com/IHP-GmbH/IHP-Open-PDK/blob/a065e8596663227569eddfdcd03581f30122ffaf/ihp-sg13g2/libs.tech/klayout/python/cni/shape.py
#
#   Author        Modification
# ------------  -------------------------------------------------
# He.Zeng      modify __init__, create three properties: name layer bbox
# He.Zeng      add getBBox, getPin, getNet methods 
#
########################################################################


from cni.dlo.box import *

from cni.dlo.shapefilter import ShapeFilter
from cni.dlo.layer import *  


class Shape(object):  #attrubutes: bbox layer, name

    cell = None
    layer_bbox_map = {}

    def __init__(self, layer=None, bbox = None, name=None):
        self.shape = None
        if isinstance(layer, Layer):
            self._layer = layer
        elif isinstance(layer, str):
            self._layer = Layer(layer)
        elif layer is not None:
            raise ValueError("layer must be a Layer instance or a string representing the layer name.")

        self._bbox = bbox
        self._name = name
        self.color_mask = None
        self.net = None
        self.pin = None
       
        if layer is not None and bbox is not None:  
            Shape.layer_bbox_map[self._layer.number] = bbox

    def set_shape(self, sh):
        self.shape = sh
        
    @property
    def bbox(self):
        return self._bbox
   
    @bbox.setter 
    def bbox(self, value):
        self._bbox = value
        
    
    @property
    def layer(self):
        return self._layer
    
    @layer.setter
    def layer(self, value):
        self._layer = value
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value

    def getBBox(self, filter=ShapeFilter()):
        if not filter.layersSet: 
            if not filter.excludedLayersSet:
                return self.bbox
            else:
                if self.layer and self.layer not in filter.excludedLayersSet:
                    return self.bbox  
                else:
                    return self.bbox.init()
        else: 
            if self.layer and self.layer in filter.layersSet:
                return self.bbox
            else:
                return self.bbox.init()
           

    def getPin(self):
        return self.pin

    def getNet(self):
        return self.net 
        
    def setLayer(self, layer):
        self.layer = layer  
 
    
