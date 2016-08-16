#!/usr/bin/env python

'''
Main.py program
Version 1.0
Created by Chandler Norris March 18, 2015

This is the basic format for a pygame main loop.  This has everything
needed to initialize a screen and draw to it with minimal dependencies.
This program uses another file named helpers.py. If you don't want to
use helpers.py, simply copy the SurfaceSetup function to either this file
or another file of your choice.
'''

# Import the needed accessory libraries
import pygame, helpers, os, Levels, Effects, math
from Locations import *
from random import randrange
from CONSTANTS import *
from pygame.locals import *
import pygame._view,pygame.surface,pygame.image,pygame.mixer

# Center the window, since that's the nice way to do it.
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Optional, but it helps with version control
#from time import ctime
#print("Build Created " + ctime(os.path.getmtime(os.path.basename(__file__))))

# Initialize Pygame
pygame.init()
# Initialize the sound module
pygame.mixer.init()

# Name the window screen
pygame.display.set_caption("Space Mashers")
# Initialize the clock to limit the frames per second
CLOCK = pygame.time.Clock()
# Initialize a screen to reference later
SCREEN = pygame.display.set_mode(SCREENSIZE)

# Used for the targeting minigame
targetImg = helpers.LoadImage("Enemy Craft.png","Art",-1)
aimImg = helpers.LoadImage("Recticle.png","Art",-1)

# BLINKY lights
redlight = helpers.LoadImage("Light.png","Art")
redoverlay = helpers.SurfaceSetup(redlight.get_size(),BLUE)
redoverlay.set_alpha(75)
redlight.blit(redoverlay,(0,0))
redlight.set_colorkey(redlight.get_at((0,0)),RLEACCEL)
redlight.set_alpha(200)
# And the green blinky one!
greenlight = helpers.LoadImage("Light.png","Art")
greenoverlay = helpers.SurfaceSetup(greenlight.get_size(),YELLOW)
greenoverlay.set_alpha(75)
greenlight.blit(greenoverlay,(0,0))
greenlight.set_colorkey(greenlight.get_at((0,0)),RLEACCEL)
greenlight.set_alpha(200)

# AUDIO!!!
Explosion = pygame.mixer.Sound(os.path.join("Sound","Impact.wav"))
Movement = pygame.mixer.Sound(os.path.join("Sound","Jump.ogg"))
Klaxon = pygame.mixer.Sound(os.path.join("Sound","Alien_Siren.wav"))
# This audio is from KevanGC

def Main():
    while True:
        choose = Effects.MainMenu(SCREEN,CLOCK)
        if choose == 1:
            Game()
        elif choose == 2:
            SimpleScreen("Tutorial.png")
        elif choose == 3:
            Effects.ScrollingScreen(SCREEN,CLOCK,"Credits.png")
        else:
            helpers.ExitGame()
            return

        
def SimpleScreen(baseImage):
    # Make something to draw to the screen
    background = helpers.LoadImage(baseImage,"Art")

    # Make a cursor
    mouse = pygame.mouse.get_pressed()
    MousePos = pygame.mouse.get_pos()

    # The Menu Loop
    while True:
        
        # Check for quit and do so if needed
        for event in pygame.event.get():
            if event.type == QUIT:
                helpers.ExitGame()
                return
            # Get the state of the mouse
            mouse = pygame.mouse.get_pressed()
            MousePos = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONUP:
                return
            if event.type == KEYUP:
                return
        # Draw the background to the screen
        SCREEN.blit(background,(0,0))
        # Update the screen to reflect changes
        pygame.display.update()
        # Limit the frames drawn per second
        CLOCK.tick(30)

        
def CreateNewLevel(levelsPassed,levelsLost):
    #print("New level ",levelsPassed)
    if (levelsPassed + levelsLost) == 1:
        
        return Levels.AimLevel(0)
    elif (levelsPassed + levelsLost) == 2:
        
        return Levels.TimedLevel(0)
    elif levelsPassed == 3:
        difficulty = randrange(0,2)
    elif levelsPassed < 6:
        difficulty = randrange(0,3)
    elif levelsPassed < 8:
        difficulty = randrange(1,4)
    else:
        difficulty = randrange(2,4)
    minigameSelect = randrange(0,4)
    if minigameSelect == 0:
        returnLevel = Levels.PatternLevel(difficulty)
    elif minigameSelect == 1:
        returnLevel = Levels.TimedLevel(difficulty)
    elif minigameSelect == 2:
        returnLevel = Levels.MashLevel(difficulty)
    else:
        returnLevel = Levels.AimLevel(difficulty)
    print(returnLevel)

    return returnLevel
        
def ShakeImage(loc,badanswershake):
    returnLoc = loc
    if badanswershake > 0:
        returnLoc = (loc[0] + randrange(-badanswershake,badanswershake),
                     loc[1] + randrange(-badanswershake,badanswershake))

    return returnLoc


def Game():
    showPreviewKeys = False
    nextLevel = None
    levelsPassed = 0
    levelsLost = 0
    timerDigitImg = helpers.LoadImage("Base Seven Numerals.png","Art",-1)
    blinders = helpers.LoadImage("Button popup.png","Art",-1)
    blinders.set_alpha(150)
    # text for debugging
    font = pygame.font.Font("freesansbold.ttf",24)
    # Make something to draw to the screen
    background = helpers.SurfaceSetup(SCREENSIZE,BLACK)
    # Create a first level
    activelevel = Levels.MashLevel(0)
    SimpleScreen("Tut_Cockpit.png")
    # Variable for screenshake (with timer intertwined)
    badanswershake = 0
    capslockalarm = False
    capslockoverlay = helpers.SurfaceSetup(SCREENSIZE,RED)
    capslockoverlay.set_alpha(75)
    EngineRoom.setImage("Engine room rd 1.png")
    Turret.setImage("Turret.png")
    # setup the location
    locale = Cockpit
    Cockpit.setImage("Cockpit RD.png")
    # The Game Loop
    while True:
        # The key variable
        key = []
        answer = True
        # Check for quit and do so if needed
        for event in pygame.event.get():
            if event.type == QUIT:
                helpers.ExitGame()
                return
            if event.type == KEYDOWN:
                if event.key == K_CAPSLOCK:
                    if capslockalarm == False:
                        Klaxon.play(loops=-1)
                        capslockalarm = True
                    else:
                        Klaxon.fadeout(250)
                        capslockalarm = False
                elif event.key == K_PRINT:
                    pass
                elif event.key == K_LALT:
                    pass
                else:
                    key.append(event.key)
                    
            # Get the state of the mouse
            mouse = pygame.mouse.get_pressed()
            MousePos = pygame.mouse.get_pos()

        # subtract from the shake time
        if badanswershake > 0:
            badanswershake -= 1
        # UPDATE THE ACTIVE LEVEL
        answer = activelevel.Update(key)
        # Commence the shaking if the player answers incorrectly
        if answer == False:
            Explosion.play()
            badanswershake = 15
        # Check to see if the level is done
        timeLeft = activelevel.timeLeft()
        if timeLeft == 0:
            # Current level is done
            if activelevel.won == True:
                Klaxon.fadeout(250)
                Movement.play()
                Effects.Transition(SCREEN,CLOCK,True,0)
                if capslockalarm == True:
                    Klaxon.play(loops = -1)
                levelsPassed += 1
                if levelsPassed > 9:
                    # If they win the game, go to victory and end
                    Klaxon.fadeout(250)
                    Movement.play()
                    Effects.Ending(SCREEN,CLOCK,True)
                    return
            else:
                Explosion.play()
                Klaxon.fadeout(250)
                Effects.Transition(SCREEN,CLOCK,False,0)
                if capslockalarm == True:
                    Klaxon.play(loops = -1)
                levelsLost += 1
                if levelsLost > 2:
                    Explosion.play()
                    Klaxon.fadeout(250)
                    Effects.Ending(SCREEN,CLOCK,False)
                    return
            # Set up for next level
            if nextLevel == None:
                nextLevel = CreateNewLevel(levelsPassed,levelsLost)
            activelevel = nextLevel
            nextLevel = None
            showPreviewKeys = False
            # Set up locale for next level
            if (levelsPassed + levelsLost == 1):
                SimpleScreen("Tut_Turret.png")
                locale = Turret
            elif (levelsPassed + levelsLost == 2):
                SimpleScreen("Tut_EngineRoom.png")
                locale = EngineRoom
            else:
                if isinstance(activelevel,Levels.AimLevel):
                    i = randrange(0,2)
                    if i == 0:
                        locale = Cockpit
                    else:
                        locale = Turret
                else:
                    i = randrange(0,3)
                    if i == 0:
                        locale = Cockpit
                    elif i == 1:
                        locale = EngineRoom
                    else:
                        locale = Turret
            # print("Pass fail ",levelsPassed, levelsLost)
        elif timeLeft < 5 * FPS:
            # Stop showing next game preview
            showPreviewKeys = False
        elif timeLeft < 10 * FPS:
            # Start showing next game preview
            if nextLevel == None:
                nextLevel = CreateNewLevel(levelsPassed + 1, levelsLost) # assume we'll pass, I guess
            showPreviewKeys = True

        # Draw Everything to the screen
        # Draw the background image
        SCREEN.blit(locale.Image,ShakeImage((0,0),badanswershake))
        # Draw things inside your helmet (that never shake)
        SCREEN.blit(blinders,locale.thiskeys)
        SCREEN.blit(pygame.transform.flip(blinders,True,False),locale.nextkeys)
        textimg = font.render(str(chr(activelevel.getLeftKey()-32))+" "+str(chr(activelevel.getRightKey()-32)),False,(255,255,255))
        SCREEN.blit(textimg,(locale.thiskeys[0]+(textimg.get_width())/2,locale.thiskeys[1]+(textimg.get_height())/2))
        if showPreviewKeys:
            textimg = font.render(str(chr(nextLevel.getLeftKey()-32))+" "+str(chr(nextLevel.getRightKey()-32)),False,(255,255,255))
            SCREEN.blit(textimg,(locale.nextkeys[0]+(textimg.get_width()/2),locale.nextkeys[1]+(textimg.get_height()/2)))
        # Draw things on the ship (that will shake if something goes wrong)
        
        # Draw the red blinky
        if activelevel.getLeftKey() == activelevel.pattern[0]:
            SCREEN.blit(redlight,ShakeImage(locale.redlocation,badanswershake))
        # Draw the green blinky
        else:
            SCREEN.blit(greenlight,ShakeImage(locale.grnlocation,badanswershake))
        # Draw the timer
        shakenLoc = ShakeImage(locale.timerHigh,badanswershake)
        SCREEN.blit(timerDigitImg,shakenLoc,(30*math.floor(timeLeft / FPS / 7),0,30,30))
        shakenLoc2 = (shakenLoc[0] - locale.timerHigh[0] + locale.timerLow[0],
                      shakenLoc[1] - locale.timerHigh[1] + locale.timerLow[1])
        SCREEN.blit(timerDigitImg,shakenLoc2,(30*math.floor(timeLeft / FPS % 7),0,30,30))
        # Draw the targets, if applicable
        if isinstance(activelevel,Levels.AimLevel):
            SCREEN.blit(targetImg,(activelevel.GetTargetLoc()[0]-targetImg.get_width()/2,
                                   activelevel.GetTargetLoc()[1]-targetImg.get_height()/2))
            shakenLoc = ShakeImage(activelevel.GetAimLoc(),badanswershake)
            shakenLoc2 = (shakenLoc[0] - aimImg.get_width()/2,
                          shakenLoc[1] - aimImg.get_height()/2)
            SCREEN.blit(aimImg,shakenLoc2)
        if(capslockalarm == True or badanswershake > 0):
            SCREEN.blit(capslockoverlay,(0,0))

        # Update the screen to reflect changes
        pygame.display.update()
        # Limit the frames drawn per second
        CLOCK.tick(30)


# Call the Main function to start the program
if __name__ == "__main__":
    Main()
