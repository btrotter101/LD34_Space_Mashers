#!/usr/bin/env python

import os,pygame,sys
from pygame.locals import *


#
# LoadImage program Version 1.0
# Created by Chandler Norris May 12,2014
# This program takes an image filename, subdirectory filename and RGB
# value for the colorkey.
#
# LoadImage is used to load and prepare an image for use.
#
def LoadImage(ImageFile, SubFolder=None, ColorKey=None):
    if SubFolder is not None:
        Image = pygame.image.load(os.path.join(SubFolder,ImageFile))
    else:
        Image = pygame.image.load(ImageFile)
    Image = Image.convert()
    if ColorKey is not None:
        if ColorKey is -1:
            ColorKey = Image.get_at((0,0))
        Image.set_colorkey(ColorKey,RLEACCEL)
    return Image

#
# SurfaceSetup program Version 1.0
# Created by Chandler Norris March 2, 2011
# This program takes (x,y) for size and RGB for color.
#
# SurfaceSetup is used to setup all of the surfaces that will be used by
# the program.
#
def SurfaceSetup(size, color=(125,125,125),ColorKey=None,Convert = True):
    surface = pygame.Surface(size)
    surface = surface.convert()
    surface.fill(color)
    if ColorKey is not None:
        if ColorKey is -1:
            ColorKey = Image.get_at((0,0))
        if Convert == True:
            surface.set_colorkey(ColorKey,RLEACCEL)
    return surface 

#
# ExitGame program Version 1.0
# Created by Chandler Norris May 12, 2014
# This program does not take any inputs.
#
# ExitGame exits the game gracefully.
#
def ExitGame():
    pygame.quit()
    sys.exit()
    return

#
# SetupWindow program Version 1.0
# Created by Chandler Norris May 12, 2014
# This program takes (x,y) for window size, string filename for Icon
# and a boolean for whether the window is centered or not.
#
# SetupWindow prepares a window for use.
#
def SetupWindow(WindowSize, Title, Icon=None, Centered=True, NoFrame=False):
    if Centered is True:
        os.environ['SDL_VIDEO_CENTERED']='1'
    if Icon is not None:
        pygame.display.set_icon(LoadImage(Icon))
    if NoFrame is True:
        pygame.display.set_mode(pygame.NOFRAME)
    Screen = pygame.display.set_mode(WindowSize)
    pygame.display.set_caption(Title)
    return Screen

#
# Camera Class
# Created by Dominic Kexel  January 16, 2013
# This is a class with a series of functions to make a camera follow
# any given target.
#
# This came from:
# http://stackoverflow.com/questions/14354171/add-scrolling-to-a-platformer-in-pygame
#
class Camera(object):
    def __init__(self,CameraFunction,ScreenSize,LevelSize=None):
        self.CameraFunction = CameraFunction
        self.state = pygame.rect.Rect(0,0,ScreenSize[0],ScreenSize[1])
        self.ScreenSize = ScreenSize
        if LevelSize == None:
            self.LevelSize = ScreenSize
        else:
            self.LevelSize = LevelSize

    def SetLevelSize(self,LevelSize):
        self.LevelSize = LevelSize
        return

    def apply(self,Target):
        return Target.move(self.state.topleft)

    def update(self, Target):
        self.state = self.CameraFunction(self.state,Target,self.ScreenSize,self.LevelSize)
        return

#
# simple_camera program
# Created by Dominic Kexel  January 16, 2013
# This is a program that calculates the camera offset from
# any given target.  This version does not care about going outside
# the drawable area.
#
def simple_camera(camera, target_rect,ScreenSize,LevelSize):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+int(ScreenSize[0]/2), -t+int(ScreenSize[1]/2), w, h)

#
# complex_camera program
# Created by Dominic Kexel  January 16, 2013
# This is a program that calculates the camera offset from
# any given target.  This version will not go outside
# the drawable area.
#
def complex_camera(camera, target_rect,ScreenSize,LevelSize):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+int(ScreenSize[0]/2), -t+int(ScreenSize[1]/2), w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(LevelSize[0]-ScreenSize[0]), l)   # stop scrolling at the right edge
    t = max(-(LevelSize[1]-ScreenSize[1]), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)

#
# ScreenObject Class
# Created by Chandler Norris  August 22nd, 2014
#
# This class is used in the ScreenUpdate function to contain the necessary
# properties and to speed up the drawing process.
class ScreenObject():
    def __init__(self,Rectangle,surface=None):
        self.Rectangle = Rectangle
        self.offset = Rectangle
        self.Surface = surface
    def OffsetRect(self,Rectangle):
        self.offset = Rectangle
        return
    def MoveRect(self,Rectangle):
        self.Rectangle = Rectangle
        return
    def Rect(self):
        return self.Rectangle
    def Offset(self):
        return self.offset
    def Surf(self):
        if self.Surface != None:
            return self.Surface
        else:
            print("error! No Surface!")
            return

#
# screenupdate function Version 1.1
# Created by Chandler Norris March 2, 2011
# This function takes a list for all functions.
#
# screenupdate assumes that the background is the first surface on the list.
# Any surfaces after that are assumed to be tied to the newpositions list.
# For example, if newposition[1] is a rect, then it will draw what is on
# surfacelist[2] to the display surface. Screenupdate assumes that the
# sprite's new location correlates with the same location on the newpositions list.
# Ex. newpositions[1] will write where the new surface will be on the screen,
# while the newsurfloc[1] will write which part of the surface will be written
# there. There is only minimal error checking at this point, so be
# careful using this function!
#
# 1.1 UPDATE: I added errorchecking for more newpositions than surfaces.
#
def screenupdate(Screen, OldLocations = None, NewDrawObjs = None, Background = None,Offset=False):
    if Background != None:
        if Offset == False:
            for i in OldLocations:
                Screen.blit(Background,i.Rect(),i.Rect())
        else:
            for i in OldLocations:
                Screen.blit(Background,i.Offset(),i.Rect())
    DrawLocation = []
    if Offset == False:
        for i in NewDrawObjs:
            Screen.blit(i.Surf(),i.Rect())
            DrawLocation.append(ScreenObject(i.Rect()))
    else:
        for i in NewDrawObjs:
            Screen.blit(i.Surf(),i.Offset())
            DrawLocation.append(ScreenObject(i.Rect()))
    return (Screen,DrawLocation)
