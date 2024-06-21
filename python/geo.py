
########################################################################
#
# written by He Zeng  #add 4 method
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
# Comments by He.Zeng: These four methods should be used together with the regionToGroup method from the ihp.geometry module.
# Comments by He.Zeng: For example: The dbLayerXorList method calls the fgXor method from cni.geo and then uses regionToGroup to convert the result into a Grouping object.
#
########################################################################

from cni.dlo.shapefilter import *
import pya
from cni.dlo.grouping import *
from cni.dlo.rect import *
from cni.dlo.polygon import *


'''
PhysicalComponent methods: 'abut', 'alignEdge', 'alignEdgeToPoint', 'alignLocation',
'alignLocationToPoint', 'fgAbut', 'fgAddEnclosingPolygon', 'fgDeriveLayer', 'fgMinSpacing',
'fgAnd', 'fgOr', 'fgNot', 'fgXor', 'fgSize', 'fgFill', 'fgMerge', 'fgPlace', 'getSpacing', 'place
'''
def abut():
    pass

    
def fgAnd(comps1, comps2, resultLayer, cell=None, filter1=ShapeFilter(), filter2=None, grid=None):
    comp1Region = pya.Region()
    if isinstance(comps1, Grouping):
        for comp in comps1.getComps():
            comp1Region.insert(pya.Region(comp.shape.polygon))          
    else:
        comp1Region = pya.Region(comps1.shape.polygon)
    
    comp2Region = pya.Region()
    if isinstance(comps2, list):
        for item in comps2:
            comp2Region.insert(pya.Region(item.shape.polygon))          
    elif isinstance(comps2, Grouping):
        for comp in comps2.getComps():
            comp2Region.insert(pya.Region(comp.shape.polygon))  
    elif isinstance(comps2,(Rect,Polygon)):
        comp2Region.insert(pya.Region(comps2.shape.polygon))
        
    andListRegion = comp1Region.and_(comp2Region)
    return andListRegion



    
def fgOr(comps1, comps2, resultLayer, cell=None, filter1=ShapeFilter(), filter2=None, grid=None):
    comp1Region = pya.Region()
    if isinstance(comps1, Grouping):
        for comp in comps1.getComps():
            comp1Region.insert(pya.Region(comp.shape.polygon))          
    else:
        comp1Region = pya.Region(comps1.shape.polygon)
    
    comp2Region = pya.Region()
    if isinstance(comps2, list):
        for item in comps2:
            comp2Region.insert(pya.Region(item.shape.polygon))          
    elif isinstance(comps2, Grouping):
        for comp in comps2.getComps():
            comp2Region.insert(pya.Region(comp.shape.polygon))  
    elif isinstance(comps2,(Rect,Polygon)):
        comp2Region.insert(pya.Region(comps2.shape.polygon))
        
    orListRegion = comp1Region.or_(comp2Region)
    return orListRegion


    
    
def fgXor(comps1, comps2, resultLayer, cell=None, filter1=ShapeFilter(), filter2=None, grid=None):
    comp1Region = pya.Region()
    if isinstance(comps1, Grouping):
        for comp in comps1.getComps():
            comp1Region.insert(pya.Region(comp.shape.polygon))          
    else:
        comp1Region = pya.Region(comps1.shape.polygon)
    
    comp2Region = pya.Region()
    if isinstance(comps2, list):
        for item in comps2:
            comp2Region.insert(pya.Region(item.shape.polygon))          
    elif isinstance(comps2, Grouping):
        for comp in comps2.getComps():
            comp2Region.insert(pya.Region(comp.shape.polygon))  
    elif isinstance(comps2,(Rect,Polygon)):
        comp2Region.insert(pya.Region(comps2.shape.polygon))
        
    xorListRegion = comp1Region.xor(comp2Region) 
    return xorListRegion    

def fgNot(comps1, comps2, resultLayer, cell=None, filter1=ShapeFilter(), filter2=None, grid=None):
    comp1Region = pya.Region()
    if isinstance(comps1, Grouping):
        for comp in comps1.getComps():
            comp1Region.insert(pya.Region(comp.shape.polygon))          
    else:
        comp1Region = pya.Region(comps1.shape.polygon)
    
    comp2Region = pya.Region()
    if isinstance(comps2, list):
        for item in comps2:
            comp2Region.insert(pya.Region(item.shape.polygon))          
    elif isinstance(comps2, Grouping):
        for comp in comps2.getComps():
            comp2Region.insert(pya.Region(comp.shape.polygon))  
    elif isinstance(comps2,(Rect,Polygon)):
        comp2Region.insert(pya.Region(comps2.shape.polygon))
        
    notListRegion = comp1Region.not_(comp2Region) 
    return notListRegion   



def fgMerge():
  # TODO: implement
    pass

def place(): # Usage Example: place(gateContact, NORTH, gateRect, 0)
    pass

def fgAddEnclosingPolygon():
    pass
  
def place():
    pass
    
