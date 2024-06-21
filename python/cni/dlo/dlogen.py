
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
# CHANGELOG: based on the version: https://github.com/IHP-GmbH/IHP-Open-PDK/commit/f4be620a803953e4f0f91488b200d6e447be3cf0
#
#  Author        Modification
# ------------  -------------------------------------------------
# He.Zeng      provide a simple version of addpin addterm, need continue improve the addpin and addterm method
#
########################################################################


from abc import ABC, abstractmethod
from cni.dlo.rect import *
from cni.dlo.termtype import * 
from cni.dlo.term import * 
from cni.dlo.pin import * 
from cni.dlo.shape import *


class DloGen(ABC):
    AttrType = ['CELL_NAME', 'CELL_TYPE', 'LAST_SAVED_TIME', 'LIB_NAME', 'VIEW_NAME']
    
    def __init__(self):
        self.tech = None
        self.props = {}
        self.terms = {}
        self.pins = {}
      
    def set_tech(self, tech):
        self.tech = tech
        

    def addPin(self, pinName, termName, box, layer):   
        if termName not in self.terms:
            self.terms[termName] = Term(termName)
        term = self.terms[termName]
        if pinName in self.pins:
            print("PIN PROBLEM")
            #raise ValueError(f"Pin '{pinName}' already exists.")   
        centerX = box.getCenter().x
        centerY = box.getCenter().y
        pinShapes = []
        if isinstance(layer, list):
            for lay in layer:
                rectShape = Rect(lay, box)  
                pinShapes.append(rectShape)
                pin = Pin(pinName, termName, rectShape)
                self.pins[pinName] = pin
                term.pins.append(pin)
                textShape = pya.DText(self.pinName,pya.DTrans(pya.DTrans.R0, pya.DVector(centerX, centerY)), 1, 0.05)  #origin set 0.05  0.05对应font等于0
                Shape.cell.shapes(layer.number).insert(textShape)
                
        else:
            rectShape = Rect(layer, box)
            pinShapes.append(rectShape)
            pin = Pin(pinName, termName, rectShape)
            self.pins[pinName] = pin
            term.pins.append(pin) 
                
            textShape = pya.DText(pinName, pya.DTrans(pya.DTrans.R0, pya.DVector(centerX, centerY)), 1, 0.05) 
            textShape.valign = 0    
            Shape.cell.shapes(layer.number).insert(textShape)
          
        pin = Pin(pinName, termName, pinShapes)
        self.pins[pinName] = pin
        term.pins.append(pin)
        return pin
  
    def addTerm(self, name, termType=TermType.INPUT_OUTPUT):
      
        names = name if isinstance(name, list) else [name]
        for n in names:
            if n == "" or n in self.terms:
                raise ValueError(f"Invalid or duplicate term name '{n}'.")

            nTerm = Term(n, termType)
            self.terms[n] = nTerm
            if n not in self.nets:
                self.nets[n] = Net(n)
            nTerm.net = self.nets[n]

    def setTermOrder():
        pass
     
     
    def getNets(self):

        return list(self.nets.values())

    def getShapes(self, layer=None, box=None, startLevel=0, stopLevel=0):
        
        pass

    def makeNetName(self, prefix):
        pass
 

    def makePinName(self, prefix):
        pass


    def makeTermName(self, prefix):
        pass

        
    def makeGrouping(): # Usage example: NWellRect = Rect(self.nWellLayer, self.makeGrouping().getBBox(self.tubLayer))
        pass

    @classmethod
    @abstractmethod
    def defineParamSpecs(cls, specs):
        pass

    @abstractmethod
    def setupParams(self, params):
        pass

    @abstractmethod
    def genLayout(self):
        pass
    
    def genTopology(self):
        pass
    
    def sizeDevices(self):
        pass


    