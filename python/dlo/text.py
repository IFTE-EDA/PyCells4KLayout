

########################################################################
#
#  written and verified by He.Zeng  #add 12 methods 
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



from cni.dlo.shape import *
from cni.dlo.font import *
from cni.dlo.layer import *
from cni.dlo.location import *
from cni.dlo.point import *
from cni.dlo.box import *
from cni.dlo.orientation import *
from cni.dlo.snaptype import *
import pya


import importlib
importlib.invalidate_caches()
import cni.dlo.point
importlib.reload(cni.dlo.point)

importlib.invalidate_caches()
import cni.dlo.orientation
importlib.reload(cni.dlo.orientation)


class Text(Shape):
    def __init__(self, layer, text, origin, height, location=Location.CENTER_CENTER, orient=Orientation.R0, font=Font.STICK, overbar=False, visible=True, drafting=False):
        # In both the PyCell API and Klayout API, the fonts "stick" and "Gothic" are commonly supported.
        # In this project, the default font is set to default (0) for further verification of layouts.
        self.layerid = layer
        self.text = text
        #Point.isInstPoint(origin)
        self.origin = origin
        self.height = height
        self.location =location
        self.orient = orientMapping[orient.value]
        self.font = font
        self.overbar = overbar
        self.visible = visible
        self.drafting = drafting
        self.dtextShape = None  
        self._updateText() 

       
    # already been tested.  
    def setOrigin(self, new_origin):
        Point.isInstPoint(new_origin)
        if self.origin != new_origin:
            self.origin = new_origin
            self._updateText()
            

    def _updateText(self):
        # for the font， 0 is default font, 2 is stick font,
        #It is recommended to use font '0' for verification of layouts, when executing PyCell in KLayout and PyCell Studio.
        tempDtext = pya.DText(self.text ,pya.DTrans(self.orient, pya.DVector(0, 0)), self.height, 0)
        tempDtext.x=self.origin.x
        tempDtext.y=self.origin.y
        dbox = self._calculateTextBbox().transformed(pya.DTrans(self.orient, pya.DVector(self.origin.x, self.origin.y))) 
        super().__init__(layer= self.layerid, bbox =Box(dbox))
        locationMap = {Location.LOWER_LEFT: self.bbox.lowerLeft(), Location.CENTER_LEFT: self.bbox.centerLeft(), Location.UPPER_LEFT: self.bbox.upperLeft(),
                        Location.LOWER_CENTER: self.bbox.lowerCenter(), Location.CENTER_CENTER: self.bbox.centerCenter(), Location.UPPER_CENTER: self.bbox.upperCenter(),
                        Location.LOWER_RIGHT: self.bbox.lowerRight(), Location.CENTER_RIGHT: self.bbox.centerRight(), Location.UPPER_RIGHT: self.bbox.upperRight(),}
      
        
        vertex = locationMap.get(self.location, self.bbox.centerCenter())
        dVector = pya.DVector(self.origin.x, self.origin.y)-pya.DVector(vertex.x, vertex.y) 
        halvalMap = {Location.LOWER_LEFT: (0,2), Location.CENTER_LEFT: (0,1), Location.UPPER_LEFT: (0,0),
                        Location.LOWER_CENTER: (1,2), Location.CENTER_CENTER: (1,1), Location.UPPER_CENTER: (1,0),
                        Location.LOWER_RIGHT: (2,2), Location.CENTER_RIGHT: (2,2), Location.UPPER_RIGHT: (2,0),}                
        
        tempDtext.halign, tempDtext.valign = halvalMap.get(self.location, (1,1))
        if self.dtextShape is not None:
            self.dtextShape = Shape.cell.shapes(self.layerid.number).replace(self.dtextShape, tempDtext)
        else:
            self.dtextShape = Shape.cell.shapes(self.layerid.number).insert(tempDtext)   
        dbox = dbox.moved(dVector)

        self.bbox = Box(dbox)
        
        
    # already been tested. 
    def getAlignment(self):
          return self.location
       
    # already been tested.   
    def setAlignment(self, location):
        self.location = location
        self._updateText() 


    def getFont(self):
        return self.font

    def setFont(self, font):
        raise Exception("Changing the font of text object is not supported in this project.")

    # already been tested. 
    def getHeight(self):
        return self.height

    # already been tested. 
    def setHeight(self, height):
        self.height = height
        self._updateText()

    # already been tested. 
    def getOrientation(self):
        return self.orient
    
    # already been tested. 
    def setOrientation(self, orient):
      
        self.orient = orientMapping[orient.value]
        self._updateText()

    # already been tested. 
    def getOrigin(self):
        return self.origin

    # already been tested. 
    def getText(self):
        return self.text
    # already been tested. 
    def setText(self, text):
        self.text = text
        self._updateText()
    

    def hasOverbar(self):
        return self.overbar

    def setOverbar(self, overbar):
        raise Exception("Not implemented yet!,lack the detail of setDrafting method")

    def isDrafting(self):
        return self.drafting

    def setDrafting(self, drafting):
        print("Not implemented yet!,lack the detail of setDrafting method")
        #raise Exception("Not implemented yet!,lack the detail of setDrafting method")

    def isVisible(self):
        return self.visible

    def setVisible(self, visible):
        raise Exception("Not implemented yet!")
     

        
    def _calculateTextBbox(self): 
        #Note: This method provides a rough estimate the Box coordinates given the string length and heightand and the result is not exact.
        length = len(self.text)
        height=self.height*1.06
        left = SnapType.round(0.0005, -0.002 * length - 6.112 * height + 0.029)
        bottom = SnapType.round(0.0005, -1.0 * height)
        right = SnapType.round(0.0005, 0.002 * length + 6.135 * height - 0.029)
        top = SnapType.round(0.0005, 0.500 * height + 0.001)
        dBox= pya.DBox(left, bottom, right, top)
        return dBox

