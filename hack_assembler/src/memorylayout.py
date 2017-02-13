# Apparently this Harvard architecture that we've used is much simpler because instructions are
# located on a separate ROM and they can't be changed, thus all @labels are going straight to
# RAM. This makes it much much easier to handle. I am a little disappointed actually.


class MemoryLayout:
    """Represents mostly RAM memory of our Hack Computer (Predefined Symbols Map and Labels Map),
     but to make it more universal it also stores any branch references to ROM instructions.
     It's expected to be prefilled with

    """
    def __init__(self):
        # Predefined symbols that map string representations to their RAM memory addresses in DEC
        self.PREDEFINED_SYMBOLS_MAP = {"SP": "0",
                                       "LCL": "1",
                                       "ARG": "2",
                                       "THIS": "3",
                                       "THAT": "4",
                                       "R0": "0",
                                       "R1": "1",
                                       "R2": "2",
                                       "R3": "3",
                                       "R4": "4",
                                       "R5": "5",
                                       "R6": "6",
                                       "R7": "7",
                                       "R8": "8",
                                       "R9": "9",
                                       "R10": "10",
                                       "R11": "11",
                                       "R12": "12",
                                       "R13": "13",
                                       "R14": "14",
                                       "R15": "15",
                                       "SCREEN": "16384",
                                       "KBD": "24576"}

        # Representation of custom labels and their memory allocations in DEC
        self.LABELS_MAP = {}

        # Representation of branches addresses in the instruction memory (ROM).
        self.BRANCHES_MAP = {}

        # Free RAM counter (due to specification it's supposed to start from 16)
        self.FREE_MEMORY_LOCATION = 16

    def get_memory_address(self, memory_label: str) -> int:
        """
        Tries to find previously allocated memory address to provided label(RAM) or
         branch name(ROM). If it doesn't find any then creates a new label allocation in RAM.

        :param memory_label: either a string label or a number representing memory adr.
        :return: allocated memory address in decimal
        """
        if memory_label in self.PREDEFINED_SYMBOLS_MAP:  # is it a predefined symbol?
            return self.PREDEFINED_SYMBOLS_MAP[memory_label]
        elif memory_label in self.BRANCHES_MAP:
            return self.BRANCHES_MAP[memory_label]
        elif memory_label in self.LABELS_MAP:  # was memory label already defined?
            return self.LABELS_MAP[memory_label]
        else:
            # Apparently it's a new label, thus find
            #  a free memory address (in dec) that is >= 16 but < 16384
            if self.FREE_MEMORY_LOCATION >= int(self.PREDEFINED_SYMBOLS_MAP["SCREEN"]):
                raise MemoryError("Out of memory! Memory allocation exceeded 16384 addresses.")
            else:
                self.LABELS_MAP[memory_label] = self.FREE_MEMORY_LOCATION
                self.FREE_MEMORY_LOCATION += 1
                return self.LABELS_MAP[memory_label]

    def allocate_branch(self, branch_name: str, address: int) -> int:
        """
        Inserts new branch allocation into branches_map. It's expected to be called only once
        per given unique branch name else throws a ValueError.

        :param branch_name: string representation of branch_name
        :param address: decimal representation of memory address in ROM
        :return: decimal representation of allocated branch's memory address
        """
        if branch_name in self.BRANCHES_MAP:
            raise ValueError("Provided branch name (%s) has already"
                             " been registered in memory." % branch_name)
        else:
            self.BRANCHES_MAP[branch_name] = address
            return address

    def get_branch_allocation(self, branch_name: str) -> int:
        """
        Returns a decimal ROM address previously allocated for given branch_name, if was wasn't
         allocated yet then throws a ValueError (it's against Hack Assembly rules).

        :param branch_name: string name of a code branch
        :return: decimal ROM address for given label
        """
        if branch_name in self.BRANCHES_MAP:
            return self.BRANCHES_MAP[branch_name]
        else:
            raise ValueError("Provided branch name wasn't registered in RAM yet!")
