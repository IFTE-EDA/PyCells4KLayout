
########################################################################
#
# Copyright 2024 IHP PDK Authors
#
#
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
# CHANGELOG: based on the version：https://github.com/IHP-GmbH/IHP-Open-PDK/commit/aa97e9551dfdc167a839dde9e99e03f96a2958fc
#
#   Author        Modification
# ------------  -------------------------------------------------
# He.Zeng      Added exists method in the Dlo class.
# He.Zeng      Modified the __call__ method, coerce_parameters method, and PyCellContext class.
# He.Zeng      Adapted some methods and descriptors from KLayout's main source: class _PCellDeclarationHelperParameterDescriptor, method init_values, method finish
# He.Zeng      Added exists and getProps methods to the Dlo class.
# He.Zeng      Added getGridResolution method to the Tech class.
########################################################################


import pya
import sys

from cni.constants import *
from cni.dlo.numeric import *
from cni.dlo.orientation import *
from cni.dlo.location import *
from cni.dlo.layer import *
from cni.dlo.pathstyle import *
from cni.dlo.signaltype import *
from cni.dlo.termtype import *
from cni.dlo.font import *
from cni.dlo.point import *
from cni.dlo.box import *
from cni.dlo.shape import *

from cni.dlo.dlogen import *
from cni.dlo.rangeconstraint import *
from cni.dlo.paramarray import *
from cni.dlo.choiceconstraint import *
from cni.dlo.stepconstraint import *
from cni.dlo.propset import *

#from ihp.cmim import *

from abc import ABC, abstractmethod




class Dlo(ABC):
    def __init__(self, libName, cellName, viewName='layout', viewType=None, mode='r', params=None):#, unsupported=HandlingStatus.ERROR
        if type(self) is Dlo:
            raise TypeError("Dlo is an ABC and cannot be instantiated")
        self.libName = libName
        self.cellName = cellName
        self.viewName = viewName
        self.viewType = viewType
        self.mode = mode
        self.params = params
        self.props = PropSet()
        self.tech = None 
        self.unsupported = unsupported 
        
    @abstractmethod
    def create_design(self):
        pass

    def getProps(self):
        return self.props
    
    # already been tested.  
    def getTech(self):
        return self.tech
        
    # already been tested.  
    @staticmethod
    def exists(name):
        parts = name.split('/')
        libraryName = parts[0]
        cellName = parts[1] if len(parts) > 1 else None
        #view_name = parts[2] if len(parts) > 2 else None
        lib = pya.Library.library_by_name(libraryName) if libraryName else None
        if not lib:
            print(f"Library {libraryName} does not exist.")
            return False
       
        layout = lib.layout()
        if cellName in layout.pcell_names():
            print(f"Cell {cellName} is registered as a PCell in the library {libraryName}.")
        else:
            print(f"Cell {cellName} is not registered in the library {libraryName}.")

        if not layout.has_cell(cellName):
            print(f"Cell {cellName} should be instantiated and added to the library{libraryName} once.")
            return False
        return True
    
  
        


class TechImpl():
   def __init__(self):
      pass
      
      
class Tech():

    techsByName = {}
    @staticmethod
    def register(tech):
        Tech.techsByName[tech.name()] = tech
    
    # already been tested.  
    @staticmethod
    def get(techLibName):
        return Tech.techsByName.get(techLibName)
        #print(Tech.techsByName[techLibName])
        
    # already been tested.         
    def getGridResolution(self):
        default_resolution = 0.001 
        tech_params = self.getTechParams()
        if 'grid' in tech_params:
            return float(tech_params['grid'])
        return default_resolution
    # already been tested.      
    def getTechParams(self): #todo involke bool local=flase in the code, if local=true, properties are taken only from the top technology database
        tech_params = self.techsByName.get(self.name, {})
        return tech_params


# adapted from from KLayout main source https://github.com/KLayout/klayout/blob/master/src/pymod/distutils_src/klayout/db/pcell_declaration_helper.py#L33
class _PCellDeclarationHelperParameterDescriptor(object):
      def __init__(self, param_index, param_name):
        self.param_index = param_index
        self.param_name = param_name
        self.value = None
      
      def __get__(self, obj, type = None):
        if obj._param_values:
          return obj._param_values[self.param_index]
        elif obj._param_states:
          return obj._param_states.parameter(self.param_name)
        else:
          return self.value
        
      def __set__(self, obj, value):
        if obj._param_values:
          obj._param_values[self.param_index] = value
        else:
          self.value = value


class PyCellContext(object):
    context_stack = []
    
    # already been tested.  
    def __init__(self, tech, cell):
      self.tech = tech
      self.cell = cell
    
    # already been tested.  
    def __enter__(self):
      PyCellContext.context_stack.append((Layer.tech, Layer.layout, Shape.cell))
      Layer.tech = self.tech
      Layer.layout = self.cell.layout()
      Shape.cell = self.cell
     
    # already been tested.  
    def __exit__(self, *params):
        Layer.tech, Layer.layout, Shape.cell = PyCellContext.context_stack.pop()
    


class PCellWrapper(pya.PCellDeclaration):
 
    def __init__(self, impl, tech):
        super(PCellWrapper, self).__init__()

        self.impl = impl
        self.impl.set_tech(tech)
        self.tech = tech
        self.param_decls = []
        self.constraints = {}
        self._param_values = []
        type(impl).defineParamSpecs(self)

    # already been tested.  
    def __call__(self, name, value, description = None, choices = None):
        # NOTE: this is calles from inside defineParamSpecs as we
        # supply the "specs" object through self.

        if type(value) is float:
            value_type = pya.PCellParameterDeclaration.TypeDouble
        elif type(value) is int:
            value_type = pya.PCellParameterDeclaration.TypeInt
        elif type(value) is str:
            value_type = pya.PCellParameterDeclaration.TypeString
        elif type(value) is bool:
            value_type = pya.PCellParameterDeclaration.TypeBoolean 
        else:
            print(f"Invalid parameter type for parameter {name} (value is {repr(value)})")
            assert(False)
            
        if isinstance(choices, ChoiceConstraint):
            if value not in choices.choices and choices.action ==REJECT:
              raise ValueError(f"Invalid value in defineParamSpecs for param '{name}': {value} (violated ChoiceConstraint:{choices}.")
            for c in choices.choices:
               param_decl = pya.PCellParameterDeclaration(name, value_type, description, value)
               param_decl.add_choice(c, c)
            self.constraints[name] = (value,choices) 
            param_index = len(self.param_decls)
            setattr(type(self), name, _PCellDeclarationHelperParameterDescriptor(param_index, name))
            
        if isinstance(choices, RangeConstraint):
            flag = True
            if choices.low is not None and Numeric(value) < choices.low:
                flag = False
            if choices.high is not None and Numeric(value) > choices.high:   
                flag = False
            if choices.low is None and Numeric(value) > choices.high:
                flag = False
            if choices.high is None and Numeric(value) < choices.low: 
                flag = False   
            if not flag and choices.action == REJECT:
                    raise ValueError(f"Invalid value in defineParamSpecs for param '{name}': {value} (violated RangeConstraint: {choices.low} <= value <= {choices.high}.")
     
            self.constraints[name] = (value,choices)
            param_index = len(self.param_decls)
            setattr(type(self), name, _PCellDeclarationHelperParameterDescriptor(param_index, name))
             
        if isinstance(choices, StepConstraint):
            flag = False
            if choices.action ==ACCEPT or choices.action ==USE_DEFAULT:
                flag = False
            elif choices.action ==REJECT: 
                if choices.limit is None:
                    flag = not ((Numeric(value) - choices.start) % choices.step == 0 and Numeric(value) >= choices.start)
                else:
                    flag = not((Numeric(value) - choices.start) % choices.step == 0 and choices.start <= Numeric(value) <= choices.limit)
            if flag:
                raise ValueError(f"Invalid value for param '{name}': {value} (violated StepConstraint:{choices}).")
            self.constraints[name] = (value,choices)
            param_index = len(self.param_decls)   
            setattr(type(self), name, _PCellDeclarationHelperParameterDescriptor(param_index, name))
        
        param_decl = pya.PCellParameterDeclaration(name, value_type, description, value)
        self._param_values.append(value)     
        self.param_decls.append(param_decl)
   
        
    def get_parameters(self):
        return self.param_decls
     
    # adapted from from KLayout main source https://github1s.com/KLayout/klayout/blob/master/src/pymod/distutils_src/klayout/db/pcell_declaration_helper.py#L33
    def init_values(self, values = None, layers = None, states = None):
        self._param_values = None
        self._param_states = None
        if states:
          self._param_states = states
        elif not values:
          self._param_values = []
          for pd in self._param_decls:
            self._param_values.append(pd.default)
        else:
          self._param_values = values
    # adapted from from KLayout main source https://github.com/KLayout/klayout/blob/master/src/pymod/distutils_src/klayout/db/pcell_declaration_helper.py#L33
    def get_values(self):
        v = self._param_values
        self._param_values = None
        return v    
    # adapted from from KLayout main source https://github.com/KLayout/klayout/blob/master/src/pymod/distutils_src/klayout/db/pcell_declaration_helper.py#L33
    def finish(self):
        self._param_values = None
        self._param_states = None

    
    def coerce_parameters(self,layout, parameters):

        self.init_values(parameters) 
        for coerceName, valConstraint in self.constraints.items():
            if isinstance(valConstraint, tuple):
                defaultValue, choices = valConstraint
                currentValue = getattr(self, coerceName, None)
                if isinstance(choices,RangeConstraint):
                    currentValue = Numeric(currentValue)
                    flag = True
                    if choices.low is not None and currentValue < choices.low:
                        flag = False
                    if choices.high is not None and currentValue > choices.high:
                        flag = False    
                    if choices.low is not None and choices.high is not None:
                        if currentValue< choices.low or currentValue> choices.high:
                            flag = False           
                    if not flag:
                        if choices.action == REJECT:
                            raise ValueError(f'Illegal user set value. Value {currentValue} violates RangeConstraint: not within the allowable range ({choices.low}, {choices.high})')  
                        elif choices.action == ACCEPT:
                            if choices.low is not None and choices.high is not None:
                                newValue = max(min(currentValue, choices.high), choices.low)
                            elif choices.low is None:
                                newValue = min(currentValue, choices.high)
                            elif choices.high is None:
                                newValue = max(currentValue, choices.low)
                            setattr(self, coerceName, newValue)    
                        elif choices.action == USE_DEFAULT:
                            setattr(self, coerceName, defaultValue)
                    else:
                        continue        
                elif isinstance(choices, ChoiceConstraint):
                    if choices.action ==REJECT:
                        if currentValue not in choices.choices:
                            raise ValueError(f"Invalid value for param '{coerceName}': violated ChoiceConstraint.")
                        else:
                            continue
                    elif choices.action == ACCEPT or choices.action == USE_DEFAULT:  
                        setattr(self, coerceName, defaultValue)

                elif isinstance(choices, StepConstraint):
                    currentValue = Numeric(currentValue)
                    if choices.action == REJECT:
                        if choices.limit is None:
                            if not ((currentValue - choices.start) % choices.step == 0 and currentValue >= choices.start):
                                raise ValueError(f'Illegal value for parameter{coerceName}, Value {currentValue} does not meet StepConstraint {choices}.')
                        else:
                            if not ((currentValue - choices.start) % choices.step == 0 and choices.start <= currentValue <= choices.limit):
                                raise ValueError(f'Illegal value for parameter{coerceName}, Value {currentValue} does not meet StepConstraint {choices}.')
                    elif choices.action == ACCEPT:
                        newValue = choices.start + ((currentValue - choices.start) // choices.step) * choices.step
                        newValue = min(max(choices.start, adjustedValue), choices.limit) if choices.limit is not None else newValue
                        setattr(self, coerceName, newValue)
                    elif choices.action == USE_DEFAULT:
                        setattr(self, coerceName, defaultValue)
              
            else:
                raise ValueError(f"Invalid temp parameter: 'valConstraint' should be a tuple")
        parameters = self.get_values()  
        self.finish()
        return parameters
    
    def params_as_hash(self, parameters):
        return dict(zip([param.name for param in self.param_decls], parameters))
        
    def display_text(self, parameters):
        params = self.params_as_hash(parameters)
        return type(self.impl).__name__
        
    def produce(self, layout, layers, parameters, cell):
        params = self.params_as_hash(parameters)
        with (PyCellContext(self.tech, cell)):
            self.impl.setupParams(params)
            
            self.impl.genLayout()
            
          

