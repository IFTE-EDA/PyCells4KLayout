
########################################################################
#
#  written by He Zeng  #add 39 methods
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
from cni.dlo.box import *
from cni.dlo.gapstyle import *
from cni.dlo.grouping import *
from cni.dlo.polygon import *
#import copy


class Rect(Shape):
    # already been tested.   
    def __init__(self, layerid, box):
        
        super().__init__(layer = layerid, bbox = box.fix())
        self._desRectFlag = False
        self._updateRect()
        
    def _updateRect(self):
        if self.shape is not None:
            self.shape = Shape.cell.shapes(self.layer.number).replace(self.shape, self.bbox.dbox)  
        else:
            self.shape = Shape.cell.shapes(self.layer.number).insert(self.bbox.dbox) 
    

    # already been tested.   
    def clone(self):
      
        if self._desRectFlag:
            raise ValueError("Rect: object is destroyed")
            
        nlayer = self.layer 
        nbbox = Box(self.bbox.left, self.bbox.bottom, self.bbox.right, self.bbox.top) 
        clonedRect = Rect(nlayer, nbbox)   
        return clonedRect
        
    # already been tested.       
    def getBBox(self):
        return self.bbox
    
    # already been tested.      
    def __str__(self): 
        
        if self._desRectFlag is True:
            return f"Rect: object is destroyed"
        else:
            return f"Rect({self.layer}, {self.bbox})"  
        
        return f"Rect({self.layer}, {self.bbox})" 
    
    # already been tested.   
    def destroy(self): 
        #self.shape._destroy()
        if not self.shape.is_null():
            self.shape.delete()
        self._desRectFlag = True    
            
    def moveTo(self, destination, loc = Location.CENTER_CENTER):  
        newbox = self.bbox.moveTo(destination, loc = Location.CENTER_CENTER)
        self.setBBox(newbox) 
        return self
        
    def moveBy(self,x,y):
        newbox = self.bbox.moveBy(x,y)
        self.setBBox(newbox) 
        return self
        
    # already been tested.        
    def transform(self, trans): 
        newbox = self.bbox.transform(trans)
        self.setBBox(newbox)
        return self
        
    # already been tested.   
    def rotate90(self, origin = Point()):
        r90box= self.bbox.rotate90(origin)
        self.setBBox(r90box)
        return self
    
    # already been tested.   
    def rotate180(self, origin = Point()):
        r180box= self.bbox.rotate180(origin)
        self.setBBox(r180box)
        return self
    #already test 
    def rotate270(self, origin = Point()):
        r270box= self.bbox.rotate270(origin)
        self.setBBox(r270box)
        return self
   

   
    # already been tested.       
    def fgXor(self, comp, resultLayer, filter1=ShapeFilter(), filter2=None, grid=None):
        dregion = pya.Region(comp.shape.polygon)
        nregion = pya.Region(self.shape.polygon).xor(dregion)
        return nregion
        
     # already been tested.     
    def fgOr(self, comp, resultLayer, filter1=ShapeFilter(), filter2=None, grid=None):
        dregion = pya.Region(comp.shape.polygon)  
        nregion = pya.Region(self.shape.polygon).or_(dregion)  
        return nregion   
        
    # already been tested.   
    def fgAnd(self, comp, resultLayer, filter1=ShapeFilter(), filter2=None, grid=None):
        dregion = pya.Region(comp.shape.polygon)  
        nregion = pya.Region(self.shape.polygon).and_(dregion) 
        return nregion  
        
    # already been tested.    
    def fgNot(self, comp, resultLayer, filter1=ShapeFilter(), filter2=None, grid=None):
        dregion = pya.Region(comp.shape.polygon)  
        nregion = pya.Region(self.shape.polygon).not_(dregion)  
        return nregion  
     
    # already been tested.       
    @property
    def left(self):
        return self.bbox.left
        
    # already been tested.      
    @left.setter
    def left(self, value):
        self.bbox.left = value
        if self.bbox.isInverted():
            raise ValueError(f"New left value {value} cannot be greater than the right value {self.right}.")
        self._updateRect()

    # already been tested.   
    @property
    def bottom(self):
        return self.bbox.bottom

    # already been tested.   
    @bottom.setter
    def bottom(self, value): 
        self.bbox.bottom = value
        if self.bbox.isInverted():  
            raise ValueError(f"New bottom value {value} cannot be higher than the top value {self.top}.")
        self._updateRect()
    
    # already been tested.    
    @property
    def right(self):
        return self.bbox.right
        
    # already been tested.        
    @right.setter
    def right(self, value):
        self.bbox.right = value
        if self.bbox.isInverted():  
            raise ValueError(f"New right value {value} cannot be less than the left value {self.left}.")
        self._updateRect()

    # already been tested.   
    @property
    def top(self):
        return self.bbox.top
        
    # already been tested.   
    @top.setter
    def top(self, value): 
        self.bbox.top = value
        if self.bbox.isInverted():
            raise ValueError(f"New top value {value} cannot be lower than the bottom value {self.bottom}.")
        self._updateRect()
        
   

    def getHeight(self):
        return self.bbox.getHeight()
     
    #modify self # already been tested.   
    def expand(self, coord): 
        self.bbox.expand(coord)
        return self
    #modify self，return self, already been tested.   
    def expandDir(self, dir, coord):
        self.bbox.expandDir( dir, coord) 
        return self
      
    
    @staticmethod
    def fillBBoxWithRects(layer, box, width=None, height=None, spaceX=None, spaceY=None, gapStyle=GapStyle.MINIMUM, group=None):
        # Assuming default minimum design rule values, should get from technology file
        defaultMinWidth = 0.01
        defaultMinHeight = 0.001
        defaultMinSpaceX = 0.005
        defaultMinSpaceY = 0.005
        def calcNumRects(length, rectSize, spacing, mimSpacing):
            numRect = 0
            currentLength = rectSize
            while currentLength <= length -mimSpacing*2:
                numRect += 1
                currentLength  += rectSize + spacing
            if numRect < 1:
                raise ValueError("Cannot fit any rectangle within the given Box")
            return numRec
        width = width if width is not None else defaultMinWidth
        height = height if height is not None else defaultMinHeight
        spaceX = spaceX if spaceX is not None else defaultMinSpaceX
        spaceY = spaceY if spaceY is not None else defaultMinSpaceY
        numRectsX = calcNumRects(box.getWidth(), width, spaceX, defaultMinSpaceX)
        numRectsY = calcNumRects(box.getHeight(), height, spaceY, defaultMinSpaceY)
        rects = []
        if gapStyle == GapStyle.DISTRIBUTE:
            
            newSpaceX = (box.getWidth()- defaultMinSpaceX*2 - numRectsX*width)/(numRectsX-1) if numRectsX !=1 else 0
            startX = box.getCenterX() -numRectsX* width /2 - (numRectsX-1)* newSpaceX/2 

            newSpaceY = (box.getHeight() - defaultMinSpaceY * 2 - numRectsY * height) / (numRectsY - 1)  if numRectsY !=1 else 0
            startY = box.getCenterY() - numRectsY * height / 2 - (numRectsY - 1) * newSpaceY / 2 
            for i in range(numRectsX):
                for j in range(numRectsY):
                    rectX = startX + i * (width + newSpaceX)
                    rectY = startY + j * (height + newSpaceY)
                    rect = Rect(layer, Box(rectX, rectY, rectX + width, rectY + height))
                    rects.append(rect)
                    if group:
                        pass
                        #group.add(rect)
        elif gapStyle == GapStyle.MIN_CENTER:
            startX = box.getCenterX() -numRectsX* width /2 - (numRectsX-1)* spaceX/2
            startY = box.getCenterY() - numRectsY * height / 2 - (numRectsY - 1) * spaceY / 2
            
            for i in range(numRectsX):
                for j in range(numRectsY):
                    rectX = startX + i * (width + spaceX)
                    rectY = startY + j * (height + spaceY)
                    # Create the rectangle here, potentially as a Rect object or another suitable representation
                    rect = Rect(layer, Box(rectX, rectY, rectX + width, rectY + height))
                    rects.append(rect)
                    if group:
                        pass
       
        elif gapStyle == GapStyle.MINIMUM: 
            for i in range(numRectsX):
                for j in range(numRectsY):
                    rectX = box.left + defaultMinSpaceX + i * (width + spaceX)
                    rectY = box.bottom + defaultMinSpaceY + j * (height + spaceY)
                    # Create the rectangle here, potentially as a Rect object or another suitable representation
                    rect = Rect(layer, Box(rectX, rectY, rectX + width, rectY + height))
                    rects.append(rect)
                    if group:
                        pass
        else:
             raise ValueError("Invalid gapStyle: " + str(gapStyle))
        return rects
    
    # already been tested.   
    def getBottom(self):
        return self.bbox.bottom
        
    # already been tested.   
    def getCoord(self, dir):
        return self.bbox.getCoord(dir)

    # already been tested.   
    def getLeft(self):
        return self.bbox.left

    # already been tested.   
    def getRight(self):
        return self.bbox.right

    # already been tested.   
    def getTop(self):
        return self.bbox.top

    # already been tested.   
    def getWidth(self):
        return self.bbox.getWidth()

    # already been tested.   
    def setBBox(self, box):
        self.bbox = box
        self._updateRect()
       
    def setBottom(self, value):
        self.bottom = value

    def setCoord(self, dir, coord):
        self.bbox.setCoord(dir, coord)
        self._updateRect()
     
    def setLeft(self, value):
        self.left = value
    
    def setRight(self, value):
        self.right = value
       
    def setTop(self, value):
        self.top = value
 
           
            
            
