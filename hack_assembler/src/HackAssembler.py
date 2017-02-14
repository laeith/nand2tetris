# define dictionaries representing instructions and their binary parts
# syntax: dest = comp ; jump
# or: @value / @variable <- memory pointer
#
# A-type instructions (ie. @15) are memory pointers
# C-type instructions follow: 'dest = comp ; jump' where dest, comp and jump are instructions
# from corresponding dictionaries
#
# Binary format follows something like this (16 bit instructions):
# A z z a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3
# for detailed meaning of each bit take a look at Chapter 6


import sys
import re
from memorylayout import MemoryLayout

global CURRENT_MEMORY_LAYOUT  # Memory layout of currently compiled file.

DEST = {"null": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111"}

JUMP = {"null": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"}

COMP = {"0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "-D": "0001111",
        "-A": "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",
        "M": "1110000",
        "!M": "1110001",
        "-M": "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101"}


def assemble(file_name) -> list:
    """Entry point for compilation (assembling) process.

    :param file_name: file path (ie. something.asm)
    :return: a list of tuples: (line_number, assembly_code_line, machine_code_line)
    """

    global CURRENT_MEMORY_LAYOUT
    CURRENT_MEMORY_LAYOUT = MemoryLayout()  # New compilation - new memory layout needed in case
                                            # the program wasn't restarted after last compilation

    translation = []

    # First iteration - find all labels and allocate their ROM addresses
    allocate_all_branches(file_name)

    # Second iteration - actual compilation from Hack Language to machine code
    with open(file_name, 'r') as input_file:
        line_counter = 0
        for line in input_file:
            line = strip_asm_line(line)
            if line and not line.startswith("//") and not line.startswith(
                    "("):  # omit empty lines TODO: doesn't strip asm do the same for //?
                try:
                    output = parse(line)
                except (ValueError, KeyError) as error:
                    output = "Line %s:'%s' contains an error: %s" % (line_counter, line, error)
                    print(output)
                finally:
                    translation.append((line_counter, line, output))
            line_counter += 1
    return translation


def allocate_all_branches(file_name: str) -> None:
    """
    Goes through *.asm source code, finds and allocates memory (ROM) for each unique branch label
    using previously created MemoryLayout object (by assemble function). Thus watch out, unlike
    most of these functions this one is NOT PURE.

    :param file_name: string of relative or absolute file path including file extension
    """
    global CURRENT_MEMORY_LAYOUT

    with open(file_name, 'r') as input_file:
        current_ROM_address = 0
        for line in input_file:
            line = line.strip().replace(" ", "")
            if line and not line.startswith("//"):
                if re.fullmatch('\(([^)( ]+)\)', line):
                    CURRENT_MEMORY_LAYOUT.allocate_branch(line[1:-1], current_ROM_address)
                    current_ROM_address -= 1
                current_ROM_address += 1


def parse(line: str) -> str:
    """ Tries to validate provided line and find out which instruction was given, then translates
    those into their corresponding machine code (16-bit binary instructions).

    :param line: A-type or C-type instruction
    :return: 16-bit binary instruction for Hack machine code
    """
    if is_valid_A_instruction(line):  # is it A-type instruction?
        binary_code = "0"
        binary_code += translate_A_instruction(line[1:])
    elif is_valid_C_instruction(line):  # is it C-type instruction?
        binary_code = "111"
        binary_code += translate_C_instruction(line)
    else:
        raise ValueError("Provided line isn't neither A-type nor C-type instruction")
    return binary_code


def translate_A_instruction(memory_address_representation: str) -> str:
    """
    Translates A-type instruction (ie. '@15' or '@label_name') into machine code.

    :param memory_address_representation: string representation of memory address (decimal) or
            label.
    :return: 15-bit memory address
    """
    if memory_address_representation.isdigit():
        return to_binary_from_dec(int(memory_address_representation))
    else:
        decimal_memory = CURRENT_MEMORY_LAYOUT.get_memory_address(memory_address_representation)
        return to_binary_from_dec(decimal_memory)


def to_binary_from_dec(memory_address_representation: int) -> bin:
    binary_address = bin(int(memory_address_representation))[2:19]
    if len(binary_address) < 15:
        padding = "0" * (15 - len(binary_address))
        binary_address = padding + binary_address
    return binary_address


def translate_C_instruction(line: str) -> str:
    """
    Translates C-type instruction (ie. 'D=1' or jumps) into machine code

    :param line: Hack Language code line representing C-type instruction
    :return: 13-bit representation of C-type instruction in machine code
    """
    binary_dest = DEST['null']
    binary_jump = JUMP['null']
    binary_comp = ""  # binary comp is a required instruction

    if ';' in line:  # Is it a jump instruction?
        split_jump = line.split(';')
        binary_jump = JUMP[split_jump[1]]
        if '=' in split_jump[0]:  # does it contain assignment?
            split_assignment = split_jump[0].split("=")
            binary_dest = DEST[split_assignment[0]]
            binary_comp = COMP[split_assignment[1]]
        elif split_jump[0] in COMP:
            binary_comp = COMP[split_jump[0]]
        else:
            raise ValueError("COMP instruction was either not provided or incorrectly declared.")
    elif '=' in line:  # Is it C-type instruction but not a jumping one?
        split_assignment = line.split("=")
        if (split_assignment[0] not in DEST) or (split_assignment[1] not in COMP):
            raise ValueError("Either DEST or COMP value was incorrectly declared.")
        binary_dest = DEST[split_assignment[0]]
        binary_comp = COMP[split_assignment[1]]

    if not binary_comp:
        raise ValueError("COMP value is missing but is required")

    return binary_comp + binary_dest + binary_jump


def is_valid_A_instruction(line: str) -> bool:
    return line.startswith('@') and ' ' not in line


def is_valid_C_instruction(line: str) -> bool:
    if ';' in line:
        split = line.split(';')
        if '=' in split[0]:
            split2 = split[0].split('=')
            if (split2[0] not in DEST) or (split2[1] not in COMP):
                raise ValueError('Incorrect DEST or COMP value.')
        if (split[1] not in JUMP) or (split[0] not in COMP):
            raise ValueError('Incorrect JUMP instruction.')
        return True
    elif '=' in line:
        split2 = line.split('=')
        if (split2[0] not in DEST) or (split2[1] not in COMP):
            raise ValueError('Incorrect DEST or COMP value.')
        return True
    return False


def strip_asm_line(line: str) -> str:
    if "//" in line:
        comment_start = line.find('//')
        line = line[:comment_start]
    line = line.strip().replace(" ", "")
    return line


if __name__ == "__main__":
    args = sys.argv

    if len(args) > 2 or not args[1].endswith('.asm'):
        print(
            "Incorrect arguments, specify exactly one argument with filename name ie. "
            "'HackAssembler somefile.asm', file has to have a *.asm extension.")
    else:
        file_name = args[1]
        print("Starting the compilation process...")
        translation = assemble(file_name)
        output_name = args[1][:-4] + ".hack"
        print("Compilation finished, writing to %s" % output_name)
        with open(output_name, "w+") as output_file:
            for line_number, line, machine_code in translation:
                output_file.write(machine_code + "\n")

        print("Compilation has finished >> " + output_name)
