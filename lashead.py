import argparse
import sys
import os


def test_encoding(filename):
    encodings = ['ascii', 'windows-1252', 'latin-1', 'utf-8']
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


def get_section_list(args):
    args_dict = vars(args)
    args_dict.pop('filename')
    line_numbers = args_dict.pop('line_numbers', False)
    section_list = list(args_dict.values())
    return section_list, line_numbers


def get_section(filename, section=None, line_numbers=False):
    line_number = 0
    text_block = ''
    if not section:
        terminator = '~A'
        section = '~'
    else:
        terminator = '~'
    with open(filename, 'r', encoding=enc) as file_obj:
        line = file_obj.readline()
        while not line.strip().startswith('~A'):
            if line.strip().upper().startswith(section):
                while True:
                    line_number += 1
                    try:
                        if line_numbers:
                            text_block += '{:>3}| {}'.format(line_number, line)
                            line = file_obj.readline()
                        else:
                            text_block += line
                            line = file_obj.readline()
                        if line.strip().startswith(terminator):
                            break
                    except StopIteration:
                        sys.exit('Malformed LAS or not LAS. Exiting.')
            else:
                line_number += 1
                try:
                    line = file_obj.readline()
                except:
                    sys.exit('Malformed LAS or not LAS. Exiting.')
                if (line.strip().startswith(terminator)) and (text_block):
                    break
    return text_block


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-v', '--version', help='display version block',
                        action='store_true')
    parser.add_argument('-w', '--well', help='display well block',
                        action='store_true')
    parser.add_argument('-p', '--parameters', help='display parameters block',
                        action='store_true')
    parser.add_argument('-c', '--curves', help='display curve information block',
                        action='store_true')
    parser.add_argument('-l', '--line-numbers', help='show line numbers',
                        action='store_true')
    args = parser.parse_args()

    filename = args.filename
    if not os.path.isfile(filename):
        sys.exit("Argument provided is not a file. Exiting.")
    enc = test_encoding(filename)

    section_list, line_numbers = get_section_list(args)
    header = ''
    if any(section_list):
        if args.version:
            text_block = get_section(filename, '~V', line_numbers)
            header += text_block
        if args.well:
            text_block = get_section(filename, '~W', line_numbers)
            header += text_block
        if args.parameters:
            text_block = get_section(filename, '~P', line_numbers)
            header += text_block
        if args.curves:
            text_block = get_section(filename, '~C', line_numbers)
            header += text_block
    else:
        text_block = get_section(filename, None, line_numbers)
        header += text_block

    print(header)
