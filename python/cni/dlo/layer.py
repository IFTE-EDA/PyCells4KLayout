
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
#
# CHANGELOG: based on the version: https://github.com/IHP-GmbH/IHP-Open-PDK/commit/ee1948bb59a87c2b537cb244eff2f6e1d88ba4da
#
#  Author        Modification
# ------------  -------------------------------------------------
# He.Zeng      Add magic methods __eq__, __hash__,__lt__,__str__ ,add property purposeNumber
#
########################################################################


class Layer(object):

    tech = None
    layout = None

    def __init__(self, name, purpose = None):
        self._name = name if purpose is None else f"{name}.{purpose}"
        self._purposeName = purpose if purpose else ""
        try:
            layerNum, datatype = Layer.tech.stream_layers()[self._name]
            self._number = Layer.layout.layer(layerNum, datatype, self._name) 
        except KeyError:
            raise ValueError(f"Layer with name '{self._name}' not found in stream layers.")
    
    # already been tested.      
    def __eq__(self, otherlayer):
        if not isinstance(otherlayer, Layer):
            return False
        return (self.name, self.purposeName) == (otherlayer.name, otherlayer.purposeName)


    def __hash__(self):
        return hash(self.name)
    
    # already been tested.  
    def __lt__(self, otherlayer):
        if self.number != otherlayer.number:
            return self.number < otherlayer.number
        else:
            return self.purposeNumber < otherlayer.purposeNumber
    
    # already been tested.      
    def __str__(self):
        return f"Layer('{self._name}')"

    def getAttrs(self):
        raise Exception("Not implemented yet!")

    def getGridResolution(self):
        raise Exception("Not implemented yet!")

    def getLayerAbove(self):
        raise Exception("Not implemented yet!")

    def getLayerAbove(self, layerMaterial):
        raise Exception("Not implemented yet!")

    def getLayerBelow(self):
        raise Exception("Not implemented yet!")

    def getLayerBelow(self, layerMaterial):
        raise Exception("Not implemented yet!")

    def getLayerName(self):
        return self._name

    def getLayerNumber(self):
        return self._number

    def getMaterial(self):
        raise Exception("Not implemented yet!")

    def getPurposeName(self):
        raise Exception("Not implemented yet!")

    def getPurposeNumber(self):
        raise Exception("Not implemented yet!")

    def getRoutingDir(self):
        raise Exception("Not implemented yet!")

    def isAbove(self, layer):
        raise Exception("Not implemented yet!")

    def isMaskLayer(self):
        raise Exception("Not implemented yet!")
    def __str__(self):
        return f"Layer('{self.name}')"

    @property
    def name(self):
        return self._name

    @property
    def number(self):
        return self._number

    @property
    def purposeName(self):
        return self._purposeName

    # already been tested.  
    @property
    def purposeNumber(self):
        try:
            A, purpose_number = Layer.tech.stream_layers1()[self._name]
            return purpose_number
        except KeyError:
            raise ValueError(f"Layer with name '{self._name}' does not have the corresponding purposeNumber.")


