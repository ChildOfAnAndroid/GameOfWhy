# VISUALISATION FILE: GAME OF WHY
# CHARIS CAT 2024

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from functools import partial
import numpy as np
import random
from config import *
from cell import *

class Visualisation:
    def __init__(self, stats, environment):
        # Visualization and Interaction
        self.stats = stats
        self.environment = environment
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.cid = self.fig.canvas.mpl_connect('button_press_event', partial(self.on_click, self))
        top_energy = VISUALISATION_BASE_ENERGY_TOP_RECORD
        for step in range(NUM_STEPS):
            print(f"Step {step} start")
            stats.beginTurn()
            self.ax.clear()
            #ax.imshow(gridSize, alpha=0.5)
            self.ax.imshow(inertGrid, cmap=terrain_colormap, alpha=INERT_GRID_TRANSPARENCY)
            self.ax.imshow(waifuGrid, cmap="BuPu", alpha=ATTRACTIVENESS_GRID_TRANSPARENCY, interpolation="bilinear")
            self.ax.imshow(lightGrid, cmap=purple_yellow_colormap, alpha=LIGHT_GRID_TRANSPARENCY, interpolation="bilinear")

            key = {}
            key["gas"] = {
                "color": (150, 0, 100),
                "count": 0
            }
            for x in range(grid.shape[0]):
                for y in range(grid.shape[1]):
                    cell = grid[x,y]
                    if isinstance(cell, Cell): #and cell.alive:
                        if cell.alive:
                            stats.addCellAlive()
                            try:
                                ax.add_patch(plt.Rectangle((cell.y - 0.5, cell.x - 0.5), 1, 1, color=cell.getCellColor(top_energy), alpha=cell.get_alpha()))
                            except Exception as e:
                                print(f"Color is {cell.get_color(top_energy)} (current energy {cell.energy} top_energy {top_energy}), Alpha is {cell.getCellAlpha()} state: {cell.state} alive: {cell.alive} {cell} ({e})")
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
        # full_key=[]
        # for k in key:
        #     v=key[k]
        #     correct_color=(v["color"][0]/255,v["color"][1]/255,v["color"][2]/255)
        #     patch = mpatches.Patch(color=correct_color, label=f"{v['count']}")
        #     full_key.append(patch)
        # self.ax.legend(handles=full_key)

        self.ax.set_title(f"Step {step + 1} ({stats.cellAliveCount})")
        print(f"Done plotting, {self.stats.cellAliveCount} cells are alive and displayed. Starting env changes")
        plt.pause(0.1)

    def on_click(self, event):
        # Handles mouse clicks to place cells
        if event.xdata is None or event.ydata is None:
            return
        x, y = int(event.ydata), int(event.xdata)
        self.environment.attemptForcedSpawn((x, y))