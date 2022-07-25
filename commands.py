# -*- coding: utf-8 -*-

"""
Commands file

Copyright © 2022 Roman Clavier

Contains all commands classes.
"""

import abc
from abc import ABC

import pyplot_utils


class Command(metaclass=abc.ABCMeta):
    """Command class"""
    def __init__(self,
                 name=None,
                 description=None,
                 code=None,
                 arg=None,
                 examples=None,
                 note=None,
                 arg_info=None):
        self.name = name
        self.description = description
        self.code = code
        self.arg = arg
        self.examples = examples
        self.note = note
        self.arg_info = arg_info

    @abc.abstractmethod
    def build_data(self, data):
        """Return None if the validation has failed, else return a data ready to be used"""
        return None


class NewCommand(Command, ABC):
    """New command class"""
    def __init__(self):
        super().__init__(
            name="New",
            description="Initialize program. Create a new save file. If a graph already exists, it is cleaned up.\n" +
                        "Remove Unused Files can also be set at the same time. See command -ruf.\n" +
                        "About ruf:\nDefault value: False",
            code="-n",
            arg="[ruf*:bool]",
            examples="-n        => Initialize the program and create a new file.\n" +
                     "-n True   => Initialize the program and enable the deletion of all created empty files.\n" +
                     "-n 1      => Exactly the same result as the previous example.",
            note="About ruf:\n" +
                 "To set to True, you can use a non-zero integer, \"true\" or \"True\".\n" +
                 "To set to False, you can use 0, \"false\" or \"False\".",
        )

    def build_data(self, data):
        if len(data) == 1 or (len(data) == 2 and parse_bool(data, [1])):
            return data
        return None


class RemoveUnusedFilesCommand(Command, ABC):
    """Remove unused files command class"""
    def __init__(self):
        super().__init__(
            name="Remove Unused Files",
            description="Enable or disable the deletion of all empty files created at the end of the run.\n" +
                        "Default value: False",
            code="-ruf",
            arg="[ruf:bool]",
            examples="-ruf True   => Enable deletion of all created empty files.\n" +
                     "-ruf 1      => Exactly the same result as the previous example.\n" +
                     "-ruf 0      => Disable deletion of all created empty files.",
            note="To set to True, you can use a non-zero integer, \"true\" or \"True\".\n" +
                 "To set to False, you can use 0, \"false\" or \"False\"."
        )

    def build_data(self, data):
        if len(data) == 2 and parse_bool(data, [1]):
            return data
        return None


class SeparatorCommand(Command, ABC):
    """Separator command class"""
    def __init__(self):
        super().__init__(
            name="Separator",
            description="Set the separator used to save the data in the save file.\n" +
                        "Default value: \";\"",
            code="-s",
            arg="[separator:str]",
            examples="-s -   => Use the '-' character instead of ';' to separate data."
        )

    def build_data(self, data):
        if len(data) == 2:
            replace_underscore_by_space(data)
            return data
        return None


class DecimalCharacterCommand(Command, ABC):
    """Decimal character command class"""
    def __init__(self):
        super().__init__(
            name="Decimal Character",
            description="Set the decimal character used to save the numeric data in the save file.\n" +
                        "Default value: \".\"",
            code="-dc",
            arg="[character:str]",
            examples="-dc ,   => The float written in the save file contains the decimal character ','."
        )

    def build_data(self, data):
        if len(data) == 2:
            replace_underscore_by_space(data)
            return data
        return None


class MaxValueCommand(Command, ABC):
    """Max value command class"""

    def __init__(self):
        super().__init__(
            name="Max Values",
            description="Set the maximum number of data displayed on all lines.",
            code="-mv",
            arg="[max_values:int]",
            examples="-mv 50   => Display a maximum of 50 points per graph.",
            note="Max values must be greater than 0 or None."
        )

    def build_data(self, data):
        if len(data) == 2 and ((parse_int(data, [1]) and data[1] >= 1) or data[1] == "None"):
            if data[1] == "None":
                data[1] = None
            return data
        return None


class AddAxisCommand(Command, ABC):
    """Add axis command class"""
    def __init__(self):
        super().__init__(
            name="Add Axis",
            description="Add a new axis.\n" +
                        "The title and the labels can be set optionally.",
            code="-aa",
            arg="[rcp:int] [title*:str] [xlabel*:str] [ylabel*:str]",
            examples="-aa 111                                  => Add an axis with position: row: 1 ; column: 1 ; Place: 1.\n" +
                     "-aa 211 new_axis                         => Add an axis with position: row: 2 ; column: 1 ; Place: 1, with title 'new axis'.\n" +
                     "-aa 211 new_axis my_label                => Add an axis with position: row: 2 ; column: 1 ; Place: 1, with title 'new axis', and x label 'my label'.\n" +
                     "-aa 212 new_axis time_(s) position_(m)   => Add an axis with position: row: 2 ; column: 1 ; Place: 2, with title 'new axis', and labels 'time (s)' and 'position (m).'",
            note="Position is defined by a tree-digit number corresponding at row (>= 1), " +
                 "column (>= 1) and place (1 <= place <= row * column)."
        )

    def build_data(self, data):
        if len(data) in range(2, 6) and parse_int(data, [1]) and data[1] >= 111:
            replace_underscore_by_space(data, [1])
            return data
        return None


class AddAxesCommand(Command, ABC):
    """Add axes command class"""
    def __init__(self):
        super().__init__(
            name="Add Axes",
            description="Add new several axes.\nSet the grid by row (>= 1) and column (>= 1).\n" +
                        "The number of axes created is equal to row * column.",
            code="-aas",
            arg="[row:int] [column:int]",
            examples="-aas 2 2   => Adds 4 (2 x 2 = 4) axes arranged in 2 rows and 2 columns"
        )

    def build_data(self, data):
        if len(data) == 3 and parse_int(data, [1, 2]) and data[1] >= 1 and data[2] >= 1:
            return data
        return None


class AxisTitleCommand(Command, ABC):
    """Axis title command class"""
    def __init__(self):
        super().__init__(
            name="Axis Title",
            description="Set the title of an axis.",
            code="-at",
            arg="[axis:int] [title:str]",
            examples="-at 1 new_title_!   => Set the title of axis 1 as 'new title !'.",
            note="Select an axis by its position (>= 1).\n" +
                 "If the title contains spaces, replace them with _: my title => my_title."
        )

    def build_data(self, data):
        if len(data) == 3 and parse_int(data, [1]) and data[1] >= 1:
            replace_underscore_by_space(data, [1])
            return data
        return None


class AxisLabelsCommand(Command, ABC):
    """Axis labels command class"""
    def __init__(self):
        super().__init__(
            name="Axis Labels",
            description="Set the xlabel and the ylabel of an axis.",
            code="-albl",
            arg="[axis:int] [xlabel:str] [ylabel:str]",
            examples="-albl 1 my_x_label my_y_label   => Set the labels of axis 1 as 'my x label' and 'my y label'.",
            note="Select an axis by its position (>= 1).\n" +
                 "If a label contains spaces, replace them with _: my label => my_label."
        )

    def build_data(self, data):
        if len(data) == 4 and parse_int(data, [1]) and data[1] >= 1:
            replace_underscore_by_space(data, [1])
            return data
        return None


class SynchronizeAxesCommand(Command, ABC):
    """Synchronize axes command class"""
    def __init__(self):
        super().__init__(
            name="Synchronize Axes",
            description="Allow to synchronize the dimension of the abscissa of all specified axes with respect to a reference axis.\n" +
                        "Set the synchronization time (in seconds) to loop.\n" +
                        "Set it to 0 to do it only once.\n" +
                        "Set it to -1 to stop the loop.\n" +
                        "Axes to synchronize must be different than the reference axis.\n" +
                        "If no axis is specified, all axes will be synchronized to the reference axis.\n" +
                        "No limit.",
            code="-sa",
            arg="[time:float] [ori_axis:int] [synchronize_axis_1*:int] [synchronize_axis_2*:int] ...",
            examples="-sa 0 1 2 3   => Axes 2 and 3 are synchronized on axis 1, only once.\n" +
                     "-sa 1 1 2 3   => Axes 2 and 3 are synchronized on axis 1, every 1 second.\n" +
                     "-sa 2.5 1     => All existing axes are selected to be synchronized on axis 1, every 2.5 seconds.\n" +
                     "You can start many synchronizations:\n-sa 2 1 2\n-sa 3 3 4\n" +
                     "=> Axis 2 is synchronized with axis 1, every 2 seconds, while axis 4 is synchronized with axis 3, every 3 seconds.\n" +
                     "-sa -1 1      => Stop the synchronization with axis 1. Other synchronizations on other axes are not affected.\n" +
                     "-sa -1 1 2    => Stop the synchronization with axis 1, only for axis 2."
        )

    def build_data(self, data):
        if not (len(data) >= 3 and parse_float(data, [1]) and parse_int(data, range(2, len(data))) and data[2] >= 1):
            return None

        if data[1] < 0 and data[1] != -1.0:
            return None

        axes = []
        for i in range(3, len(data)):
            if data[i] < 1 or data[i] == data[2]:
                return None
            else:
                axes.append(data[i])

        return [data[0], data[1], data[2], axes]


class ClearAxisCommand(Command, ABC):
    """Clear axis command class"""
    def __init__(self):
        super().__init__(
            name="Clear Axis",
            description="Remove all lines of an axis.",
            code="-clra",
            arg="[axis:int]",
            examples="-clra 1   => Clear the first axis."
        )

    def build_data(self, data):
        if len(data) == 2 and parse_int(data, [1]) and data[1] >= 1:
            return data
        return None


class RemoveAxisCommand(Command, ABC):
    """Remove axis command class"""
    def __init__(self):
        super().__init__(
            name="Remove Axis",
            description="Remove an axis.",
            code="-ra",
            arg="[axis:int]",
            examples="-ra 1   => Remove the first axis."
        )

    def build_data(self, data):
        if len(data) == 2 and parse_int(data, [1]) and data[1] >= 1:
            return data
        return None


class AddLineCommand(Command, ABC):
    """Add line command class"""
    def __init__(self):
        super().__init__(
            name="Add Line",
            description="Add a new line to an axis. Select an axis by its position (>= 1).\n" +
                        "Line's color can be set optionally. Color can be a color's name \"red\" or a hexadecimal code \"#FF0000\".\n" +
                        "If no color is specified, it is automatically chosen from the following list:\n" +
                        "Hex. code ~ Approximate rendering\n" +
                        "#E24A33   ~ red\n" +
                        "#348ABD   ~ blue\n" +
                        "#988ED5   ~ purple\n" +
                        "#777777   ~ gray\n" +
                        "#FBC15E   ~ orange\n" +
                        "#8EBA42   ~ green\n" +
                        "#FFB5B8   ~ pink\n" +
                        "When all the colors are taken, the next new line will be the first color, and so on...",
            code="-al",
            arg="[axis:int] [color*:str]",
            examples="-al 1           => Add a new line in the axis 1.\n" +
                     "-al 1 #78EAFC   => Add a new line in the axis 1, with a specific color."
        )

    def build_data(self, data):
        if len(data) in [2, 3] and parse_int(data, [1]) and data[1] >= 1:
            return data
        return None


class ColorLineCommand(Command, ABC):
    """Color line command class"""
    def __init__(self):
        super().__init__(
            name="Color Line",
            description="Set the line's color.\n" +
                        "Select a line (>= 1) in an axis (>= 1).\n" +
                        "Color can be a color's name \"red\" or a hexadecimal code \"#FF0000\".",
            code="-cl",
            arg="[axis:int] [line:int] [color:str]",
            examples="-cl 1 2 #78EAFC   => Set the color of line 2 in axis 1."
        )

    def build_data(self, data):
        if len(data) == 4 and parse_int(data, [1, 2]) and data[1] >= 1 and data[2] >= 1:
            return data
        return None


class MarkerLineCommand(Command, ABC):
    """Marker line command class"""
    def __init__(self):
        super().__init__(
            name="Marker Line",
            description="Set the line's marker.\n" +
                        "Select a line (>= 1) in an axis (>= 1).\n" +
                        f"Default value: \"{pyplot_utils.default_marker}\"\n" +
                        "If you want to remove the marker, use \"None\".",
            code="-ml",
            arg="[axis:int] [line:int] [marker:str]",
            examples="-ml 1 1 None   => Remove the marker of line 1 in axis 1.\n" +
                     "-ml 1 2 *      => The marker of line 2 in axis 1 will be a star.",
            note="See this to know more about marker: https://matplotlib.org/stable/api/markers_api.html",
            arg_info="See this to know more about marker: https://matplotlib.org/stable/api/markers_api.html"
        )

    def build_data(self, data):
        if len(data) == 4 and parse_int(data, [1, 2]) and data[1] >= 1 and data[2] >= 1:
            return data
        return None


class StyleLineCommand(Command, ABC):
    """Style line command class"""
    def __init__(self):
        super().__init__(
            name="Style Line",
            description="Set the line's style.\n" +
                        "Select a line (>= 1) in an axis (>= 1).\n" +
                        f"Default value: \"{pyplot_utils.default_style}\"\n" +
                        "If you want to remove the marker, use \"None\".\n" +
                        "Available values:\n" +
                        "==========================================  =================\n" +
                        "linestyle                                   description      \n" +
                        "==========================================  =================\n" +
                        "'-'    or 'solid'                           solid line       \n" +
                        "'--'   or 'dashed'                          dashed line      \n" +
                        "'-.'   or 'dash-dot'                        dash-dotted line \n" +
                        "':'    or 'dotted'                          dotted line      \n" +
                        "'none' or 'None'                            draw nothing     \n" +
                        "==========================================  =================",
            code="-sl",
            arg="[axis:int] [line:int] [style:str]",
            examples="-sl 1 1 None   => Line 1 in axis 1 has no style.\n" +
                     "-sl 1 2 --     => The style of line 2 in axis 1 will be a dashed line."
        )

    def build_data(self, data):
        if len(data) == 4 and parse_int(data, [1, 2]) and data[1] >= 1 and data[2] >= 1:
            return data
        return None


class ClearLineCommand(Command, ABC):
    """Clear line command class"""
    def __init__(self):
        super().__init__(
            name="Clear Line",
            description="Remove all points of an line.",
            code="-clrl",
            arg="[axis:int] [line:int]",
            examples="-clrl 1 1  => Clear the first axis of the first axis."
        )

    def build_data(self, data):
        if len(data) == 3 and parse_int(data, [1, 2]) and data[1] >= 1 and data[2] >= 1:
            return data
        return None


class RemoveLineCommand(Command, ABC):
    """Remove line command class"""
    def __init__(self):
        super().__init__(
            name="Remove Line",
            description="Remove a line.",
            code="-rl",
            arg="[axis:int] [line:int]",
            examples="-rl 1 1  => Remove the first line of the first axis."
        )

    def build_data(self, data):
        if len(data) == 3 and parse_int(data, [1, 2]) and data[1] >= 1 and data[2] >= 1:
            return data
        return None


class HeaderCommand(Command, ABC):
    """Header command class"""
    def __init__(self):
        super().__init__(
            name="Header",
            description="Write the headers to the save file on one line.\n" +
                        "If the save file is deleted during use, a new file is created and the headers written are the last headers sent.",
            code="-h",
            arg="[header1] [header2] [header3]  ... ",
            examples="-h Time_(s) Position_(m) Speed_(m/s)  => Write \"Time (s);Position (m);Speed (m/s)\" in the save file (if the separator is ';').",
            note="The character used to separate each header is defined by the command Seperator (-s). See command -s.\n" +
                 "If a header contains spaces, replace them with _: my header => my_header.\n" +
                 "No limit.",
        )

    def build_data(self, data):
        if len(data) >= 2:
            replace_underscore_by_space(data)
            return data
        return None


class WriteCommand(Command, ABC):
    """Write command class"""
    def __init__(self):
        super().__init__(
            name="Write",
            description="Write the data to the save file on one line.\n" +
                        "If the save file is deleted during use, a new file is created and the headers written are the last headers sent. See command -h.",
            code="-w",
            arg="[data1] [data2] [data3]  ... ",
            examples="-w 0 2 4  => Write \"0;2;4\" in the save file (if the separator is ';').",
            note="The character used to separate each data is defined by the command Seperator (-s). See command -s.\n" +
                 "If a data contains spaces, replace them with _: my data => my_data.\n" +
                 "No limit."
        )

    def build_data(self, data):
        if len(data) >= 2:
            replace_underscore_by_space(data)
            return data
        return None


class WriteSeveralCommand(Command, ABC):
    """Write several command class"""
    def __init__(self):
        super().__init__(
            name="Write Several",
            description="Write the data to the save file on many lines.\n" +
                        "The character used to indicate a new line is \";\".\n" +
                        "It is not required that all lines have the same amount of data.",
            code="-ws",
            arg="[data11] [data12] [data13] ; [data21] [data22] [data23] ; [data31] [data32] ; ... ",
            examples="-ws 0 2 4 ; 1 3 6.5   => Write two lines \"0;2;4\" and \"1;3;6.5\" in the save file (if the separator is ';' and the decimal character is '.').",
            note="The character used to separate each data is defined by the command Seperator (-s). See command -s.\n" +
                 "If a data contains spaces, replace them with _: my data => my_data.\n" +
                 "No limit."
        )

    def build_data(self, data):
        length = len(data)
        if length <= 2:
            return None
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
            return [data[0], lines]


class LineCommand(Command, ABC):
    """Line command class"""
    def __init__(self):
        super().__init__(
            name="Line",
            description="Add values to a line.\n" +
                        "Select a line (>= 1) in an axis (>= 1).\n" +
                        "Each data pair is composed by an xdata and an ydata.",
            code="-l",
            arg="[axis:int] [line:int] [xdata1:float] [ydata1:float] ; [xdata2:float] [ydata2:float] ; [xdata3:float] [ydata3:float] ; ...",
            examples="-l 2 1 0 2 1 2.5 2 3     => Add values (0, 2), (1, 2.5) and (2, 3) to line 1 in axis 2.\n" +
                     "-l 2 1 0 2 ; 1 2.5 ; 2 3 => Exactly the same result as the previous example, but using ';' to separate data.",
            note="The character used to indicate a new pair of data is \";\" or a simple space \" \".\n" +
                 "No limit.",
            arg_info="The character used to indicate a new pair of data is \";\" or a simple space \" \"."
        )

    def build_data(self, data):
        while ";" in data:
            data.remove(";")
        length = len(data)
        if length >= 3 and length % 2 == 1 and parse_int(data, [1, 2]) and data[1] >= 1 and data[
            2] >= 1 and parse_float(data, range(3, length)):
            return data
        return None


class LineWriteCommand(Command, ABC):
    """Line Write command class"""
    def __init__(self):
        super().__init__(
            name="Line and Write",
            description="Add value to a line and write it to the save file.\n" +
                        "Select a line (>= 1) in an axis (>= 1).\n" +
                        "The data is composed by an xdata and an ydata.",
            code="-lw",
            arg="[axis:int] [line:int] [xdata:float] [ydata:float]",
            examples="-lw 1 1 2 5   => Write in the file \"2;5\" and add the value (2, 5) to line 1 in axis 1."
        )

    def build_data(self, data):
        if len(data) == 5 and parse_int(data, [1, 2]) and parse_float(data, [3, 4]) and data[1] >= 1 and data[2] >= 1:
            return data
        return None


class LineWriteSeveralCommand(Command, ABC):
    """Line Write several command class"""
    def __init__(self):
        super().__init__(
            name="Line and Write Several",
            description="Add values to a line and write them to the save file.\n" +
                        "Select a line (>= 1) in an axis (>= 1).\n" +
                        "Each data pair is composed by an xdata and an ydata.",
            code="-lws",
            arg="[axis:int] [line:int] [xdata1:float] [ydata1:float] ; [xdata2:float] [ydata2:float] ; [xdata3:float] [ydata3:float] ; ...",
            examples="-lws 1 1 0 0 ; 1 2   => Write two lines\"0;0\" and \"1;2\" (if the separator is ';') and add values (0, 0) and (1, 2) to the line 1 in axis 1.",
            note="The character used to indicate a new pair of data is \";\".\n" +
                 "No limit."
        )

    def build_data(self, data):
        length = len(data)
        if not (length >= 3 and parse_int(data, [1, 2]) and data[1] >= 1 and data[2] >= 1):
            return None
        else:
            lines = []
            line = []
            for i in range(3, length):
                if data[i] == ";":
                    if len(line) > 0:
                        valid = parse_float(line) and len(line) == 2
                        if not valid:
                            return None
                        lines.append(line)
                        line = []
                    continue
                line.append(data[i])

            if len(line) != 0:
                valid = parse_float(line) and len(line) == 2
                if not valid:
                    return None
                lines.append(line)

            return [data[0], data[1], data[2], lines]


class LineDerivationCommand(Command, ABC):
    """Line derivation command class"""
    def __init__(self):
        super().__init__(
            name="Line Derivation",
            description="Add all missing derivative values from the \"oriLine\" to the \"derivedLine\"" +
                        "to have the same number of points. It will deduce all the xdata and ydata to add.\n" +
                        "The degree can be set optionnaly. Default value: 1.\n" +
                        "Degree must be greater or equal to 0. 0 return the original value.\n",
            code="-ld",
            arg="[oriAxis:int] [oriLine:int] [derivedAxis:int] [derivedLine:int] [degree*:int]",
            examples="-ld 1 1 2 1     => Take the line 1 in axis 1, and add its derivation in line 1 in axis 2. Variation degree is automatically set to 1.\n" +
                     "-ld 1 1 2 1 1   => Exactly the same result as the previous example.\n" +
                     "-ld 1 1 1 3 2   => Add the derived line in the same axis, in line 3. The derivative's degree is 2."
        )

    def build_data(self, data):
        length = len(data)
        if length == 5:
            if not (parse_int(data, range(1, 5)) and data[1] >= 1 and data[2] >= 1 and data[3] >= 1 and data[4] >= 1):
                return None
        elif length == 6:
            if not (parse_int(data, range(1, 6)) and data[1] >= 1 and data[2] >= 1 and data[3] >= 1 and data[4] >= 1 and
                    data[5] >= 0):
                return None
        else:
            return None
        return data


def build_error(command, data_read: str):
    """
    Build the validation error message
    :param command: The command tested
    :param data_read: The string received
    :return: An error message
    """
    return f"Usage: {command.code} {command.arg}\n" \
           f"Given: {data_read}\n" \
           f"To get more details, use: python command_helper.py -d {command.code[1:]}"


def build_details(command, char: str):
    """
    :param command: The command used
    :param char: Used to start an information
    :return: A string containing details of a command
    """
    note = f"\n{char}Note:\n{command.note}" if command.note else ""
    return f"{char}Name: {command.name}\n" \
           f"{char}Description:\n{command.description}\n" \
           f"{char}Usage: {command.code} {command.arg}\n" \
           f"{char}Examples:\n{command.examples}" + \
           note


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
