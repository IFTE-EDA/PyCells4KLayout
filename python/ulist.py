########################################################################
#
# written and verified by He.Zeng  #add 12 method 
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




from cni.dlo.point import *
from cni.dlo.box import *
from cni.dlo.layer import *



class UListMeta(type): 
    def __getitem__(cls, itemType): 
        
        if itemType not in ulist.baseTypes:  
            raise TypeError(f"Unsupported item type:{itemType}")
        class SubUList(ulist):
            def __init__(self, *args):
                super().__init__(itemType,*args)  
        return SubUList


class ulist(list, metaclass=UListMeta):
    baseTypes = {int, str, float, complex, list, Layer, Point, Box}
    
    # already been tested.  
    def __init__(self, itemType, *args):
        self.itemType = itemType
        super().__init__(*args)       
    # already been tested.  
    def __str__(self):
        return '[' + ', '.join(str(item) for item in self) + ']'  
    
    # already been tested.  
    def __eq__(self, other):
        if not isinstance(other, (list, ulist)):
            return False
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if self[i] != other[i]:
                return False
        return True 
        
    # already been tested.  
    def copy(self):
        newUlist = ulist[self.itemType]()
        for i in self:
            newUlist.append(i)
        return newUlist
    # already been tested.  
    def _checkType(self, item):
        if not isinstance(item, self.itemType):
            print(item, type(item), self.itemType)
            #raise TypeError(f"Expected item of type'{self.itemType.__name__}'")
    # already been tested.  
    def append(self, item):
        self._checkType(item)
        super().append(item)
    # already been tested.  
    def count(self, item):
        countNum = 0 
        for i in self:
            if i == item:
                countNum += 1 
        return countNum
    # already been tested.  
    def extend(self, otherlist):
        for item in otherlist:
            self._checkType(item)
        super().extend(otherlist)
        
    # already been tested.  
    def index(self, item, *args):
        if item in self:
            return super().index(item, *args)
        else:
            raise ValueError(f"Item '{item}' not found in the list.")
    # already been tested.         
    def insert(self, index, item):
        self._checkType(item)
        super().insert(index, item)
    # already been tested.  
    def pop(self, index=-1):
        return super().pop(index)
    # already been tested.  
    def remove(self, item):
        self._checkType(item)
        if item in self:
            super().remove(item)
        else:
            print(f"Item {item} not found in the list.")
    # already been tested.  
    def reverse(self):
        super().reverse()

   

