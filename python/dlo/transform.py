
########################################################################
#
#  written and verified by He.Zeng  #add 9 methods 
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

from cni.dlo.point import *
from cni.dlo.orientation import *


class Transform():
    # already been tested. 
    def __init__(self, *args):
        '''
        self.offset = Point(0,0)
        self.orientation = Orientation.R0
        '''
        
        if len(args) == 4 and all(isinstance(arg, (int, float)) for arg in args[:2]) and isinstance(args[2], Orientation) and isinstance(args[3], (int, float)):
            self.offset = Point(args[0], args[1])
            self.orientation = args[2]
            self.mag = args[3]   
        elif len(args) == 3:
            self.offset = Point(args[0], args[1])
            self.orientation = args[2]
            
            '''
            if type(args[0]) is Point and isinstance(args[1], Orientation) and isinstance(args[2], (int, float)):
                self.offset = args[0]
                self.orientation = args[1]
                self.mag = args[2]
            elif all(isinstance(arg, (int, float)) for arg in args[:2]) and isinstance(args[2], (Orientation, int, float)):

                self.offset = Point(args[0], args[1])
                if isinstance(args[2], Orientation):
                    self.orientation = args[2]
                else:
                    self.mag = args[2]
            '''
        elif len(args) == 2:
            self.offset = args[0]
            self.orientation = args[1]
            
            '''
            if isinstance(args[0], Point) and isinstance(args[1], (Orientation, int, float)):
               
                self.offset = args[0]
                if isinstance(args[1], Orientation):
                    self.orientation = args[1]
                else:
                    self.mag = args[1]
            elif all(isinstance(arg, (int, float)) for arg in args):
                
                self.offset = Point(args[0], args[1])
            '''
        elif len(args) == 1 and isinstance(args[0], Point):
            self.offset = args[0]
        elif len(args)==0:
            self.offset = Point(0,0)
        else:
            raise ValueError("Transform objects only accept either a Point object or two coordinate values, both of which can be followed by two optional arguments: orientation and mag.")
        
        self.xOffset = self.offset.x
        self.yOffset = self.offset.y
        self.mag = 1.0
    
    # already been tested.     
    def __str__(self):
        return f"Transform(xOffset={self.xOffset}, yOffset={self.yOffset}, orientation={self.orientation}, mag={self.mag})"
   
    # already been tested.   
    def concat(self, trans):
        newOffset = Point(self.offset.x + trans.offset.x, self.offset.y + trans.offset.y)
        newOrientation = self.orientation.concat(trans.orientation)
        newMag = self.mag * trans.mag
        return Transform(newOffset, newOrientation, newMag)
    
    # already been tested.     
    def invert(self):  
        if self.orientation not in [Orientation.R0, Orientation.R90, Orientation.R180, Orientation.R270]:
            raise ValueError("Inversion is only meaningful for orientations:[Orientation.R0, Orientation.R90, Orientation.R180, Orientation.R270].")
        inversedOrientation = self.orientation.getRelativeOrient(Orientation.R0)
        if self.orientation == Orientation.R0:
            invertedOffset = Point(-self.offset.x, -self.offset.y)
        elif self.orientation == Orientation.R90:
            invertedOffset = Point(-self.offset.y, self.offset.x )
        elif self.orientation == Orientation.R180:
            invertedOffset = Point(self.offset.x, self.offset.y)
        elif self.orientation == Orientation.R270:
            invertedOffset = Point(self.offset.y, -self.offset.x)
        return Transform(invertedOffset, inversedOrientation, self.mag)
   
    # already been tested. 
    def mirrorX(self, yCoord=0):
        mXorientation = self.orientation.concat(MX)
        return Transform(0, 2 * yCoord, mXorientation)

    # already been tested. 
    def mirrorY(self, xCoord=0):
        mYorientation=self.orientation.concat(Orientation.MY)
        return Transform(2 * xCoord, 0, mYorientation)

    # already been tested. 
    def rotate90(self, origin=None):
        newOrigin = Point(origin.x + origin.y, origin.y - origin.x) if isinstance(origin, Point) else Point()
        r90orientation = Orientation.R90
        return Transform(newOrigin, r90orientation, self.mag)

    # already been tested. 
    def rotate180(self, origin=None):
        newOffset = Point(2*origin.x,2*origin.y) if isinstance(origin, Point) else Point()
        r180orientation = Orientation.R180
        return Transform(newOffset,  r180orientation, self.mag)

    # already been tested. 
    def rotate270(self, origin=None):
        newOffset = newOrigin = Point(origin.x - origin.y, origin.y + origin.x) if isinstance(origin, Point) else Point()
        r270orientation = Orientation.R270
        return Transform(newOffset, r270orientation, self.mag)


