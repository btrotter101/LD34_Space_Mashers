
import random
from CONSTANTS import *
from pygame.locals import *

# The keys available to use in the minigames
rightpossiblekeys = [K_h,K_i,K_j,K_k,K_l,K_m,K_n,K_o,K_p,K_u,K_y]
leftpossiblekeys = [K_q,K_w,K_e,K_r,K_t,K_a,K_d,K_f,K_g,K_z,K_x,K_c,K_v,K_b]

# A game class that needs a pattern, but does not have a time limit
class PatternLevel():

    # Difficulty is a scale from 0-3 (or higher, but we don't care, yet)
    def __init__(self,difficulty):
        self.won = False
        self.pattern = []
        self.length = 0
        self.twobuttons = []
        self.strikes = 0
        self.GenerateLevel(difficulty)
        return

    def GenerateLevel(self,difficulty):
        if difficulty == 0:
            self.length = 9
        elif difficulty == 1:
            self.length = 14
        elif difficulty == 2:
            self.length = 19
        else:
            self.length = 24
        # Assign each key to the keys list
        self.twobuttons.append(leftpossiblekeys[random.randrange(0,len(leftpossiblekeys))])
        self.twobuttons.append(rightpossiblekeys[random.randrange(0,len(rightpossiblekeys))])
        # Fill up the pattern list for the level
        while(len(self.pattern) < self.length):
            self.pattern.append(self.twobuttons[random.randrange(0,2)])
        return

    def Update(self,key):
        if (len(key) == 0):
            return True
        if (key[0] == self.pattern[0]):
            del self.pattern[0]
            return True
        else:
            self.strikes += 1
            return False

    def timeLeft(self):
        if (len(self.pattern) <=0):
            self.won = True
            return 0
        elif self.strikes >= 3:
            return 0
        else:
            return 1    # Might want to increase this a bit?

    def getLeftKey(self):
        return self.twobuttons[0]

    def getRightKey(self):
        return self.twobuttons[1]

class TimedLevel(PatternLevel):
    def __init__(self,difficulty):
        self.time = 0
        self.timepassed = 0
        PatternLevel.__init__(self,difficulty)
        return

    def GenerateLevel(self,difficulty):
        PatternLevel.GenerateLevel(self,difficulty)
        self.time = self.length*(2*FPS/3)-(FPS*self.length/9*difficulty)
        return

    def Update(self,key):
        self.timepassed += 1
        if self.timepassed >= self.time:
            return False
        if (len(key) == 0):
            return True
        if (key[0] == self.pattern[0]):
            del self.pattern[0]
            return True
        else:
            self.strikes += 1
            return False

    def timeLeft(self):
        if (len(self.pattern) <=0):
            self.won = True
            return 0
        elif self.strikes >= 3:
            return 0
        elif self.timepassed >= self.time:
            return 0
        else:
            return self.time - self.timepassed


class PatternTimedLevel(PatternLevel):
    def __init__(self,difficulty):
        self.timebetweenbeats = 0
        self.beatlength = 0
        PatternLevel.__init__(self,difficulty)
        return

    def GenerateLevel(self,difficulty):
        PattenLevel.GenerateLevel(self,difficulty)
        self.timebetweenbeats = CONSTANTS.FPS-(5*difficulty)
        self.beatlength = CONSTANTS.FPS-(5*difficulty)
        return

    
class MashLevel(PatternLevel):
    def __init__(self,difficulty):
        PatternLevel.__init__(self,difficulty)
        self.timepassed = 0
        return

    def GenerateLevel(self,difficulty):
        # Assign each key to the keys list
        self.twobuttons.append(leftpossiblekeys[random.randrange(0,len(leftpossiblekeys))])
        self.twobuttons.append(rightpossiblekeys[random.randrange(0,len(rightpossiblekeys))])
        self.pattern = [self.twobuttons[0],self.twobuttons[1]]
        self.time = 10*FPS
        self.length = self.time/4+(difficulty*4)
        self.keyspressed = 0
        return

    def Update(self,key):
        self.timepassed += 1
        if self.timepassed % 3 == 0:
            if self.pattern[0] == self.twobuttons[0]:
                self.pattern[0] = self.twobuttons[1]
            else:
                self.pattern[0] = self.twobuttons[0]
        if self.timepassed > self.time:
            return False
        if len(key) <= 0:
            return True
        for i in key:
            if i == self.twobuttons[0]:
                self.keyspressed += 1
            elif i == self.twobuttons[1]:
                self.keyspressed += 1
        return True

    def timeLeft(self):
        if (self.keyspressed >= self.length):
            self.won = True
            return 0
        elif self.timepassed >= self.time:
            return 0
        else:
            return self.time - self.timepassed

class AimLevel():
    
    def __init__(self,difficulty):
        self.timeLimit = 0   # Time limit of level
        self.timePassed = 0     # How much time has passed on the level
        self.length = 0     # Number of targets on this level
        self.strikes = 0    # Number of failed interactions on this level
        self.aimPoint = [320,100]  # Bad programming, but I'm tired of long formulas
        self.targets = []
        self.pattern = []
        self.won = False

        self.timerHorizontal = AIM_TIMER_MAX # Horizontal variables
        self.buttonHorizontal = 0
        self.numPressesHorizontal = 0

        self.timerVertical = AIM_TIMER_MAX   # Vertical variables
        self.buttonVertical = 0
        self.numPressesVertical = 0
        self.GenerateLevel(difficulty)
        return

    def GenerateLevel(self,difficulty):
        self.timeLimit = AIM_TIME_LIMIT
        
        # Assign each key to the keys list
        self.buttonHorizontal = leftpossiblekeys[random.randrange(0,len(leftpossiblekeys))]
        self.buttonVertical = rightpossiblekeys[random.randrange(0,len(rightpossiblekeys))]
        self.pattern.append(self.buttonHorizontal)
        self.pattern.append(self.buttonVertical)
        # Assign length of level: number of targets to hit
        if difficulty == 0:
            self.length = 1
        elif difficulty == 1:
            self.length = 2
        elif difficulty == 2:
            self.length = 3
        else:
            self.length = 5
        while(len(self.targets) < self.length):
            self.targets.append([random.randrange(AIM_H_MIN,AIM_H_MAX,AIM_STEP), random.randrange(AIM_V_MIN,AIM_V_MAX,AIM_STEP)])
        return

    def Update(self,key):
        ReturnValue = True
        self.timePassed += 1
        #print("Aim timePassed ",self.timePassed)
        if self.timePassed % 10 == 0:
            if self.pattern[0] == self.buttonVertical:
                self.pattern[0] = self.buttonHorizontal
            else:
                self.pattern[0] = self.buttonVertical
        if self.timePassed >= self.timeLimit:
            #print("Timeout ", self.timeLimit)
            return False
        
        for k in key:
            #print(chr(k))
            if(k == self.buttonHorizontal):
                if (self.numPressesHorizontal == 0):
                    self.timerHorizontal = self.timePassed + DOUBLE_CLICK_TIME
                    #print("Start H timer ",self.timerHorizontal)
                self.numPressesHorizontal += 1
            elif (k == self.buttonVertical):
                # As above for vertical
                if (self.numPressesVertical == 0):
                    self.timerVertical = self.timePassed + DOUBLE_CLICK_TIME
                self.numPressesVertical += 1
            else:
                # Wrong keypresses are bad!
                self.strikes += 1
                ReturnValue = False
                #print("Wrong Strike ",self.strikes)

        if self.timePassed >= self.timerHorizontal:
            #print("H check ",self.timerHorizontal)
            if self.numPressesHorizontal > 2:
                # Not a button mashing level: button mashing should be penalized
                self.strikes += 1
                ReturnValue = False
                #print("Mash Strike ",self.strikes)
            elif self.numPressesHorizontal == 2:
                # Double click
                #print("Double click")
                self.aimPoint[0] += AIM_STEP
                if self.aimPoint[0] >= AIM_H_MAX:
                    self.aimPoint[0] = AIM_H_MAX
            else:
                # Single click
                #print("Single click")
                self.aimPoint[0] -= AIM_STEP
                if self.aimPoint[0] <= AIM_H_MIN:
                    self.aimPoint[0] = AIM_H_MIN
            self.timerHorizontal = AIM_TIMER_MAX
            self.numPressesHorizontal = 0

        if self.timePassed >= self.timerVertical:
            if self.numPressesVertical > 2:
                # Not a button mashing level: button mashing should be penalized
                self.strikes += 1
                ReturnValue = False
            elif self.numPressesVertical == 2:
                # Double click
                self.aimPoint[1] += AIM_STEP
                if self.aimPoint[1] >= AIM_V_MAX:
                    self.aimPoint[1] = AIM_V_MAX
            else:
                # Single click
                self.aimPoint[1] -= AIM_STEP
                if self.aimPoint[1] <= AIM_V_MIN:
                    self.aimPoint[1] = AIM_V_MIN
            self.timerVertical = AIM_TIMER_MAX
            self.numPressesVertical = 0

        # Check if aim point is on current target
        if (self.aimPoint == self.targets[0]):
            del self.targets[0]
            #print("Target destroyed")
            return True

        # Check for strikeout
        if self.strikes >= 3:
            #print("Strikeout")
            return False

        return ReturnValue
                        
    def timeLeft(self):
        if (len(self.targets) <=0):
            self.won = True
            return 0
        elif self.strikes >= 3:
            return 0
        elif self.timePassed >= self.timeLimit:
            return 0
        else:
            return self.timeLimit - self.timePassed

    def getLeftKey(self):
        return self.buttonHorizontal

    def getRightKey(self):
        return self.buttonVertical

    def GetTargetLoc(self):
        return self.targets[0]

    def GetAimLoc(self):
        return self.aimPoint
        
