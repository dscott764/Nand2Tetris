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
            output_text = '\n'.join(sanitized_code) + '\n'
            outfile.write(output_text)

        print(f"Assembly successful! Output written to '{output_filename}'")
    except IndexError:
        print('Error: No file name given.')
        print('Usage: python assembler <file name>')
    except FileNotFoundError:
        print(f"Error: The file '{sys.argv[1]}' wasn't found.")


if __name__ == '__main__':
    main()

