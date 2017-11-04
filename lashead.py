import sys
import os


def test_encoding(filename):
    encodings = ['ascii', 'windows-1252', 'utf-8']
    for i in encodings:
        enc = i
        f = open(filename, 'r', encoding=enc)
        try:
            next(f)
            f.close()
            break
        except UnicodeDecodeError:
            f.close()
            pass
        enc = None
    return enc


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        sys.exit("Must provide file name as argument. Exiting.")

    if not os.path.isfile(filename):
        sys.exit("Argument provided is not a file. Exiting.")

    enc = test_encoding(filename)

    with open(filename, 'r', encoding=enc) as f:
        line_number = 0
        header = ''
        while True:
            line_number += 1
            try:
                line = next(f)
                header += line
                if line.strip().startswith('~A'):
                    break
            except StopIteration:
                sys.exit('Malformed LAS or not LAS. Exiting.')

    print(header)
