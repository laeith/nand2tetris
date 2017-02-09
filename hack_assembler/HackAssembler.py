# define dictionaries representing instructions and their binary parts
# syntax: dest = comp ; jump
# or: @value / @variable <- memory pointer
#
# A-type instructions (ie. @15) is a memory pointer
# C-type instructions follow: 'dest = comp ; jump' where dest, comp and jump are instructions
# from corresponding dictionaries
#
# Binary format follows something like this (16 bit instructions):
# A z z a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3
# for detailed meaning of each bit take a look at Chapter 6

import sys

DEST = {"null": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111"}

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

JUMP = {"null": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"}

# initialize symbol table with all pre-defined symbols
SYMBOLS = {}


def compile(input_file):
    line_counter = 0;
    print("Compilation started \n")

    # first pass - extract variables and label symbols

    for line in input_file:
        line = line.strip()
        if line:  # omit empty lines
            try:
                line_counter += 1
                binary_code = parse(line)
                print(line + "\t => \t" + binary_code)
            except ValueError as error:
                print("Line %s:'%s' contains an error: %s" % (line_counter, line, error))


def parse(line):
    binary_code = ""

    if is_valid_A_instruction(line):  # is it A-type instruction?
        binary_code += "0"  # requires 15 more bits representing memory
        binary_code += translate_to_binary_address(line[1:])
    elif is_valid_C_instruction(line):  # is it C-type instruction?
        # validate syntax
        binary_code += "C type instruction"
    return binary_code


def translate_to_binary_address(memory_address_representation):
    # memory address -> 15-bit binary memory address
    # although it also translates built-in and custom symbols [TODO]
    binary_address = bin(int(memory_address_representation))[3:19]

    if len(binary_address) < 15:  #
        padding = "0" * (15 - len(binary_address))
        binary_address = padding + binary_address

    return binary_address


def is_valid_A_instruction(line):
    return line.startswith('@') and not ' ' in line


def is_valid_C_instruction(line):
    # DEST = COMP; JUMP
    if ';' in line:
        split = line.split(';')
        if '=' in split[0]:
            split2 = split.split('=')
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


if __name__ == "__main__":
    args = sys.argv

    if len(args) != 2 or not args[1].endswith('.asm'):
        print(
            "Incorrect arguments, specify exacly one argument with filename name ie. "
            "'HackAssembler somefile.asm', file has to end with .asm extension.")
    else:
        file_name = args[1]
        with open(file_name, 'r') as source:
            compile(source)
