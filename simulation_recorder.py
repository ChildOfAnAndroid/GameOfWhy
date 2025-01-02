from functools import partial, wraps
from os import makedirs
from os.path import isdir

from config import VISUALISATION_OUTPUT_FILE_SAVE_MAIN_FOLDER, VISUALISATION_OUTPUT_FILE_SAVE_SIM_FOLDER, \
                   RECORDER_PRINT_TO_STDOUT, RECORDER_PRINT_TO_FILE, CELL_MEMORY_DISPLAY_MODE, \
                   RECORDER_STATS_DEFINITION, RECORDER_PRINT_MEMORIES

def singleton(cls):
    """Make a class a Singleton class (only one instance)"""
    @wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if wrapper_singleton.instance is None:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance
    wrapper_singleton.instance = None
    return wrapper_singleton

@singleton
class SimulationRecorder:
    recorder = None
    def __init__(self):
        if not isdir(f"{VISUALISATION_OUTPUT_FILE_SAVE_MAIN_FOLDER}/{VISUALISATION_OUTPUT_FILE_SAVE_SIM_FOLDER}"):
            makedirs(f"{VISUALISATION_OUTPUT_FILE_SAVE_MAIN_FOLDER}/{VISUALISATION_OUTPUT_FILE_SAVE_SIM_FOLDER}")
        self.outputStreams = []
        if RECORDER_PRINT_TO_FILE:
            self.cellRecorder = open(f"{VISUALISATION_OUTPUT_FILE_SAVE_MAIN_FOLDER}/{VISUALISATION_OUTPUT_FILE_SAVE_SIM_FOLDER}/record.txt", "x")
            self.outputStreams.append(partial(self.writeToFile, self.cellRecorder))

        if RECORDER_PRINT_TO_STDOUT:
            self.outputStreams.append(self.writeToStdout)

        self.recorder = self
        self.cellArchive = {}
        self.records = []
        self.birthRecordPattern = None
        self.deathRecordPattern = None

    def statNameToDisplayName(self, name):
        display = ""
        for x in name:
            if x.isupper():
                display += " " + x
            else:
                display += x
        return display.title()

    def getBirthRecordPattern(self):
        if self.birthRecordPattern is None:
            self.birthRecordPattern = "Hey, Cell {id} here. Just passing on my birth certificate!\n"
            statsToWrite = self.getStatDefinition()
            for stat in statsToWrite:
                name = stat["name"] if "name" in stat else self.statNameToDisplayName(stat["stat"])
                if "display" in stat:
                    if not stat["display"] is False:
                        self.birthRecordPattern += f"{name:>25} | {{birth_{stat['stat']}:>20{stat['display']}}} |\n"
                else:
                    self.birthRecordPattern += f"{name:>25} | {{birth_{stat['stat']}:>20}} |\n"
        
        return self.birthRecordPattern

    def getDeathRecordPattern(self):
        if self.deathRecordPattern is None:
            self.deathRecordPattern = "Hey, Cell {id} here. Just passing on my memoir... at: {death_age:.2f}:\n"
            self.deathRecordPattern += "My Dear Parent is Cell {parent}\n"
            statsToWrite = self.getStatDefinition()
            for stat in statsToWrite:
                name = stat["name"] if "name" in stat else self.statNameToDisplayName(stat["stat"])
                if "display" in stat:
                    if not stat["display"] is False:
                        self.deathRecordPattern += f"{name:>25} | {{birth_{stat['stat']}:>20{stat['display']}}} | {{death_{stat['stat']}:<20{stat['display']}}} |\n"
                else:
                    self.deathRecordPattern += f"{name:>25} | {{birth_{stat['stat']}:>20}} | {{death_{stat['stat']}:<20}} |\n"
        return self.deathRecordPattern

    def end(self):
        if RECORDER_PRINT_TO_FILE:
            self.cellRecorder.close()

    def endTurn(self):
        self.printRecords()

    def writeToFile(self, file, str):
        file.write(str + "\n")

    def writeToStdout(self, str):
        print(str)

    def recordBirth(self, cell):
        self.cellArchive[cell.id] = {
            "cell": cell,
            "stats": self.buildStatArray(cell, True)
        }
        # self.records.append(("birth", self.cellArchive[cell.id]))

    def recordDeath(self, cell):
        if not cell.id in self.cellArchive:
            raise Exception(f"This cell {cell.id} ({cell}) wasn't registered at birth")
        
        self.cellArchive[cell.id]["stats"] |= self.buildStatArray(cell, False)
        self.records.append(("death", self.cellArchive[cell.id]))

        del self.cellArchive[cell.id]

    def getStatDefinition(self):
        return RECORDER_STATS_DEFINITION

    def buildStatArray(self, cell, isBirth):
        if isBirth:
            prefix = "birth_"
        else:
            prefix = "death_"
        statsToRecord = self.getStatDefinition()
        stats = {}
        for property in statsToRecord:
            if "prefix" in property:
                stat = property["prefix"] + property["stat"]
            else:
                stat = prefix + property["stat"]
            if "record" in property:
                stats[stat] = property["record"](cell, isBirth)
            else:
                if hasattr(cell, property["stat"]):
                    stats[stat] = getattr(cell, property["stat"])
                else:
                    raise Exception(f"Unable to find property {property["stat"]} on cell {cell.id} ({cell})")

        return stats

    def printRecords(self):
        for record in self.records:
            self.printRecord(record)
        
        self.records.clear()

    def printRecord(self, record):
        str_record = self.getRecord(*record)
        for stream in self.outputStreams:
            stream(str_record)
    
    def getMemories(self, cell):
        memories = []

        if CELL_MEMORY_DISPLAY_MODE == "event":
            summary = {}

            for memory_entry in cell.memory:
                if len(memory_entry) == 3:
                    turn_count, memory_type, details = memory_entry
                elif len(memory_entry) == 2:
                    turn_count, memory_type = memory_entry
                    details = None
                else:
                    print(f"Unexpected memory format: {memory_entry}")
                    continue

                # Aggregate memory by type
                if memory_type not in summary:
                    summary[memory_type] = []
                summary[memory_type].append({
                    "turn": turn_count,
                    "details": details})

            # Output the summary
            memories.append("Memory Summary:")
            for memory_type, entries in summary.items():
                memories.append(f"{memory_type}:")
                for entry in entries:
                    if entry["details"] is None:
                        memories.append(f"  Turn {entry['turn']}")
                    else:
                        memories.append(f"  Turn {entry['turn']}: {entry['details']}")
        elif CELL_MEMORY_DISPLAY_MODE == "turn":
            last_turn = -1
            for memory_entry in cell.memory:
                if len(memory_entry) == 3:
                    turn_count, memory_type, details = memory_entry
                elif len(memory_entry) == 2:
                    turn_count, memory_type = memory_entry
                    details = None
                else:
                    print(f"Unexpected memory format: {memory_entry}")
                    continue
                if turn_count > last_turn:
                    last_turn = turn_count
                    memories.append(f"On Turn {turn_count}:")
                if details is None:
                    memories.append(f"  {memory_type}")
                else:
                    memories.append(f"  {memory_type}: {details}")

        return "\n".join(memories)

    def getRecord(self, kind, record):
        cell, stats = record["cell"], record["stats"]
        if kind == "birth":
            get_record_pattern = self.getBirthRecordPattern
        else:
            get_record_pattern = self.getDeathRecordPattern
        header = get_record_pattern().format(**stats)
        if RECORDER_PRINT_MEMORIES:
            memories = self.getMemories(cell)
            return header + "\n" + memories

        return header # + "\n" + memories