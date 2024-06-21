
########################################################################
#
# written a by He.Zeng  #add 2 methods
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



from cni.constants import REJECT, ACCEPT, USE_DEFAULT


class RangeConstraint:
    # already been tested.  
    def __init__(self, *args, **kwargs):
        self.low = None
        self.high = None
        self.resolution = None
        self.action = REJECT
    
        if len(args) < 2:
            raise ValueError("Invalid object of RangeConstraint:At least two arguments need to be passed.")
        if len(args)>4:
            raise ValueError("Invalid object of RangeConstraint:at most four positional to be passed.")
            
        if args[0] is None or isinstance(args[0], (int, float)):
            self.low = args[0]
        else:
            raise ValueError("Invalid low bound")
        if args[1] is None or isinstance(args[1], (int, float)):
            self.high = args[1]
        else:
            raise ValueError("Invalid high bound")
        if self.low is None and self.high is None:
            raise ValueError("Invalid object of RangeConstraint: No bound values")
               
        self.resolution = kwargs.get("resolution", None)
        self.action = kwargs.get("action", REJECT)
        if len(args)== 3:
            if isinstance(args[2], (int, float, type(None))):
                self.resolution = args[2]
            elif args[2] in [REJECT, ACCEPT, USE_DEFAULT]:
                self.action =args[2]
            else:
                raise ValueError("Invalid object of RangeConstraint:The third parameter should be of type int or float")
        if len(args) == 4: 
            if args[3] in [REJECT, ACCEPT, USE_DEFAULT] and isinstance(args[2], (int, float, type(None))):
                self.action = args[3]
                self.resolution = args[2]    
            else:
                raise ValueError("Invalid object of RangeConstraint:The fourth parameter should be in the range [REJECT, ACCEPT, USE_DEFAULT]")
    
    # already been tested.   
    def __str__(self):
        return f"RangeConstraint(Low={self.low}, High={self.high}, Resolution={self.resolution}, Action={self.action})"
        



       