
########################################################################
#
#  written by He.Zeng  #add 7 methods. The function for mapping shapes with pins is currently non-functional and requires further investigation.
#  The Pin object now contains a Rect object and a text label: already tested.
#  Regarding the mapping of shapes with pins, it may be necessary to verify the OpenAccess (OA) implementation in other EDA tools.
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


from collections import OrderedDict
from cni.dlo.term import *
from cni.dlo.shape import *

class Pin:
    _pinsName = OrderedDict()
    shapeMapPin = {} 

    def __init__(self, pinName, termName, shape=None):
        if pinName in Pin._pinsName:
            print("Problem on pins")
            #raise ValueError("Pin with this name already exists.")

        self.name = pinName
        if termName in Term._terms:
            self.term = Term._terms[termName]
        else:
            self.term = Term(termName)
        self.net = self.term.getNet()
        self.shapes = [shape] if shape else []
        Pin._pinsName[pinName] = self
        
        if shape:
            self.addShape(shape)
      
    def getNet(self):
        return self.net

    def setTerm(self, term):
        self.term = term
        self.net = term.getNet() if term else None

    @staticmethod
    def find(name=""):   #test code Pin.find('pin1').
        if name:
            return Pin._pinsName.get(name, None)
        else:
            return list(Pin._pinsName.values())[0] if Pin._pinsName else None

    def setName(self, name):
        if name in Pin._pinsName:
            print("Problem on pins")
            #raise ValueError("Pin with this name already exists.")
        del Pin._pinsName[self.name]
        self.name = name
        Pin._pinsName[name] = self


    def addShape(self, shapes):
        if not isinstance(shapes, list):
            shapes = [shapes]

        for shape in shapes:
            if shape in Pin.shapeMapPin:
                print("Shape is already associated with another pin.")
                #raise ValueError("Shape is already associated with another pin.")
            Pin.shapeMapPin[shape] = self
            self.shapes.append(shape)
