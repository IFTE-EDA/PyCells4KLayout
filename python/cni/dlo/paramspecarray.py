########################################################################
#
#  written by He.Zeng  #add 6 methods
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




class ParamSpecArray:
    def __init__(self, tech=None, **kwargs):
        self.tech = tech
        self.paramSpec = {}
        for name, spec in kwargs.items():
            if isinstance(spec, tuple):
                defaultValue, docstr, constraint = (None, None, None)   
                if len(spec) >= 1:
                    self.defaultValue = spec[0]
                if len(spec) >= 2:
                    docStr = spec[1]
                if len(spec) == 3:
                    constraint = spec[2]
                self.paramSpec[name] = (self.defaultValue, docStr, constraint)
            else:
                raise ValueError(f"Invalid spec for {name}, must be a tuple of form (defaultValue, [docstr, [constraint]])")

    

    def has_key(self, name):
        return name in self.paramSpec
        
    def remove(self, name):
        if name not in self.paramSpec:
            raise ValueError(f"This name:{name} is not in the paramSpecarray")
        return self.paramSpec.pop(name)
        
    def iteritems(self):
        return ((key, value) for key, value in self.paramSpec.items())

    def iterkeys(self):
        return (key for key, value in self.paramSpec.items())

    def itervalues(self):
        return (value for key, value in self.paramSpec.items())




