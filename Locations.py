from helpers import LoadImage

class Location():
    def __init__(self,Name):
        self.name = Name
        return
    def setRedLight(self,xy):
        self.redlocation = xy
        return
    def setGreenLight(self,xy):
        self.grnlocation = xy
        return
    def setCurrentBracket(self,xy):
        self.thiskeys = xy
        return
    def setFutureBracket(self,xy):
        self.nextkeys = xy
        return
    def setTimerHigh(self,xy):
        self.timerHigh = xy
        return
    def setTimerLow(self,xy):
        self.timerLow = xy
        return
    def setImage(self,Image):
        print(self.name)
        self.Image = LoadImage(Image,"Art")

    
Cockpit = Location("Cockpit")
Cockpit.setRedLight((280,370))
Cockpit.setGreenLight((305,370))
Cockpit.setCurrentBracket((0,390))
Cockpit.setFutureBracket((560,390))
Cockpit.setTimerHigh((290,270))
Cockpit.setTimerLow((320,270))

EngineRoom = Location("Engine Room")
EngineRoom.setRedLight((240,225))
EngineRoom.setGreenLight((310,230))
EngineRoom.setCurrentBracket((30,400))
EngineRoom.setFutureBracket((550,400))
EngineRoom.setTimerHigh((500,50))
EngineRoom.setTimerLow((530,50))

Turret = Location("Turret")
Turret.setRedLight((170,360))
Turret.setGreenLight((400,325))
Turret.setCurrentBracket((0,390))
Turret.setFutureBracket((560,390))
Turret.setTimerHigh((290,400))
Turret.setTimerLow((320,400))
