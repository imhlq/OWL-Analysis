# One of my ideal match system

# everyone is circle at different position
# go bigger with time
# until touch other circle
# match them togerher
import random
import time

class player:
    def __init__(self, pos):
        self.id = random.randint(0, 99999)
        self.pos = pos

class matchSys:
    
    teamNum = 0
    teamPeopleNum = 6
    bubbleInitSize = 1
    bubbleGrowthSpeed = 1
    inGameTeam = []

    def __init__(self):
        self.gameLine = []
        self.bubbleDict = {}


    def addPlayer(self, player):
        if len(self.gameLine) == 0:
            self.gameLine.append(player)
            self.bubbleDict[player] = self.bubbleInitSize
            return True

        for i in range(len(self.gameLine)):
            if player.pos < gameLine[i].pos:
                self.gameLine.insert(i-1, player)
                self.bubbleDict[player] = self.bubbleInitSize
                return True
        # if larger than all current players
        self.gameLine.append(player)
        self.bubbleDict[player] = self.bubbleInitSize
        return True


    def flash(self):
        # flash every unit time
        # 1. Chech and match
        connect = 0
        for i in range(len(self.gameLine)-1):
            if self.gameLine[i].pos + self.bubbleDict[self.gameLine[i].pos] >= self.gameLine[i+1] - self.bubbleDict[self.gameLine[i+1].pos]:
                connect += 1
            else:
                connect = 0

            if connect == self.teamPeopleNum:
                # Match success!
                newTeam = self.gameLine[i-4:i+2]
                self.inGameTeam.append(newTeam)
                for rmplayer in newTeam:
                    self.gameLine.remove(rmplayer)
            
        # 2. Grow bubble
        for ip in self.gameLine:
            self.bubbleDict[ip] = self.bubbleDict[ip] + self.bubbleGrowthSpeed

    def go_run(self, dt):
        self.flash()
        time.sleep(dt)