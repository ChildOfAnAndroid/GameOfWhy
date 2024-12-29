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

    def run(self):
        for turn in range(NUM_STEPS):
            self.stats.beginTurn()
            self.visualisation.runLoop(turn)
            self.environments.runLoop(turn)
            self.automaton.runLoop(turn)
            self.stats.endTurn()

            # Early exit condition: nothing is alive anymore
            if not self.environments.isAlive():
                print("All cells have become inert. You may want to... leave now.")
        
        self.stats.endRun()
        self.visualisation.endRun(NUM_STEPS)


# Set it to auto-run this file
main = Main()
main.run()