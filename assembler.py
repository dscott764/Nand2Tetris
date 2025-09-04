"""A basic assembler for the Hack assembly language.

This script takes a single command-line argument which is the path to an .asm 
file.  It performs the first pass of the assembly process by removing all 
comments and whitespace (including blank lines).

The sanitized code is then written to a new file with the same name but with 
an .hack extension.

Usage:
    python assembler.py YourProgram.asm
"""
import sys
import re


def sanitize(raw_lines):
    """
    Removes comments and whitespace from a list of lines.

    Args:
        raw_lines: A list of strings.

    Returns:
        A new list of strings with comments and whitespace removed.
    """
    cleaned_lines  = []
     
    for line in raw_lines:
        comment_start = line.find('//')

        if comment_start != -1:
            line = line[:comment_start]

        processed_line = line.strip()

        if processed_line:
            cleaned_lines.append(processed_line)

    return cleaned_lines


def convert_c_instruction(c_instruction):
    """
    Converts a c-instruction into machine code. The binary representation of a
    c-instruction is of the form ixxaccccccdddjjj where i is 1.

    Args:
        line: A line containing a c-instruction.

    Returns:
        A string representing a binary number.
    """
    # A c-instruction begins with 1. The following xx bits aren't used.
    machine_code = '111'
    dest = ''
    comp = ''
    jump = ''

    if '=' in c_instruction:
        parts = c_instruction.split('=')
        dest = parts[0]
        c_instruction = parts[1]

    if ';' in c_instruction:
        parts = c_instruction.split(';')
        comp = parts[0]
        jump = parts[1]
    else:
        comp = c_instruction

    comp_codes = {
        '0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100',
        'A': '0110000', 'M': '1110000', '!D': '0001101', '!A': '0110001',
        '!M': '1110001', '-D': '0001111', '-A': '0110011', '-M': '1110011',
        'D+1': '0011111', 'A+1': '0110111', 'M+1': '1110111', 'D-1': '0001110',
        'A-1': '0110010', 'M-1': '1110010', 'D+A': '0000010', 'D+M': '1000010',
        'D-A': '0010011', 'D-M': '1010011', 'A-D': '0000111', 'M-D': '1000111',
        'D&A': '0000000', 'D&M': '1000000', 'D|A': '0010101', 'D|M': '1010101'
    }

    dest_codes = {
        '': '000', 'M': '001', 'D': '010', 'MD': '011',
        'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'
    }

    jump_codes = {
        '': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
        'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'
    }

    try:
        machine_code += comp_codes[comp] + dest_codes[dest] + jump_codes[jump]
        return machine_code
    except KeyError:
        raise ValueError(f'Invalid c-instruction: {c_instruction}')


def convert_to_machine_code(assembler_code):
    """
    Converts assembler code into machine code.

    Args:
        assembler_code: A list of assembler lines.

    Returns:
        A list of machine code.
    """
    machine_code = []

    for line in assembler_code:
        if line.startswith('@'):
            machine_code.append(format(int(line[1:]), '016b'))
        else:
            machine_code.append(convert_c_instruction(line))

    return machine_code


def main():
    """Main function to run the assembler script."""
    try:
        input_filename = sys.argv[1]

        if input_filename.endswith('.asm'):
            output_filename = input_filename.replace('.asm', '.hack')
        else:
            output_filename = input_filename + '.hack'

        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            lines_from_file = infile.readlines()
            sanitized_code = sanitize(lines_from_file)
            machine_code = convert_to_machine_code(sanitized_code)
            output_text = '\n'.join(machine_code) + '\n'
            outfile.write(output_text)

        print(f"Assembly successful! Output written to '{output_filename}'")
    except IndexError:
        print('Error: No file name given.')
        print('Usage: python assembler <file name>')
    except FileNotFoundError:
        print(f"Error: The file '{sys.argv[1]}' wasn't found.")


if __name__ == '__main__':
    main()

