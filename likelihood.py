# Python 3.7
import numpy as np
import requests

# Hero List
heroesList = ['ana', 'ashe', 'bastion', 'baptiste', 'brigitte', 'doomfist', 'dva', 'genji', 'hanzo', 'junkrat', 'lucio', 'mccree', 'mei', 'mercy', 'moira', 'pharah', 'reaper', 'reinhardt', 'roadhog', 'soldier76', 'symmetra', 'torbjorn', 'tracer', 'widowmaker', 'winston' , 'wreckingball', 'zarya', 'zenyatta', 'sombra', 'orisa']
heroesId = range(len(heroesList))
heroesDict = dict(zip(heroesList, heroesId))

class Player:
    name = ''
    stats = []
    def __init__(self, name, nation, stats):
        self.name = name
        self.nation = nation
        self.stats = stats

    def getTimePlayed(self):
        timeplayed = np.zeros(len(heroesList))   # for zero problem, set min time is 
        if not self.stats:
            return timeplayed
        heroesJson = self.stats['heroes']
        for heroJson in heroesJson:
            stats = heroJson['stats']
            for si in stats:
                if si['name'] == 'time_played_total':
                    timeplayed[heroesDict[heroJson['name']]] = si['value']
        return timeplayed

    def __repr__(self):
        return '<Name: %s Time: %s>' % (self.name, dict(zip(heroesList, self.getTimePlayed())))


class LikeSystem:
    pList = []
    # Read Database
    def readData(self):
        html = requests.get('https://api.overwatchleague.com/players?expand=stats')
        data = html.json()
        for eaPlayer in data:
            self.pList.append(Player(eaPlayer['name'], eaPlayer['nationality'], eaPlayer['stats']))
        return self

    def getPlayerByName(self, name):
        for py in self.pList:
            if py.name == name:
                return py
        return -1

    # Calculate Distance
    def getDistance(self, pi, pj):
        # should be in normal
        di = pi.getTimePlayed() / 100
        di = di / np.linalg.norm(di)
        dj = pj.getTimePlayed() / 100
        dj = dj / np.linalg.norm(dj)
        return np.sum(np.power(di - dj, 2.0))

    def calclikelihood(self, pi):
        likelihoods = np.zeros(len(self.pList))
        for j in range(len(self.pList)):

            likelihoods[j] = self.getDistance(pi, self.pList[j])
        return likelihoods

    def getMost(self, likelihoods, n):
        lmax = np.argsort(likelihoods)
        outlist = np.array(self.pList)
        return outlist[lmax[0:n]], likelihoods[lmax[0:n]]    # skip itself

lk = LikeSystem()
lk.readData()
print('Loaded from API')
elsa = lk.getPlayerByName('Guxue')
lh = lk.calclikelihood(elsa)
pymost = lk.getMost(lh, 5)
print(pymost)