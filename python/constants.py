

########################################################################
#
# Written and verified by He.Zeng  #Add constants
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


from cni.dlo.failaction import FailAction
from cni.dlo.viewtype import ViewType


import sys

REJECT = FailAction.REJECT
ACCEPT = FailAction.ACCEPT 
USE_DEFAULT = FailAction.USE_DEFAULT

MASK_LAYOUT = ViewType.MASK_LAYOUT
SCHEMATIC= ViewType.SCHEMATIC
SCHEMATIC_SYMBOL = ViewType.SCHEMATIC
NETLIST = ViewType.NETLIST 
HIER_DESIGN =ViewType.HIER_DESIGN


INT_MAX = sys.maxsize
INT_MIN = -sys.maxsize-1




    


