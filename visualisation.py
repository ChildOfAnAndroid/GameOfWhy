# VISUALISATION FILE: GAME OF WHY
# CHARIS CAT 2024

from scipy.ndimage import gaussian_filter
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from functools import partial
import numpy as np
import random

class Visualisation:
    # Visualization and Interaction
    plt.ion()
    fig, ax = plt.subplots()
    cid = fig.canvas.mpl_connect('button_press_event', partial(on_click, stats))
    top_energy = VISUALISATION_BASE_ENERGY_TOP_RECORD
    for step in range(NUM_STEPS):
        print(f"Step {step} start")
        stats.beginTurn()
        ax.clear()
        #ax.imshow(gridSize, alpha=0.5)
        ax.imshow(inertGrid, cmap=terrain_colormap, alpha=INERT_GRID_TRANSPARENCY)
        ax.imshow(waifuGrid, cmap="BuPu", alpha=ATTRACTIVENESS_GRID_TRANSPARENCY, interpolation="bilinear")
        ax.imshow(lightGrid, cmap=purple_yellow_colormap, alpha=LIGHT_GRID_TRANSPARENCY, interpolation="bilinear")

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
    full_key=[]
    for k in key:
        v=key[k]
        correct_color=(v["color"][0]/255,v["color"][1]/255,v["color"][2]/255)
        patch = mpatches.Patch(color=correct_color, label=f"{v['count']}")
        full_key.append(patch)
    ax.legend(handles=full_key)

    ax.set_title(f"Step {step + 1} ({stats.cellAliveCount})")
    print(f"Done plotting, {stats.cellAliveCount} cells are alive and displayed. Starting env changes")
    plt.pause(0.1)

    def on_click(stats, event):
    # Handles mouse clicks to place cells
    if event.xdata is None or event.ydata is None:
        return
    x, y = int(event.ydata), int(event.xdata)
    if grid[x, y] == 0 or grid[x, y] is None:
        new_cell = Cell(x, y, stats, organism=None)
        counter += 1
        new_cell.role = random.choice(CELL_ROLES)
        grid[x, y] = new_cell
        print(f"Placed a {new_cell.role} cell at ({x}, {y})")

    #if step % 100 == 0:  # Stir the environment every 100 steps
    #    stir_environment(grid)
