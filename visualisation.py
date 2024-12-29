# VISUALISATION FILE: GAME OF WHY
# CHARIS CAT 2024

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from functools import partial
from config import *
from cell import *

class Visualisation:
    def __init__(self, stats, environments):
        # Visualization and Interaction
        self.stats = stats
        self.environments = environments
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.cid = self.fig.canvas.mpl_connect('button_press_event', partial(self.on_click, self))

    def runLoop(self, turn):
        top_energy = VISUALISATION_BASE_ENERGY_TOP_RECORD
        print(f"Step {turn} start visualisation")
        self.ax.clear()
        #ax.imshow(gridSize, alpha=0.5)
        self.ax.imshow(self.environments.inertGrid, cmap=INERT_GRID_COLORMAP, alpha=INERT_GRID_TRANSPARENCY)
        self.ax.imshow(self.environments.waifuGrid, cmap="BuPu", alpha=ATTRACTIVENESS_GRID_TRANSPARENCY, interpolation="bilinear")
        self.ax.imshow(self.environments.lightGrid, cmap=LIGHT_GRID_COLORMAP, alpha=LIGHT_GRID_TRANSPARENCY, interpolation="bilinear")
 
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
        plt.pause(0.1)

    # Ends the run after a 60 seconds timer
    def endRun(self, turn):
        exitAfter = 60
        for seconds in range(exitAfter):
            self.ax.set_title(f"Final step {turn}, no alive cell. Ending simulation in {exitAfter - seconds}")
            plt.pause(1.0)
    
    def on_click(self, event):
        # Handles mouse clicks to place cells
        if event.xdata is None or event.ydata is None:
            return
        x, y = int(event.ydata), int(event.xdata)
        self.environment.attemptForcedSpawn((x, y))