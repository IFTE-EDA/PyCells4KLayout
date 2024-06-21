########################################################################
#
#  written and verified by He.Zeng  #add 2 methods 
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
from cni.ulist import *

class ChoiceConstraint:
    def __init__(self, choices, action = REJECT):
        if action not in [REJECT, ACCEPT, USE_DEFAULT]:
            raise ValueError("Action must be one of: REJECT, ACCEPT, USE_DEFAULT.")
        self.choices = ulist[str](choices)
        self.action = action
    
    def __str__(self):
        choices_str = ", ".join(map(str, self.choices))
        return f"ChoiceConstraint(choices=[{choices_str}], action={self.action})"
        



