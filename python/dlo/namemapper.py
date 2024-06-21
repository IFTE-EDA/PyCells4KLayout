
########################################################################
#
#  written by He Zeng  #add 2 methods, the NameMapper class need to be further improved
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

class NameMapper:

    # the self.obj may not existed in the original NameMapper class
    def __init__(self, obj):
        if not (isinstance(obj, (str, dict)) or callable(obj)):
            raise TypeError(f"Unsupported argument type for NameMapper object")
        self.obj = obj
    
    # this method is according to documentation from PyCell Studio, but need to be tested.
    def map(self, name):
        if isinstance(self.obj, str):
            nameSplit = self.obj.split(':')
            if len(nameSplit) == 2:
                subPrefix, addPrefix = nameSplit[0].split('/')
                subSuffix, addSuffix = nameSplit[1].split('/')
                if name.startswith(subPrefix):
                    name = addPrefix + name[len(subPrefix):]
                if name.endswith(subSuffix):
                    name = name[:-len(subSuffix)] + addSuffix
            elif len(nameSplit) == 1:
                if '/' in nameSplit[0]:
                    subSuffix, addSuffix = nameSplit[0].split('/')
                    if name.endswith(subSuffix):
                        name = name[:-len(subSuffix)] + addSuffix
                else:
                    raise ValueError("Invalid argument for NameMapper class")
            else:
                raise ValueError("Invalid argument for NameMapper class")                       
        elif isinstance(self.obj, dict): 
            name = self.obj.get(name, name)
        elif callable(self.obj):
            name = self.obj(name) 
        return name
