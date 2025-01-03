# VISUALISATION FILE: GAME OF WHY
# CHARIS CAT 2024

import matplotlib.pyplot as plt
from os import makedirs
from os.path import isdir
from config import *
from cell import *

class Visualisation:
    def __init__(self, stats, environments):
        # Visualization and Interaction
        self.stats = stats
        self.environments = environments
        self.displaySignalGrid, self.displayInertGrid, self.displayWaifuGrid, self.displayLightGrid = True,True,True,True
        if not VISUALISATION_OUTPUT_SCREEN_DISABLE:
            plt.ion()
        self.fig, self.ax = plt.subplots()
        self.mousecid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.keycid = self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        if ((VISUALISATION_OUTPUT_FILE_SAVE_EVERY_N_TURNS != False and VISUALISATION_OUTPUT_FILE_SAVE_EVERY_N_TURNS is not None) or\
            VISUALISATION_OUTPUT_FILE_SAVE_FINAL_TURN != False):
            # Create the folders to output
            if not isdir(f"{VISUALISATION_OUTPUT_FILE_SAVE_MAIN_FOLDER}/{VISUALISATION_OUTPUT_FILE_SAVE_SIM_FOLDER}/"):
                makedirs(f"{VISUALISATION_OUTPUT_FILE_SAVE_MAIN_FOLDER}/{VISUALISATION_OUTPUT_FILE_SAVE_SIM_FOLDER}/")

    def runLoop(self, turn, end=False):
        print(f"Step {turn} start visualisation {self.displaySignalGrid}, {self.displayInertGrid}, {self.displayWaifuGrid}, {self.displayLightGrid}")
        if self.needRender(turn, end):
            self.ax.clear()
            #ax.imshow(gridSize, alpha=0.5)
            if self.displaySignalGrid:
                self.ax.imshow(self.environments.signalGrid, cmap="spring", alpha=0.2)
            if self.displayInertGrid:
                self.ax.imshow(self.environments.inertGrid, cmap="plasma", alpha = 0.5) # interpolation = "bilinear"
            if self.displayWaifuGrid:
                self.ax.imshow(self.environments.waifuGrid, cmap="BuPu", alpha=ATTRACTIVENESS_GRID_TRANSPARENCY) # interpolation = "bilinear"
            if self.displayLightGrid:
                self.ax.imshow(self.environments.lightGrid, cmap=LIGHT_GRID_COLORMAP) # interpolation = "bilinear"

            for x in range(self.environments.grid.shape[0]):
                for y in range(self.environments.grid.shape[1]):
                    cell = self.environments.grid[x,y]
                    if isinstance(cell, Cell): #and cell.alive:
                        if cell.alive:
                            self.stats.addCellAlive()
                        try:
                            self.ax.add_patch(plt.Rectangle((cell.y - 0.5, cell.x - 0.5), 1, 1, color=cell.getCellColor()))
                        except Exception as e:
                            print(f"Exception: Color is {cell.getCellColor()} (current energy {cell.energy} top_energy {cell.topEnergy}) ; state: {cell.state} alive: {cell.alive} {cell} ({e})")
            """
            for organism in organisms:
                if organism.is_alive():
                    color = (random.random(), random.random(), random.random())  # Unique color per organism
                    key[organism.organism_id] = {
                        "color": color,
                        "count": len(organism.cells)
                    }
                    for cell in organism.cells:
                        if cell.alive or cell.state == "inert":
                            if cell.state == "gas":
                                key["gas"]["value"] += 1
                            alpha = 0.3 if cell.state == "gas" else 1
                            cell_color = color if cell.state == "living" else "gray"
                            cell_color = (150, 0, 100) if cell.state == "gas" else cell_color
                            ax.add_patch(plt.Rectangle((cell.y - 0.5, cell.x - 0.5), 1, 1, color=cell_color, alpha=alpha))
                    organism.attempt_sentience()  # Check for sentience
                    if organism.name:
                        print(f"Organism {organism.organism_id} has named itself: {organism.name}")
            """
            # key = {}
            # key["gas"] = {
            #     "color": (150, 0, 100),
            #     "count": 0
            # }
            # full_key=[]
            # for k in key:
            #     v=key[k]
            #     correct_color=(v["color"][0]/255,v["color"][1]/255,v["color"][2]/255)
            #     patch = mpatches.Patch(color=correct_color, label=f"{v['count']}")
            #     full_key.append(patch)
            # self.ax.legend(handles=full_key)

            self.ax.set_title(f"Step {turn + 1} ({self.stats.cellAliveCount})")
            print(f"Done plotting, {self.stats.cellAliveCount} cells are alive and displayed")
            if self.needSave(turn, False):
                self.saveToFile(turn, False)
            if not VISUALISATION_OUTPUT_SCREEN_DISABLE:
                plt.pause(0.1)

    # Ends the run after a 60 seconds timer
    def endRun(self, turn):
        if self.needSave(turn, True):
            self.saveToFile(turn, True)
        if not VISUALISATION_OUTPUT_SCREEN_DISABLE:
            exitAfter = 60
            for seconds in range(exitAfter):
                self.ax.set_title(f"Final step {turn},. Ending simulation in {exitAfter - seconds}")
                plt.pause(1.0)
            plt.ioff()
    
    def needRender(self, turn, end):
        return (not VISUALISATION_OUTPUT_SCREEN_DISABLE and \
            turn % VISUALISATION_OUTPUT_UPDATE_EVERY_N_TURN == 0 ) or \
            self.needSave(turn, end)

    def needSave(self, turn, end):
        return (VISUALISATION_OUTPUT_FILE_SAVE_EVERY_N_TURNS and (turn % VISUALISATION_OUTPUT_FILE_SAVE_EVERY_N_TURNS == 0)) or \
               (end and VISUALISATION_OUTPUT_FILE_SAVE_FINAL_TURN)

    def saveToFile(self, turn, end):
        plt.savefig(f"{VISUALISATION_OUTPUT_FILE_SAVE_MAIN_FOLDER}/{VISUALISATION_OUTPUT_FILE_SAVE_SIM_FOLDER}/Turn_{turn}.{VISUALISATION_OUTPUT_FILE_SAVE_FORMAT}")

    def on_click(self, event):
        # Handles mouse clicks to place cells
        if event.xdata is None or event.ydata is None:
            return
        x, y = int(event.ydata), int(event.xdata)
        self.environments.attemptForcedSpawn((x, y))

    def on_key(self, event):
        match event.key:
            case "d":
                print("Signal grid")
                self.displaySignalGrid = not self.displaySignalGrid
            case "i":
                print("Inert grid")
                self.displayInertGrid = not self.displayInertGrid
            case "w":
                print("Waifu grid")
                self.displayWaifuGrid = not self.displayWaifuGrid
            case "l":
                print("Light grid")
                self.displayLightGrid = not self.displayLightGrid
        return