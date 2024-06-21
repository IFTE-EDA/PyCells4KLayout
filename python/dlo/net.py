########################################################################
#
#  written by He.Zeng, The function for mapping shapes with nets is currently non-functional and requires further investigation.
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





class Net:
    _nets = {}  
    shapeMapNet = {}
    
    def __init__(self, netName, sigType=SignalType.SIGNAL, isGlobal=False):
        if not isinstance(netName, str):
            raise ValueError(f"netName '{netName}' must be a string.")
        if netName == "" or netName in Net._nets:
            print("\a")  
            #raise ValueError("Invalid or duplicate net name.")
        self.name = netName
        self.signalType = sigType
        self.globalNet = isGlobal
        self.shapes = []
        self.terms = []
        Net._nets[netName] = self

    @staticmethod
    def find(name=""):
        return Net._nets.get(name, None)

    @staticmethod
    def findCreate(name):
        return Net._nets.get(name, Net(name))
        
    def addShape(self, shapes):
        if not isinstance(shapes, list):
            shapes = [shapes]
        for shape in shapes:
            if shape in Net.shapeMapNet:
                raise ValueError("Shape is already associated with another net.")
            Net.shapeMapNet[shape] = self
            self.shapes.append(shape)

    def destroy(self):
        for term in self.terms:
            term.destroy()
        del Net._nets[self.name]

    def getBit(self, index):
        return self

    def getInstPins(self):
       
        pass

    def getInstTerms(self):
        
        pass

    def getName(self):
        return self.name

    def getNumBits(self):
        pass

    def getShapes(self):
        return self.shapes

    def getSignalType(self):
        return self.signalType

    def getPins(self):
        pins = []
        for term in self.terms:
            pins.extend(term.pins)
        return pins

    def getTerm(self):
        
        return self.terms[0] if self.terms else None

    def getVias(self):
        
        pass

    def isGlobal(self):
        return self.globalNet

    def removeShape(self, shapes):
        
        pass

    def setGlobal(self, isGlobal):
        self.globalNet = isGlobal

    def setName(self, name):
        if name == "" or name in Net._nets:
            print("\a")
            #raise ValueError("Invalid or duplicate new net name.")
        del Net._nets[self.name]
        self.name = name
        Net._nets[name] = self
        for term in self.terms:
            term.setName(name)

    def setNetOverride(self, assignmentName, netName):
        pass

    def setSignalType(self, sigType):
        self.signalType = sigType

