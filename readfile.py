# -*- coding: utf-8 -*-

"""
Module

Copyright © 2022 Roman Clavier

Python describing
"""

import argparse
import os
import time

import tools


def main():
    """Main function"""
    args = parser.parse_args()
    base_path = os.path.join(os.getcwd(), "data")

    if args.read:
        if os.path.exists(args.read):
            read_file(args.read)
        elif os.path.exists(os.path.join(base_path, args.read)):
            read_file(args.read)
        else:
            print(f"File not found: {args.read}")
            print("You can give a relative path to access a file in the source folder, or an absolute path to read any "
                  "file.")


def read_file(filename: str):
    """
    Read the given file and build the line.
    :param filename: Path of the file
    :return: None
    """
    sep = None
    columns_count = dict()
    types = dict()
    col_format = "{:<20}\t{:<20}\t{:}"
    headers = None
    editing = True

    with open(filename) as file:
        lines = file.readlines()
    if tools.input_choices("File contains columns?") == "y":
        sep = tools.input_validation("Input the separator used: ")

    for index, line in enumerate(lines):
        line = line.strip()
        split_line = line.split(sep) if sep else [line]
        split_line = [x.strip() for x in split_line if x.strip()]

        for index2, item in enumerate(split_line):
            try:
                split_line[index2] = float(split_line[index2])
            except ValueError:
                pass
            tmp = type(split_line[index2]).__name__
            if tmp in types.keys():
                types[tmp].count += 1
                datalines = types[tmp].lines[-1]
                if datalines.end == index + 1:
                    pass
                elif datalines.end == index:
                    datalines.end = index + 1
                else:
                    types[tmp].lines.append(DataLines(index + 1))
            else:
                types[tmp] = DataCount(1, [DataLines(index + 1)])

        tmp = len(split_line)
        if tmp in columns_count.keys():
            columns_count[tmp].count += 1
            datalines = columns_count[tmp].lines[-1]
            if datalines.end == index:
                datalines.end = index + 1
            else:
                columns_count[tmp].lines.append(DataLines(index + 1))
        else:
            columns_count[tmp] = DataCount(1, [DataLines(index + 1)])

        lines[index] = split_line

    del index, index2, line, item, split_line, file

    tmp = sorted(types.items())
    types.clear()
    for item in tmp:
        types[item[0]] = item[1]

    tmp = sorted(columns_count.items())
    columns_count.clear()
    for item in tmp:
        columns_count[item[0]] = item[1]
    del tmp

    print()
    if len(columns_count) > 1:
        print(f"All lines don't contain the same number of column:")
        print(col_format.format(*("Columns:", "Counted lines:", "Concerned lines:")))
        for item in columns_count.items():
            print(col_format.format(*(item[0], item[1].count, item[1].build_lines_str())))
        print("Is file good written? If no, please check it.")
        if tools.input_choices("Continue run?") == "n":
            tools.exit_program()

    elif len(columns_count) == 1:
        print(f"All lines have the same number of column: {list(columns_count.keys())[0]}")
    else:
        print("File is empty? No column found!")
        tools.exit_program()
    time.sleep(1)

    print()
    if len(types) > 1:
        print(f"Several data types detected:")
        print(col_format.format(*("Data types:", "Counted data:", "Concerned lines:")))
        for item in types.items():
            print(col_format.format(*(item[0], item[1].count, item[1].build_lines_str())))
        del item
        time.sleep(1)

        if "str" in types.keys() and types["str"].lines[0].start == 1:
            print()
            if tools.input_choices("This file contains headers (at line 1)?") == "y":
                headers = lines[0]
                headers_str = " ; ".join(headers)
                print(f"Headers: {headers_str}")
                del headers_str
                time.sleep(1)

        print("\nYou have now three options:")
        print("- [1] (Recommended) Remove all lines where data are not float and continue")
        print("- [2] Accept a risk to raise an error while creating lines and continue")
        print("- [3] Exit now")

        match tools.input_choices("Choice", ["1", "2", "3"]):
            case "1":
                available_types = ["float", "int"]
                index_to_remove = []
                for item in types:
                    if item not in available_types:
                        for dataline in types[item].lines:
                            for index in range(dataline.start - 1, dataline.end):
                                if index not in index_to_remove:
                                    index_to_remove.append(index)

                for index in range(0, len(index_to_remove)):
                    lines.pop(index_to_remove[index] - index)

                del available_types, item, dataline, index, index_to_remove

            case "2":
                pass

            case "3":
                tools.exit_program()

    elif len(types) == 1:
        print(f"All data have the same type: {list(types.keys())[0]}")
        if list(types.keys())[0] != "float":
            print("Data are not float! Can't build any line with them!")
            tools.exit_program()
    else:
        print("File is empty? No column found!")
        tools.exit_program()

    pass


class DataCount:
    """Data count class"""
    def __init__(self, count=1, lines=None):
        if lines is None:
            lines = []
        self.count = count
        self.lines = lines

    def build_lines_str(self):
        result = ""
        for line in self.lines:
            if len(result) != 0:
                result += f" ; "
            if line.start == line.end:
                result += str(line.start)
            elif line.start == line.end - 1:
                result += f"{line.start} ; {line.end}"
            else:
                result += f"{line.start} ... {line.end}"
        return result


class DataLines:
    """Data lines class"""
    def __init__(self, start, end=None):
        if end is None:
            end = start
        self.start = start
        self.end = end


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="main.py CLI")
    parser.add_argument("-r", "--read", type=str, help="read the file selected. You can give a relative path to access "
                                                       "a file in the source folder, or an absolute path to read any "
                                                       "file.")
    # TODO: add user info in readme
    main()
