# STATS FILE: GAME OF WHY
# CHARIS CAT 2024

import numpy as np
import random

class Stats:
    def __init__(self):
        # Population
        self.cellCounter = 0

        # death statistics
        self.cellDeathCounter = {}
        self.cellDeathEscapeCounter = 0
        self.cellDisintegrationCounter = 0
        self.cellDisintegrationDeathCounter = 0

        # birth statistics
        self.cellBabyCounter = {}
        self.cellBabysFailedCounter = {}
        self.cellForcedSpawnCounter = 0
        self.cellFailedForcedSpawnCounter = 0

        # state statistits
        self.cellStateChange = {}
        self.cellStateChangeThisTurn = {}
        self.cellStateStable = 0
        self.cellStateStableThisTurn = 0

        # Movement statistics
        self.cellMovedCounter = 0
        self.cellPushedCounter = 0
        self.cellStoppedCounter = 0

        # TURN STATISTICS
        self.cellBabysThisTurn = {}
        self.cellBabysFailedThisTurn = {}
        self.cellDeathsThisTurn = {}
        self.cellDeathEscapesThisTurn = 0
        self.cellMovedThisTurn = 0
        self.cellPushedThisTurn = 0
        self.cellStoppedThisTurn = 0
        self.cellAliveCount = 0
        self.cellYouthCount = 0
        self.cellElderlyCount = 0
        self.cellAdultCount = 0

    def beginTurn(self):
        self.cellBabysThisTurn = {}
        self.cellDeathsThisTurn = {}
        self.cellDeathEscapesThisTurn = 0
        self.cellBabysFailedThisTurn = {}
        self.cellPushedThisTurn = 0
        self.cellMovedThisTurn = 0
        self.cellStoppedThisTurn = 0
        self.cellAliveCount = 0
        self.cellYouthCount = 0
        self.cellElderlyCount = 0
        self.cellAdultCount = 0
        self.cellStateStableThisTurn = 0
        self.cellStateChangeThisTurn = {}

    def endTurn(self):
        print(f"Turn Summary: There are currently {self.cellAliveCount} living cells. There were {self.cellBabysThisTurn} babies born, {self.getDeathsThisTurn()} cells died, and {self.cellDeathEscapesThisTurn} cells evaded death! ")
        print(self)

    def endRun(self):
        print(self)

    def __str__(self):
        return f"""
Total Cell Count: {self.cellCounter+1}

# Death Statistics
Total Cell Death: {self.getTotalDeath()}
By Reason:
{"\n".join([f"{x}: {self.cellDeathCounter[x]}" for x in self.cellDeathCounter])}
Total Disintegrations: {self.cellDisintegrationCounter} (fully reclaimed: {self.cellDisintegrationDeathCounter})
Total Cell Escapes: {self.cellDeathEscapeCounter}

# Birth Statistics
Total Cell Babies: {self.cellBabyCounter}
By Reason:
{"\n".join([f"{x}: {self.cellBabyCounter[x]}" for x in self.cellBabyCounter])}
Total Cell Skipped Babies: {self.cellBabysFailedCounter}
By Reason:
{"\n".join([f"{x}: {self.cellBabysFailedCounter[x]}" for x in self.cellBabysFailedCounter])}
Total Cell Babies Spawned: {self.cellForcedSpawnCounter}
Total Cell Babies Unspawned: {self.cellFailedForcedSpawnCounter}

# Movement Statistics
Total Cell Movements: {self.cellMovedCounter}
Total Cell Pushed: {self.cellPushedCounter}
Total Cell Stopped: {self.cellStoppedCounter}

# State Statistics
Total State Changes: {self.getCellStateChangeTotal()}
By State:
{"\n".join([f"{x}: {self.cellStateChange[x]}" for x in self.cellStateChange])}
Total Stable Turns: {self.cellStateStable}

# Turn Statistics
Cell Babies: {self.cellBabysThisTurn}
Cell Skipped Babies: {self.cellBabysFailedThisTurn}
Cell Death: {self.getDeathsThisTurn()}
{"\n".join([f"{x}: {self.cellDeathsThisTurn[x]}" for x in self.cellDeathsThisTurn])}
Cell Escapes: {self.cellDeathEscapesThisTurn}
Cell Movements: {self.cellMovedThisTurn}
Cell Pushes: {self.cellPushedThisTurn}
Cell Stops: {self.cellStoppedThisTurn}
Cells Alive: {self.cellAliveCount} (Youth: {self.cellYouthCount}, Adults: {self.cellAdultCount}, Elderly: {self.cellElderlyCount})
Switched Cell States: {self.getCellStateChangesThisTurn()} 
By State:
{"\n".join([f"{x}: {self.cellStateChangeThisTurn[x]}" for x in self.cellStateChangeThisTurn])}
Stable Cell States: {self.cellStateStableThisTurn}
"""

    def addCellBaby(self, reason):
        if reason in self.cellBabyCounter:
            self.cellBabyCounter[reason] += 1

        else:
            self.cellBabyCounter[reason] = 1
        
        if reason in self.cellBabysThisTurn:
            self.cellBabysThisTurn[reason] += 1

        else:
            self.cellBabysThisTurn[reason] = 1
    
    def addCellBabyFailed(self, reason):
        if reason in self.cellBabysFailedCounter:
            self.cellBabysFailedCounter[reason] += 1
        else:
            self.cellBabysFailedCounter[reason] = 1

        if reason in self.cellBabysFailedThisTurn:
            self.cellBabysFailedThisTurn[reason] += 1
        else:
            self.cellBabysFailedThisTurn[reason] = 1
    
    def addCellDeath(self, reason):
        if reason in self.cellDeathCounter:
            self.cellDeathCounter[reason] += 1
        else:
            self.cellDeathCounter[reason] = 1
        
        if reason in self.cellDeathsThisTurn:
            self.cellDeathsThisTurn[reason] += 1
        else:
            self.cellDeathsThisTurn[reason] = 1

    def addCellDeathEscape(self):
        self.cellDeathEscapeCounter += 1
        self.cellDeathEscapesThisTurn += 1

    def addCellPush(self):
        self.cellPushedCounter += 1
        self.cellPushedThisTurn += 1
    
    def addCellAlive(self):
        self.cellAliveCount += 1

    def addCellMove(self):
        self.cellMovedCounter += 1
        self.cellMovedThisTurn += 1

    def addCellStop(self):
        self.cellStoppedCounter += 1
        self.cellStoppedThisTurn += 1

    def addCellForcedSpawn(self):
        self.cellForcedSpawnCounter += 1

    def addCellFailedForcedSpawn(self):
        self.cellFailedForcedSpawnCounter += 1

    def addCellYouth(self):
        self.cellYouthCount += 1
    
    def addCellElderly(self):
        self.cellElderlyCount += 1

    def addCellAdult(self):
        self.cellAdultCount += 1

    def addCellDisintegration(self):
        self.cellDisintegrationCounter += 1

    def addCellDisintegrationDeath(self):
        self.cellDisintegrationDeathCounter += 1

    def getTotalDeath(self):
        total = 0
        for reason in self.cellDeathCounter:
            total += self.cellDeathCounter[reason]
        return total

    def getDeathsThisTurn(self):
        sum = 0
        for reason in self.cellDeathsThisTurn:
            sum += self.cellDeathsThisTurn[reason]
        return sum
    
    def getCellStateChangeTotal(self):
        total = 0
        for reason in self.cellStateChange:
            total += self.cellStateChange[reason]
        return total

    def getCellStateChangesThisTurn(self):
        sum = 0
        for reason in self.cellStateChangeThisTurn:
            sum += self.cellStateChangeThisTurn[reason]
        return sum

    def getCellNextID(self):
        ret = self.cellCounter
        self.cellCounter += 1
        return ret
    
    def addCellStateStable(self):
        self.cellStateStable += 1
        self.cellStateStableThisTurn += 1
    
    def addCellStateChange(self, newState):
        if newState in self.cellStateChange:
            self.cellStateChange[newState] += 1
        else:
            self.cellStateChange[newState] = 1
        
        if newState in self.cellStateChangeThisTurn:
            self.cellStateChangeThisTurn[newState] += 1
        else:
            self.cellStateChangeThisTurn[newState] = 1

    def getHeightAt(self, x, y):
        x, y = self._boundXY((x, y))
        return self.heightGrid[x, y]

    def addHeightAt(self, x, y, amount):
        x, y = self._boundXY((x, y))
        self.heightGrid[x, y] += amount
        return self.heightGrid[x, y]
