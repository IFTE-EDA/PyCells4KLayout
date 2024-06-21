
########################################################################
#
#  written by He.Zeng  The function for mapping pin, term and net is currently non-functional and requires further investigation.
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

from cni.dlo.termtype import * 
from cni.dlo.net import * 


class Term:
    _terms = {}  

    def __init__(self, termName, termType=TermType.INPUT_OUTPUT):
        if termName == "" or termName in Term._terms:
            print("\a")
            #raise ValueError("Invalid or duplicate term name.")
        self.name = termName
        self.type = termType
        self.pins = []
        self.net = Net(termName)
        Term._terms[termName] = self
        
    @staticmethod
    def find(termName):
        return Term._terms.get(termName, None)

    def getNet(self):
        return self.net

    def addPin(self, pin):
        if pin not in self.pins:
            self.pins.append(pin)
            pin.setTerm(self)

    def removePin(self, pin):
        if pin in self.pins:
            self.pins.remove(pin)

    def getNumPins(self):
        return len(self.pins)

    def setName(self, newName):
        if newName == "" or newName in Term._terms:
            print("\a")
            #raise ValueError("Invalid or duplicate new term name.")
        del Term._terms[self.name]
        self.name = newName
        self.net.setName(newName)
        Term._terms[newName] = self

    def getName(self):
        return self.name

    def setTermType(self, termType):
        self.type = termType

    def getTermType(self):
        return self.type


    def destroy(self):
        for pin in self.pins:
            pin.destroy()
        del Term._terms[self.name]
