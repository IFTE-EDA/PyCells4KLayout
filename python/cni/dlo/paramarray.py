
########################################################################
#
#  written by He.Zeng  #add 16 methods
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


class ParamArray:
    def __init__(self, *args, **kwargs):
        self.params = {}
        if args and not kwargs:
            for arg in args:
                if isinstance(arg, list) and len(arg) == 3:
                    self.params[arg[0]] = (arg[1], arg[2])
                else:
                    raise ValueError("Each arg must be a list of form “name,type, value")
        for name, value in kwargs.items():
            self.params[name] = value
            
    # already been tested.  
    def __getitem__(self, name):
        return self.params[name] 
     
    # already been tested.  
    def __setitem__(self, name, value):
        self.params[name] = value
    
    # already been tested.     
    def __contains__(self, key):
        return key in self.params
    
    # already been tested.  
    def __str__(self):
        paramArrayStr = ','.join(f"{key}='{value}'" for key, value in self.params.items())
        return f"ParamArray({paramArrayStr})"
    
    # already been tested.  
    def add(self, *args, **kwargs):
        if args and len(args) == 2:
            if args[0] in self.params:
                raise ValueError(f"Parameter '{args[0]}' already exists.")
            self.params[args[0]] = args[1]
        elif kwargs and len(kwargs) == 1:
            for name, value in kwargs.items():
                if name in self.params:
                    raise ValueError(f"Parameter '{name}' already exists.")
                self.params[name] = value
        else:
            raise ValueError("Invalid arguments, two forms are supported: single (name, value) or single (name=value)")
   
    # already been tested.  
    def get(self, name):
        if isinstance(name, str):
            if name not in self.params:
                raise ValueError(f"This name:{name} is not in the paramarray")
            return self.params[name]
        elif isinstance(name, tuple):
            undefinedKeys = [name1 for name1 in name if name1 not in self.params]
            if undefinedKeys:
                raise ValueError(f"These names {', '.join(undefinedKeys)} are not in the paramarray.")
            return tuple(self.params[name1] for name1 in name)
        else:
            raise ValueError("Parameter name must be a string or a tuple of strings.")

    # already been tested.  
    def has_key(self, name):
        return name in self.params
    
    # already been tested.  
    def iteritems(self):
        return ((key, value) for key, value in self.params.items())

    # already been tested.  
    def iterkeys(self):
        return (key for key in self.params.keys())
    
    # already been tested.  
    def itervalues(self):
        return (value for value in self.params.values())
    
    # already been tested.  
    def remove(self, name):
        if name not in self.params:
            raise ValueError(f"This name:{name} is not in the paramarray")
        return self.params.pop(name)

    def reset(self):
        self.params.clear()

    def set(self, *args, **kwargs):
        if args and len(args) == 2:
            self.params[args[0]] = args[1]
        elif kwargs and len(kwargs) == 1:
            for name, value in kwargs.items():
                self.params[name] = value
        else:
            raise ValueError("Invalid arguments, two forms are supported: single (name, value) or single (name=value)")
            
    def setFromSpecs(self, specs):
         raise ValueError("unimplemented ")

    def update(self, other):
        if not isinstance(other, ParamArray):
            raise ValueError("The argument must be an object of class ParamArray.")   
        for key, value in other.params.items():
            self[key] = value
    



