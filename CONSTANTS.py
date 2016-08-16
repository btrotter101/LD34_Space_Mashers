
# Set the Frames per second
FPS = 30

# Set the screensize
SCREENSIZE = (640,480)

# Aim level constants
AIM_STEP = 10
AIM_H_MIN = 170 + AIM_STEP
AIM_V_MIN = 0 + AIM_STEP
AIM_H_RANGE = 200
AIM_V_RANGE = 200
AIM_H_MAX = AIM_H_MIN + AIM_H_RANGE - 2*AIM_STEP
AIM_V_MAX = AIM_V_MIN + AIM_V_RANGE - 2*AIM_STEP
DOUBLE_CLICK_TIME = 5*FPS/30      #Not final
AIM_TIME_LIMIT = 45 * FPS
AIM_TIMER_MAX = AIM_TIME_LIMIT + 1   # High timer value, longer than time limit

# Color constants
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,127,39)
PINK = (255,128,128)
WHITE = (255,255,255)
BLACK = (0,0,0)
