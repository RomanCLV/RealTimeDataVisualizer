# -*- coding: utf-8 -*-

"""
Command helper module

Copyright © 2021 Roman Clavier

Get the list of available commands, their details, and other actions, using a command parser.
"""

import argparse
import os

parser = argparse.ArgumentParser(description='Command helper')
parser.add_argument("-d", "--details", metavar="", required=False, type=str, help="get the details of the given command. Usage: command_helper.py -d n")
parser.add_argument("-e", "--extract", metavar="", required=False, type=str, help="extract command details to a file. Usage: command_helper.py -e filename.txt")
group = parser.add_mutually_exclusive_group()
group.add_argument("-l", "--list", action="store_true", help="get the list of available commands. Usage: command_helper.py -l")
group.add_argument("-f", "--full", action="store_true", help="full extraction. Usage: command_helper.py -e filename.txt -f")
args = parser.parse_args()


def get_command_list():
    """Get the list of the available commands"""
    return [
        "-n",
        "-ruf",
        "-s",
        "-dc",
        "-mv",
        "-aa",
        "-aas",
        "-at",
        "-albl",
        "-sa",
        "-clra",
        "-ra",
        "-al",
        "-cl",
        "-ml",
        "-clrl",
        "-rl",
        "-h",
        "-w",
        "-ws",
        "-l",
        "-lw",
        "-lws",
        "-ld"
    ]


def get_command_details(command: str):
    """
    Get command's details (description and args details).
    :param command: A string corresponding to a command.
    :return: 4 strings corresponding to the command, its name, its description and its argument details.
    """
    match command:
        case "-n":
            name = "New"
            description = "Initialize program. Create a new save file. If a graph already exists, it is cleaned up.\n" \
                          "Remove Unused Files can also be set. See command -ruf.\n" \
                          "To set to True, you can use a non-zero integer, \"true\" or \"True\".\n" \
                          "To set to False, you can use 0, \"false\" or \"False\"."
            arg = "[ruf*:bool]"
            examples = "-n        => Initialize the program and create a new file.\n" \
                       "-n True   => Initialize the program and enable the deletion of all created empty files.\n" \
                       "-n 1      => Exactly the same result as the previous example."

        case "-ruf":
            name = "Remove Unused Files"
            description = "Enable or disable the deletion of all empty files created at the end of the run.\n" \
                          "Default value: False\n" \
                          "To set to True, you can use a non-zero integer, \"true\" or \"True\".\n" \
                          "To set to False, you can use 0, \"false\" or \"False\"."
            arg = "[ruf:bool]"
            examples = "-ruf True   => Enable deletion of all created empty files.\n" \
                       "-ruf 1      => Exactly the same result as the previous example.\n" \
                       "-ruf 0      => Disable deletion of all created empty files."

        case "-s":
            name = "Separator"
            description = "Set the separator used to save the data in the save file.\nDefault value: \";\""
            arg = "[separator:str]"
            examples = "-s -   => Use the '-' character instead of ';' to separate data."

        case "-dc":
            name = "Decimal Character"
            description = "Set the decimal character used to save the numeric data in the save file.\nDefault value: \".\""
            arg = "[character:str]"
            examples = "-dc  ,   => The float written in the backup file contains the decimal character ','."

        case "-mv":
            name = "Max Values"
            description = "Set the maximum number of data displayed on all lines.\nMax values must be greater than 0 or None."
            arg = "[max_values:int]"
            examples = "-mv 50   => Display a maximum of 50 points per graph."

        case "-aa":
            name = "Add Axis"
            description = "Add a new axis.\nPosition is defined by a tree-digit number corresponding at row (>= 1), " \
                          "column (>= 1) and place (1 <= place <= row * column).\n" \
                          "The title and the labels can be set optionally."
            arg = "[rcp:int] [title*:str] [xlabel*:str] [ylabel*:str]"
            examples = "-aa 111                                  => Add an axis with position: row: 1 ; column: 1 ; Place: 1.\n" \
                       "-aa 212 new_axis time_(s) position_(m)   => Add an axis with position: row: 2 ; column: 1 ; Place: 2, with title 'new axis', and labels 'time (s)' and 'position (m).'"

        case "-aas":
            name = "Add Axes"
            description = "Add new several axes.\nSet the grid by row (>= 1) and column (>= 1)."
            arg = "[row:int] [column:int]"
            examples = "-aas 2 2   => Adds 4 axes arranged in 2 rows and 2 columns"

        case "-at":
            name = "Axis Title"
            description = "Set the title of an axis.\n" \
                          "Select an axis by its position (>= 1).\n" \
                          "If the title contains spaces, replace them with _: my title => my_title."
            arg = "[axis:int] [title:str]"
            examples = "-at 1 new_title_!   => Set the title of axis 1 as 'new title !'."

        case "-albl":
            name = "Axis Label"
            description = "Set the xlabel and the ylabel of an axis.\n" \
                          "Select an axis by its position (>= 1).\n" \
                          "If a label contains spaces, replace them with _: my label => my_label."
            arg = "[axis:int] [xlabel:str] [ylabel:str]"
            examples = "-albl 1 my_x_label my_y_label   => Set the labels of axis 1 as 'my x label' and 'my y label'."

        case "-sa":
            name = "Synchronize Axes"
            description = "Allow to synchronize the dimension of the abscissa of all specified axes with respect to a reference axis.\n" \
                          "Set the synchronization time (in seconds) to loop.\n" \
                          "Set it to 0 to do it only once.\n" \
                          "Set it to -1 to stop the loop.\n" \
                          "Axes to synchronize must be different than the reference axis.\n" \
                          "If no axis is specified, all axes will be synchronized to the reference axis.\n" \
                          "No limit."
            arg = "[time:float] [ori_axis:int] [synchronize_axis_1*:int] [synchronize_axis_2*:int] ..."
            examples = "-sa 0 1 2 3   => Axes 2 and 3 are synchronized on axis 1, only once.\n" \
                       "-sa 1 1 2 3   => Axes 2 and 3 are synchronized on axis 1, every 1 second.\n" \
                       "-sa 2.5 1     => All existing axes are selected to be synchronized on axis 1, every 2.5 seconds.\n" \
                       "You can start many synchronizations:\n-sa 2 1 2\n-sa 3 3 4\n" \
                       "=> Axis 2 is synchronized with axis 1, every 2 seconds, while axis 4 is synchronized with axis 3, every 3 seconds.\n" \
                       "-sa -1 1      => Stop the synchronization with axis 1. Other synchronizations on other axes are not affected.\n" \
                       "-sa -1 1 2    => Stop the synchronization with axis 1, only for axis 2."

        case "-clra":
            name = "Clear Axis"
            description = "Remove all lines of an axis."
            arg = "[axis:int]"
            examples = "-clra 1   => Clear the first axis."

        case "-ra":
            name = "Remove Axis"
            description = "Remove an axis."
            arg = "[axis:int]"
            examples = "-ra 1   => Remove the first axis."

        case "-al":
            name = "Add Line"
            description = "Add a new line to an axis. Select an axis by its position (>= 1).\n" \
                          "Line's color can be set optionally. Color can be a color's name \"red\" or a hexadecimal code \"#FF0000\".\n" \
                          "If no color is specified, it is automatically chosen from the following list:\n" \
                          "Hex. code ~ Approximate rendering\n" \
                          "#E24A33   ~ red\n" \
                          "#348ABD   ~ blue\n" \
                          "#988ED5   ~ purple\n" \
                          "#777777   ~ gray\n" \
                          "#FBC15E   ~ orange\n" \
                          "#8EBA42   ~ green\n" \
                          "#FFB5B8   ~ pink\n" \
                          "When all the colors are taken, the next new line will be the first color, and so on..."

            arg = "[axis:int] [color*:str]"
            examples = "-al 1           => Add a new line in the axis 1.\n" \
                       "-al 1 #78EAFC   => Add a new line in the axis 1, with a specific color."

        case "-cl":
            name = "Color Line"
            description = "Set the line's color.\n" \
                          "Select a line (>= 1) in an axis (>= 1).\n" \
                          "Color can be a color's name \"red\" or a hexadecimal code \"#FF0000\"."
            arg = "[axis:int] [line:int] [color:str]"
            examples = "-cl 1 2 #78EAFC   => Set the color of line 1 in axis 1."

        case "-ml":
            name = "Marker Line"
            description = "Set the line's marker.\n" \
                          "Select a line (>= 1) in an axis (>= 1).\n" \
                          "Default value: \"-o\"\n" \
                          "If you want to remove the marker, use \"None\"." \
                          "See this to know more about marker: https://matplotlib.org/stable/api/markers_api.html"
            arg = "[axis:int] [line:int] [marker:str]"
            examples = "-ml 1 1 None   => Remove the marker of line 1 in axis 1.\n" \
                       "-ml 1 2 *      => The marker of line 2 in axis 1 will be a star."

        case "-clrl":
            name = "Clear Line"
            description = "Remove all points of an line."
            arg = "[axis:int] [line:int]"
            examples = "-clrl 1 1  => Clear the first axis of the first axis."

        case "-rl":
            name = "Remove Line"
            description = "Remove a line."
            arg = "[axis:int] [line:int]"
            examples = "-rl 1 1  => Remove the first line of the first axis."

        case "-h":
            name = "Header"
            description = "Write the headers to the save file on one line.\n" \
                          "If the save file is deleted during use, a new file is created and the headers written are the last headers sent.\n" \
                          "The character used to separate each header is defined by the command Seperator (-s).\n" \
                          "If a header contains spaces, replace them with _: my header => my_header.\n" \
                          "No limit."
            arg = "[header1] [header2] [header3]  ... "
            examples = "-h Time_(s) Position_(m) Speed_(m/s)  => Write \"Time (s);Position (m);Speed (m/s)\" in the save file (if the separator is ';')."

        case "-w":
            name = "Write"
            description = "Write the data to the save file on one line.\n" \
                          "The character used to separate each data is defined by the command Seperator (-s).\n" \
                          "If a data contains spaces, replace them with _: my data => my_data.\n" \
                          "No limit."
            arg = "[data1] [data2] [data3]  ... "
            examples = "-w 0 2 4  => Write \"0;2;4\" in the save file (if the separator is ';')."

        case "-ws":
            name = "Write Several"
            description = "Write the data to the save file on many lines.\n" \
                          "The character used to indicate a new line is \";\".\n" \
                          "It is not required that all lines have the same amount of data.\n" \
                          "The character used to separate each data is defined by the command Seperator (-s).\n" \
                          "If a data contains spaces, replace them with _: my data => my_data.\n" \
                          "No limit."
            arg = "[data11] [data12] [data13] ; [data21] [data22] [data23] ; [data31] [data32] ; ... "
            examples = "-ws 0 2 4 ; 1 3 6.5   => Write two lines \"0;2;4\" and \"1;3;6.5\" in the save file (if the separator is ';' and the decimal character is '.')."

        case "-l":
            name = "Line"
            description = "Add values to a line.\n" \
                          "Select a line (>= 1) in an axis (>= 1).\n" \
                          "Each data pair is composed by an xdata and an ydata.\n" \
                          "The character used to indicate a new pair of data is \";\" or a simple space \" \".\n" \
                          "No limit."
            arg = "[axis:int] [line:int] [xdata1:float] [ydata1:float] ; [xdata2:float] [ydata2:float] ; [xdata3:float] [ydata3:float] ; ..."
            examples = "-l 2 1 0 2 1 2.5 2 3     => Add values (0, 2), (1, 2.5) and (2, 3) to line 1 in axis 2.\n" \
                       "-l 2 1 0 2 ; 1 2.5 ; 2 3 => Exactly the same result as the previous example, but using ';' to separate data."

        case "-lw":
            name = "Line and Write"
            description = "Add value to a line and write it to the save file.\n" \
                          "Select a line (>= 1) in an axis (>= 1).\n" \
                          "The data is composed by an xdata and an ydata."
            arg = "[axis:int] [line:int] [xdata:float] [ydata:float]"
            examples = "-lw 1 1 2 5   => Write in the file \"2;5\" and add the value (2, 5) to line 1 in axis 1."

        case "-lws":
            name = "Line and Write Several"
            description = "Add values to a line and write them to the save file.\n" \
                          "Select a line (>= 1) in an axis (>= 1).\n" \
                          "Each data pair is composed by an xdata and an ydata.\n" \
                          "The character used to indicate a new pair of data is \";\".\n" \
                          "No limit."
            arg = "[axis:int] [line:int] [xdata1:float] [ydata1:float] ; [xdata2:float] [ydata2:float] ; [xdata3:float] [ydata3:float] ; ..."
            examples = "-lws 1 1 0 0 ; 1 2   => Write two lines\"0;0\" and \"1;2\" (if the separator is ';') and add values (0, 0) and (1, 2) to the line 1 in axis 1."

        case "-ld":
            name = "Line Derivation"
            description = "Add all missing derivative values from the \"oriLine\" to the \"derivedLine\"" \
                          "to have the same number of points. It will deduce all the xdata and ydata to add.\n" \
                          "The degree can be set optionnaly. Default value: 1.\n" \
                          "Degree must be greater or equal to 0. 0 return the original value.\n"
            arg = "[oriAxis:int] [oriLine:int] [derivedAxis:int] [derivedLine:int] [degree*:int]"
            examples = "-ld 1 1 2 1     => Take the line 1 in axis 1, and add its derivation in line 1 in axis 2. Variation degree is automatically set to 1.\n" \
                       "-ld 1 1 2 1 1   => Exactly the same result as the previous example.\n" \
                       "-ld 1 1 1 3 2   => Add the derived line in the same axis, in line 3. The derivative's degree is 2."

        case _:
            name = None
            description = None
            arg = None
            examples = None

    return command, name, description, arg, examples


def validation(data_read: str):
    """
    Check if a command is valid.
    :return: None, [data] or err_message, None<br />A string corresponding to an error message if the data read is not valid, and an array with data already sorted.
    """
    data = data_read.split()
    err = None
    if len(data) == 0:
        return err, data

    match data[0]:
        case "-n":
            if not (len(data) == 1 or (len(data) == 2 and parse_bool(data, [1]))):
                err = build_error(data[0], data_read)

        case "-ruf":
            if not (len(data) == 2 and parse_bool(data, [1])):
                err = build_error(data[0], data_read)

        case "-s":
            if len(data) == 2:
                replace_underscore_by_space(data)
            else:
                err = build_error(data[0], data_read)

        case "-dc":
            if len(data) == 2:
                replace_underscore_by_space(data)
            else:
                err = build_error(data[0], data_read)

        case "-mv":
            if len(data) == 2 and ((parse_int(data, [1]) and data[1] >= 1) or data[1] == "None"):
                if data[1] == "None":
                    data[1] = None
            else:
                err = build_error(data[0], data_read)

        case "-aa":
            if len(data) in range(2, 6) and parse_int(data, [1]) and data[1] >= 111:
                replace_underscore_by_space(data, [1])
            else:
                err = build_error(data[0], data_read)

        case "-aas":
            if not (len(data) == 3 and parse_int(data, [1, 2]) and data[1] >= 1 and data[2] >= 1):
                err = build_error(data[0], data_read)

        case "-at":
            if len(data) == 3 and parse_int(data, [1]) and data[1] >= 1:
                replace_underscore_by_space(data, [1])
            else:
                err = build_error(data[0], data_read)

        case "-albl":
            if len(data) == 4 and parse_int(data, [1]) and data[1] >= 1:
                replace_underscore_by_space(data, [1])
            else:
                err = build_error(data[0], data_read)

        case "-sa":
            if not (len(data) >= 3 and parse_float(data, [1]) and parse_int(data, range(2, len(data))) and data[2] >= 1):
                err = build_error(data[0], data_read)
                return err, data

            if data[1] < 0 and data[1] != -1.0:
                err = build_error(data[0], data_read)
                return err, data
            axes = []
            for i in range(3, len(data)):
                if data[i] < 1 or data[i] == data[2]:
                    err = build_error(data[0], data_read)
                    return err, data
                else:
                    axes.append(data[i])

            data = [data[0], data[1], data[2], axes]

        case "-clra":
            if not (len(data) == 2 and parse_int(data, [1]) and data[1] >= 1):
                err = build_error(data[0], data_read)

        case "-ra":
            if not (len(data) == 2 and parse_int(data, [1]) and data[1] >= 1):
                err = build_error(data[0], data_read)

        case "-al":
            if not (len(data) in [2, 3] and parse_int(data, [1]) and data[1] >= 1):
                err = build_error(data[0], data_read)

        case "-cl":
            if not (len(data) == 4 and parse_int(data, [1, 2]) and data[1] >= 1 and data[2] >= 1):
                err = build_error(data[0], data_read)

        case "-ml":
            if not (len(data) == 4 and parse_int(data, [1, 2]) and data[1] >= 1 and data[2] >= 1):
                err = build_error(data[0], data_read)

        case "-clrl":
            if not (len(data) == 3 and parse_int(data, [1, 2]) and data[1] >= 1 and data[2] >= 1):
                err = build_error(data[0], data_read)

        case "-rl":
            if not (len(data) == 3 and parse_int(data, [1, 2]) and data[1] >= 1 and data[2] >= 1):
                err = build_error(data[0], data_read)

        case "-h":
            if len(data) >= 2:
                replace_underscore_by_space(data)
            else:
                err = build_error(data[0], data_read)

        case "-w":
            if len(data) >= 2:
                replace_underscore_by_space(data)
            else:
                err = build_error(data[0], data_read)

        case "-ws":
            length = len(data)
            if not (length >= 2):
                err = build_error(data[0], data_read)
            else:
                lines = []
                line = []
                for i in range(1, length):
                    if data[i] == ";":
                        if len(line) > 0:
                            replace_underscore_by_space(line, skip_0=False)
                            lines.append(line)
                            line = []
                        continue
                    line.append(data[i])
                if len(line) > 0:
                    replace_underscore_by_space(line, skip_0=False)
                    lines.append(line)
                data = [data[0], lines]

        case "-l":
            while ";" in data:
                data.remove(";")

            length = len(data)
            if not (length >= 3 and (length - 3) % 2 == 0 and parse_int(data, [1, 2]) and data[1] >= 1 and data[2] >= 1 and parse_float(data, range(3, length))):
                err = build_error(data[0], data_read)

        case "-lw":
            if not (len(data) == 5 and parse_int(data, [1, 2]) and parse_float(data, [3, 4]) and data[1] >= 1 and data[2] >= 1):
                err = build_error(data[0], data_read)

        case "-lws":
            length = len(data)
            if not (length >= 3 and parse_int(data, [1, 2]) and data[1] >= 1 and data[2] >= 1):
                err = build_error(data[0], data_read)
            else:
                lines = []
                line = []
                for i in range(3, length):
                    if data[i] == ";":
                        if len(line) > 0:
                            valid = parse_float(line) and len(line) == 2
                            if not valid:
                                err = build_error(data[0], data_read)
                                return err, data
                            lines.append(line)
                            line = []
                        continue
                    line.append(data[i])

                if len(line) != 0:
                    valid = parse_float(line) and len(line) == 2
                    if not valid:
                        err = build_error(data[0], data_read)
                        return err, data
                    lines.append(line)

                data = [data[0], data[1], data[2], lines]

        case "-ld":
            length = len(data)
            if length == 5:
                if not (parse_int(data, range(1, 5)) and data[1] >= 1 and data[2] >= 1 and data[3] >= 1 and data[4] >= 1):
                    err = build_error(data[0], data_read)
            elif length == 6:
                if not (parse_int(data, range(1, 6)) and data[1] >= 1 and data[2] >= 1 and data[3] >= 1 and data[4] >= 1 and data[5] >= 0):
                    err = build_error(data[0], data_read)
            else:
                err = build_error(data[0], data_read)

        case _:
            err = f"Command not found: {data[0]}\nTo get the available commands, use: command_helper.py -l"

    return err, data


def replace_underscore_by_space(data: [], index_to_skip=None, skip_0=True):
    """
    Replace all underscore by a simple space
    :param data: Array of string.
    :param index_to_skip: Array of int.
    :param skip_0: Skip the first element
    """
    if index_to_skip is None:
        index_to_skip = []
    if skip_0:
        index_to_skip.append(0)

    for i in range(len(data)):
        if i in index_to_skip:
            continue
        data[i] = data[i].replace("_", " ")


def parse_bool(data: [], index=None):
    """
    Try to parse values to boolean.
    :param data: Data to source.
    :param index: Index to parse. If None, check all the data.
    :return: True if all is parsed, else False.
    """
    if index is None:
        index = range(0, len(data))

    for i in index:
        try:
            data[i] = bool(int(data[i]))
        except ValueError:
            if data[i] in ["true", "True", "false", "False"]:
                data[i] = True if data[i] in ["true", "True"] else False
            else:
                return False
    return True


def parse_int(data: [], index=None):
    """
    Try to parse values to integer.
    :param data: Data to source.
    :param index: Index to parse. If None, check all the data.
    :return: True if all is parsed, else False.
    """
    if index is None:
        index = range(0, len(data))

    for i in index:
        try:
            data[i] = int(data[i])
        except ValueError:
            return False
    return True


def parse_float(data: [], index=None):
    """
    Try to parse values to float.
    :param data: Data to source.
    :param index: Index to parse. If None, check all the data.
    :return: True if all is parsed, else False.
    """
    if index is None:
        index = range(0, len(data))

    for i in index:
        try:
            data[i] = float(data[i])
        except ValueError:
            return False
    return True


def build_error(command: str, data_read: str):
    """
    Build the validation error message
    :param command: The command tested
    :param data_read: The string received
    :return: An error message
    """
    details = get_command_details(command)
    return f"Usage: {details[0]} {details[3]}\nGiven: {data_read}\nTo get more details, use: python command_helper.py -d {details[0][1:]}"


def build_details_str(details, char):
    """
    :param details: The details of a command
    :param char: Used to start an information
    :return: A string containing details of a command
    """
    return f"\n{char}Name: {details[1]}\n{char}Description:\n{details[2]}\n{char}Usage: {details[0]} {details[3]}\n{char}Examples:\n{details[4]}\n"


def main():
    """Main function"""

    if args.list:
        commands = get_command_list()
        for command in commands:
            details = get_command_details(command)
            print(f"{details[0]}\t{details[3]}")

    elif args.details:
        details = get_command_details(f"-{args.details}")
        if details[1] is None:
            print("Command not found!\nUse -l to get the list of available commands.")
        else:
            print(build_details_str(details, '\U0001F784 '))

    elif args.extract:
        file_path = os.path.join(os.getcwd(), args.extract)
        commands = get_command_list()

        if args.full:
            with open(file_path, "w") as file:
                for cmd in commands:
                    details = get_command_details(cmd)
                    file.write(build_details_str(details, "- "))
        else:
            col_format = "{:<10}{:}\n"

            cmd_list = []
            arg_list = []
            for cmd in commands:
                details = get_command_details(cmd)
                cmd_list.append(details[0])
                arg_list.append(details[3])

            with open(file_path, "w") as file:
                for x in zip(cmd_list, arg_list):
                    file.write(col_format.format(*x))

        print(f"File created: {file_path}")
    print()


if __name__ == '__main__':
    main()
