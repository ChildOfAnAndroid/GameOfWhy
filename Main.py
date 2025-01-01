# MAIN FILE: GAME OF WHY
# CHARIS CAT 2024

from automaton import *
from environment import *
from stats import *
from visualisation import *

class Main:
    """

    pre game:
    initialise environment
    initialise cells


    each turn:
    revisualise
    move cells
    refresh environment

    end of turn:
    print results

    end of game:
    print results

    """

    def __init__(self):
        self.stats = Stats()
        self.environments = Environment(self.stats)
        self.automaton = Automaton(self.stats, self.environments)
        self.visualisation = Visualisation(self.stats, self.environments)
        self.simulationRecorder = SimulationRecorder()

    def run(self):
        for turn in range(NUM_STEPS+1):
            self.runLoop(turn, turn == NUM_STEPS)
        
        self.stats.endRun()
        self.visualisation.endRun(NUM_STEPS)
        self.simulationRecorder.end()

    def runLoop(self, turn, end):
        self.stats.beginTurn()
        self.environments.runLoop(turn)
        self.visualisation.runLoop(turn, end=end)
        self.automaton.runLoop(turn)
        self.stats.endTurn()
        self.simulationRecorder.endTurn()


# Set it to auto-run this file
if __name__ == "__main__":
    main = Main()
    main.run()