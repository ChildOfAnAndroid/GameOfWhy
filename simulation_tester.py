import json
from config import NUM_STEPS  # Import NUM_STEPS from the config
from cell import Cell  # Import the Cell class to resolve NameError

def run_simulation_and_log(main_class, output_file="simulation_metrics.log"):
    """
    Runs the simulation using the provided main class and logs metrics to the specified output file.
    
    Args:
        main_class: The entry point of the simulation.
        output_file: Path to the log file for storing metrics.
    """
    log_data = {
        "turns": [],
        "summary": {
            "total_energy_gain": 0,
            "total_energy_loss": 0,
            "total_births": 0,
            "total_deaths": 0,
            "state_changes": {},
            "critical_cells": [],
            "average_energy": 0,
            "max_energy": 0,
            "min_energy": float("inf"),
            "environment_metrics": {},
            "movement_patterns": [],
            "resource_stats": [],
            "problematic_cells": [],
            "energy_sources": [],
            "light_and_nutrients": []  # Track light and nutrient values for each cell
        },
    }

    simulation = main_class()

    # Use NUM_STEPS from config for total_turns
    total_turns = NUM_STEPS

    for turn in range(total_turns):
        turn_data = {
            "turn": turn,
            "energy_gain": {},
            "energy_loss": {},
            "state_changes": {},
            "births": 0,  # Ensure births is initialized as an integer
            "deaths": 0,
            "critical_cells": [],
            "average_energy": 0,
            "max_energy": 0,
            "min_energy": float("inf"),
            "environment_metrics": {},
            "movement_logs": [],
            "resource_logs": {},
            "energy_sources": {},
            "light_and_nutrients": {}  # Log light and nutrients for each cell
        }

        # Step the simulation forward
        if hasattr(simulation, 'runLoop') and callable(getattr(simulation, 'runLoop')):
            simulation.runLoop(turn)
        else:
            print("Error: The Main class does not define a 'runLoop()' method.")
            break

        # Log cell energy data
        total_gain = 0
        total_loss = 0
        energy_sum = 0
        max_energy = float("-inf")
        min_energy = float("inf")

        for x in range(simulation.environments.grid.shape[0]):
            for y in range(simulation.environments.grid.shape[1]):
                cell = simulation.environments.getCellAt(x, y)
                if isinstance(cell, Cell) and cell.alive:
                    # Directly calculate energy gain/loss by tracking changes
                    previous_energy = getattr(cell, 'previousEnergy', cell.energy)
                    energy_gain = max(0, cell.energy - previous_energy)
                    energy_loss = max(0, previous_energy - cell.energy)

                    # Update total gain/loss
                    total_gain += energy_gain
                    total_loss += energy_loss

                    # Save current energy for the next turn
                    setattr(cell, 'previousEnergy', cell.energy)

                    # Aggregate metrics
                    energy_sum += cell.energy
                    max_energy = max(max_energy, cell.energy)
                    min_energy = min(min_energy, cell.energy)

                    # Use a string key for JSON compatibility
                    position_key = f"({x}, {y})"
                    turn_data["energy_gain"][position_key] = energy_gain
                    turn_data["energy_loss"][position_key] = energy_loss

                    # Log energy sources
                    sources = getattr(cell, 'energySources', {})  # Example: {"light": value, "nutrients": value}
                    turn_data["energy_sources"][position_key] = sources

                    # Log light and nutrients from the environment
                    light_value = simulation.environments.lightGrid[x, y]
                    turn_data["light_and_nutrients"][position_key] = {
                        "light": light_value,
                        "nutrients": light_value  # Assuming light and nutrients are the same
                    }

                    # Track movement patterns
                    previous_position = getattr(cell, 'previousPosition', (-1, -1))
                    if previous_position != (x, y):
                        turn_data["movement_logs"].append({
                            "id": cell.id,
                            "from": previous_position,
                            "to": (x, y)
                        })
                        setattr(cell, 'previousPosition', (x, y))

                    # Identify critical cells (low energy or other metrics)
                    if cell.energy < 10:  # Example threshold for critical energy
                        turn_data["critical_cells"].append({
                            "id": cell.id,
                            "energy": cell.energy,
                            "state": cell.state,
                            "position": (x, y)
                        })

                    # Identify problematic cells (high energy gain/loss or unexpected behavior)
                    if energy_gain > 1000 or energy_loss > 1000:  # Example thresholds
                        log_data["summary"]["problematic_cells"].append({
                            "turn": turn,
                            "id": cell.id,
                            "energy": cell.energy,
                            "gain": energy_gain,
                            "loss": energy_loss,
                            "position": (x, y)
                        })

        turn_data["average_energy"] = energy_sum / simulation.stats.cellAliveCount if simulation.stats.cellAliveCount else 0
        turn_data["max_energy"] = max_energy
        turn_data["min_energy"] = min_energy

        # Log births and deaths
        turn_data["births"] = sum(simulation.stats.cellBabysThisTurn.values()) if isinstance(simulation.stats.cellBabysThisTurn, dict) else simulation.stats.cellBabysThisTurn
        turn_data["deaths"] = simulation.stats.getDeathsThisTurn()

        # Log state changes
        for state, count in simulation.stats.cellStateChangeThisTurn.items():
            if state not in log_data["summary"]["state_changes"]:
                log_data["summary"]["state_changes"][state] = 0
            log_data["summary"]["state_changes"][state] += count

            turn_data["state_changes"][state] = count

        # Log environment metrics
        environment = simulation.environments
        light_min, light_max = environment.lightGrid.min(), environment.lightGrid.max()
        attractiveness_min, attractiveness_max = environment.waifuGrid.min(), environment.waifuGrid.max()
        turn_data["environment_metrics"] = {
            "light_min": light_min,
            "light_max": light_max,
            "attractiveness_min": attractiveness_min,
            "attractiveness_max": attractiveness_max,
            "light_sum": environment.lightGrid.sum(),  # Total light value in the grid
            "attractiveness_sum": environment.waifuGrid.sum(),  # Total attractiveness in the grid
        }

        # Track resource logs
        turn_data["resource_logs"] = {
            "light_min": light_min,
            "light_max": light_max,
            "light_sum": environment.lightGrid.sum(),
        }

        # Aggregate metrics
        log_data["summary"]["total_energy_gain"] += total_gain
        log_data["summary"]["total_energy_loss"] += total_loss
        log_data["summary"]["total_births"] += turn_data["births"]
        log_data["summary"]["total_deaths"] += turn_data["deaths"]
        log_data["summary"]["average_energy"] = energy_sum / simulation.stats.cellAliveCount if simulation.stats.cellAliveCount else 0
        log_data["summary"]["max_energy"] = max(log_data["summary"].get("max_energy", float("-inf")), max_energy)
        log_data["summary"]["min_energy"] = min(log_data["summary"].get("min_energy", float("inf")), min_energy)

        # Add movement patterns and resources per turn
        log_data["summary"]["movement_patterns"].extend(turn_data["movement_logs"])
        log_data["summary"]["resource_stats"].append(turn_data["resource_logs"])

        # Add critical cells for this turn
        log_data["summary"]["critical_cells"].extend(turn_data["critical_cells"])

        log_data["turns"].append(turn_data)

    # Write log data to the output file
    with open(output_file, "w") as f:
        json.dump(log_data, f, indent=4, ensure_ascii=False)

    print(f"Simulation metrics logged to {output_file}")

# Usage example
if __name__ == "__main__":
    from Main import Main  # Assuming Main is the entry point

    # Run the simulation and log data
    run_simulation_and_log(Main)
