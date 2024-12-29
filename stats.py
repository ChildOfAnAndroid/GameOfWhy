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

        # birth statistics
        self.cellBabyCounter = 0
        self.cellBabysFailedCounter = 0
        self.cellForcedSpawnCounter = 0
        self.cellFailedForcedSpawnCounter = 0

        # Movement statistics
        self.cellMovedCounter = 0
        self.cellPushedCounter = 0

        # TURN STATISTICS
        self.cellBabysThisTurn = 0
        self.cellBabysFailedThisTurn = 0
        self.cellDeathsThisTurn = {}
        self.cellDeathEscapesThisTurn = 0
        self.cellMovedThisTurn = 0
        self.cellPushedThisTurn = 0
        self.cellAliveCount = 0

    def beginTurn(self):
        self.cellBabysThisTurn = 0
        self.cellDeathsThisTurn = {}
        self.cellDeathEscapesThisTurn = 0
        self.cellBabysFailedThisTurn = 0
        self.cellAliveCount = 0
        self.cellPushedThisTurn = 0
        self.cellMovedThisTurn = 0

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
Total Cell Escapes: {self.cellDeathEscapeCounter}

# Birth Statistics
Total Cell Babies: {self.cellBabyCounter} (manual {self.cellForcedSpawnCounter})
Total Cell Skipped Babies: {self.cellBabysFailedCounter} (manual {self.cellFailedForcedSpawnCounter})

# Movement Statistics
Total Cell Movements: {self.cellMovedCounter}
Total Cell Pushed: {self.cellPushedCounter}

# Turn Statistics
Cell Babies: {self.cellBabysThisTurn}
Cell Skipped Babies: {self.cellBabysFailedThisTurn}
Cell Death: {self.getDeathsThisTurn()}
{"\n".join([f"{x}: {self.cellDeathsThisTurn[x]}" for x in self.cellDeathsThisTurn])}
Cell Escapes: {self.cellDeathEscapesThisTurn}
Cell Movements: {self.cellMovedThisTurn}
Cell Pushes: {self.cellPushedThisTurn}
Cells Alive: {self.cellAliveCount}
"""

    def addCellBaby(self):
        self.cellBabyCounter += 1
        self.cellBabysThisTurn += 1
    
    def addCellBabyFailed(self):
        self.cellBabysFailedCounter += 1
        self.cellBabysFailedThisTurn += 1
    
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

    def addCellForcedSpawn(self):
        self.cellForcedSpawnCounter += 1

    def addCellFailedForcedSpawn(self):
        self.cellFailedForcedSpawnCounter += 1

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

    def getCellNextID(self):
        ret = self.cellCounter
        self.cellCounter += 1
        return ret
