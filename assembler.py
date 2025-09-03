import sys


try:
    filename = sys.argv[1]

    with open(filename, 'r') as file:
        content = file.read()
        print(content)
except IndexError:
    print('Error: No file name given.')
    print('Usage: python assembler <file name>')
except FileNotFoundError:
    print(f"Error: The file '{filename}' wasn't found.")

