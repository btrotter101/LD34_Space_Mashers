import pygame, helpers
from  CONSTANTS import *
from random import randint, randrange
from pygame.locals import *

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

def ScrollingScreen(SCREEN,CLOCK,baseImage):
    # Make something to draw to the screen
    background = helpers.SurfaceSetup(SCREENSIZE,BLACK)
    foreground = helpers.LoadImage(baseImage,"Art",-1)

    starfield = StarField(45)
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
        stars = starfield.Update(2)
        for i in stars:
            SCREEN.blit(i.star.Surf(),i.star.Rect())
        SCREEN.blit(foreground,(0,0))
        # Update the screen to reflect changes
        pygame.display.update()
        # Limit the frames drawn per second
        CLOCK.tick(30)

def MainMenu(SCREEN,CLOCK):
    # Make something to draw to the screen
    background = helpers.SurfaceSetup(SCREENSIZE,(0,0,0))

    # All the stuff to draw to the screen
    ship = helpers.LoadImage("Ship outside.png","Art",-1)
    shipposition = ((3*(SCREENSIZE[0]-ship.get_width()))/4,
                    (3*(SCREENSIZE[1]-ship.get_height()))/4)
    starfield = StarField(45)
    buttons = helpers.LoadImage("Menu buttons.png","Art",-1)
    buttonsorg = (50,50)
    title = helpers.LoadImage("Title.png","Art",-1)
    titleloc = (330,50)
    MousePos = (0,0)

    buttonhighlight = helpers.SurfaceSetup((177,65),YELLOW)
    buttonhighlight.set_alpha(100)

    # The button locations
    buttonsloc = {1:Rect(buttonsorg[0]+1,buttonsorg[1]+1,177,65),
                  2:Rect(buttonsorg[0]+1,buttonsorg[1]+94,177,65),
                  3:Rect(buttonsorg[0]+1,buttonsorg[1]+205,177,65),
                  4:Rect(buttonsorg[0]+1,buttonsorg[1]+304,177,65),}
    # Ship jitter
    shipjitter = 0
    while True:
        keyup = False
        # Check for quit and do so if needed
        for event in pygame.event.get():
            if event.type == QUIT:
                helpers.ExitGame()
                return
            if event.type == MOUSEMOTION:
                MousePos = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONUP:
                keyup = True

        shipjitter += 1
        # Draw the background to the screen
        SCREEN.blit(background,(0,0))
        stars = starfield.Update(2)
        for i in stars:
            SCREEN.blit(i.star.Surf(),i.star.Rect())
        SCREEN.blit(buttons,buttonsorg)
        SCREEN.blit(title,titleloc)
        SCREEN.blit(ship,shipposition)
        if shipjitter % 7 == 0:
            shipjitter = 0
            shipposition = (shipposition[0]+randrange(-1,2),shipposition[0]++randrange(-1,2))
        for i in buttonsloc:
            if buttonsloc[i].collidepoint(MousePos) == True:
                  SCREEN.blit(buttonhighlight,buttonsloc[i])
            if(keyup == True and buttonsloc[i].collidepoint(MousePos) == True):
                return i
        # Update the screen to reflect changes
        pygame.display.update()
        # Limit the frames drawn per second
        CLOCK.tick(30)
        

def Ending(SCREEN,CLOCK,victory):
    # Make something to draw to the screen
    background = helpers.SurfaceSetup(SCREENSIZE,(0,0,0))
    ship = helpers.LoadImage("Ship outside.png","Art",-1)
    shipposition = ((SCREENSIZE[0]-ship.get_width())/2,
                    (SCREENSIZE[1]-ship.get_height())/2)
    inspacebox = helpers.LoadImage("innerspace.png","Art",-1)
    starfield = StarField(45)
    transitiontime = 5*FPS
    shipmove = SCREENSIZE[0]/(4*transitiontime)
    shipscaling = 1.0
    if victory == True:
        winbox = helpers.LoadImage("Win text.png","Art",-1)
        starbase = helpers.LoadImage("Planet.png","Art",-1)
        starbasepos = (SCREENSIZE[0]+ship.get_width()/4,150)
        gotime = 4*transitiontime/5
    else:
        losebox = helpers.LoadImage("Loss text.png","Art",-1)
        explosion = helpers.LoadImage("Sparks.png","Art",-1)

    # The Game Loop
    while True:
        keys = []
        # Check for quit and do so if needed
        for event in pygame.event.get():
            if event.type == QUIT:
                helpers.ExitGame()
                return
            if event.type == KEYDOWN:
                keys.append(event.key)


        if transitiontime >= 0:
            transitiontime -= 1
        if transitiontime <0:
            if len(keys) !=0:
                return
            if transitiontime > -1*FPS:
                transitiontime -= 1
            
        # Draw the background to the screen
        SCREEN.blit(background,(0,0))
        if victory == True:
            # Update background relative to speed
            stars = starfield.Update(int(3*shipscaling))
            for i in stars:
                SCREEN.blit(i.star.Surf(),i.star.Rect())
            if starbasepos[0] < SCREENSIZE[0]:
                SCREEN.blit(starbase,starbasepos)
            SCREEN.blit(ship,shipposition)
            if transitiontime > gotime:
                shipscaling -= 1.0*3.5/(transitiontime)
            if transitiontime < gotime:
                if starbasepos[0] > shipposition[0]:
                    shipposition = (shipposition[0]+2,shipposition[1])
                    starbasepos = (starbasepos[0]-2,starbasepos[1])
                elif shipposition[0]<SCREENSIZE[0]:
                    shipposition = (shipposition[0]+2,shipposition[1])
        elif shipscaling > 0:
            # Update background relative to speed
            stars = starfield.Update(3)
            for i in stars:
                SCREEN.blit(i.star.Surf(),i.star.Rect())
            SCREEN.blit(pygame.transform.scale(ship,(int(ship.get_width()*shipscaling),int(ship.get_height()*shipscaling))),
                        (shipposition[0]+randrange(-5,5),shipposition[1]+randrange(-5,5)))
            shipscaling -= 1.0/(transitiontime*2)
            
            SCREEN.blit(explosion,(shipposition[0]+randrange(-15,int(ship.get_width()*shipscaling)),
                                   shipposition[1]+randrange(-15,int(ship.get_height()*shipscaling))))
            SCREEN.blit(explosion,(shipposition[0]+randrange(-15,int(ship.get_width()*shipscaling)),
                                   shipposition[1]+randrange(-15,int(ship.get_height()*shipscaling))))
            SCREEN.blit(explosion,(shipposition[0]+randrange(-15,int(ship.get_width()*shipscaling)),
                                   shipposition[1]+randrange(-15,int(ship.get_height()*shipscaling))))
            SCREEN.blit(explosion,(shipposition[0]+randrange(-15,int(ship.get_width()*shipscaling)),
                                   shipposition[1]+randrange(-15,int(ship.get_height()*shipscaling))))
        else:
            # Update background relative to speed
            stars = starfield.Update(3)
            for i in stars:
                SCREEN.blit(i.star.Surf(),i.star.Rect())
        if transitiontime <= 0:
            if victory == False:
                SCREEN.blit(losebox,((SCREENSIZE[0]-losebox.get_width())/2,100))
                if transitiontime == -FPS:
                    SCREEN.blit(inspacebox,((SCREENSIZE[0]-inspacebox.get_width())/2,175))
            else:
                SCREEN.blit(winbox,((SCREENSIZE[0]-winbox.get_width())/2,100))
                if transitiontime == -FPS:
                    SCREEN.blit(inspacebox,((SCREENSIZE[0]-inspacebox.get_width())/2,175))
        # Update the screen to reflect changes
        pygame.display.update()
        # Limit the frames drawn per second
        CLOCK.tick(30)


def Transition(SCREEN,CLOCK,won,difficulty):
    # Make something to draw to the screen
    background = helpers.SurfaceSetup(SCREENSIZE,(0,0,0))
    ship = helpers.LoadImage("Ship outside.png","Art",-1)
    explosion = helpers.LoadImage("Sparks.png","Art",-1)
    shipposition = ((SCREENSIZE[0]-ship.get_width())/2,
                    (SCREENSIZE[1]-ship.get_height())/2)
    starfield = StarField(45)
    transitiontime = 5*FPS
    gotime = 4*transitiontime/5
    shipmove = SCREENSIZE[0]/(4*transitiontime)
    # The Game Loop
    while True:
        
        # Check for quit and do so if needed
        for event in pygame.event.get():
            if event.type == QUIT:
                helpers.ExitGame()
                return


        # This is where the "game logic" WILL happen.
        transitiontime -= 1
        if transitiontime <0:
            return
        # Update background relative to speed
        stars = starfield.Update(5)
            
        # Draw the background to the screen
        SCREEN.blit(background,(0,0))
        for i in stars:
            SCREEN.blit(i.star.Surf(),i.star.Rect())
        if won == True:
            SCREEN.blit(ship,shipposition)
            if transitiontime < gotime:
                shipposition = (shipposition[0]+shipmove,shipposition[1])
                shipmove += 1
        else:
            SCREEN.blit(ship,(shipposition[0]+randrange(-5,5),shipposition[1]+randrange(-5,5)))
            
            SCREEN.blit(explosion,(shipposition[0]+randrange(-15,ship.get_width()),
                                   shipposition[1]+randrange(-15,ship.get_height())))
            SCREEN.blit(explosion,(shipposition[0]+randrange(-15,ship.get_width()),
                                   shipposition[1]+randrange(-15,ship.get_height())))
            SCREEN.blit(explosion,(shipposition[0]+randrange(-15,ship.get_width()),
                                   shipposition[1]+randrange(-15,ship.get_height())))
            SCREEN.blit(explosion,(shipposition[0]+randrange(-15,ship.get_width()),
                                   shipposition[1]+randrange(-15,ship.get_height())))
        # Update the screen to reflect changes
        pygame.display.update()
        # Limit the frames drawn per second
        CLOCK.tick(30)


#
#
#
#
class Star():
    def __init__(self,size,location,speed):
        self.star = helpers.ScreenObject(location,helpers.SurfaceSetup(
            size,(255-randint(0,50),255-randint(0,50),255-randint(0,50))))
        self.speed = speed

    def ReturnX(self):
        return self.star.Rectangle[0]

    def Update(self,shipspeed=None,Location = None):
        if Location == None:
            self.star.MoveRect(self.star.Rectangle.move(shipspeed/self.speed,0))
        else:
            self.star.MoveRect(self.star.Rectangle.move(Location,0))
        return

#
#
#
class StarField():
    def __init__(self,NumOfStars):
        self.starlist = []
        i = 0
        while i < NumOfStars:
            size  = (randint(5,15),randint(3,5))
            if size[1]==3:
                speed = randint(-3,-1)
            elif size[1]==4:
                speed = randint(-5,-2)
            else:
                speed = randint(-8,-5)
            self.starlist.append(Star(size,
                                pygame.rect.Rect((randint(0,SCREENSIZE[0]),randint(5,SCREENSIZE[1]-5)),size),
                                speed))
            i = i+1

    def Update(self,shipspeed,moving = True):
        if moving == True:
            for i in self.starlist:
                if i.ReturnX()>0:
                    i.Update(shipspeed)
                else:
                    i.Update(Location=SCREENSIZE[0])
        return self.starlist



