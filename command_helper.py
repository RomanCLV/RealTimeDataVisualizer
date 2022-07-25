# -*- coding: utf-8 -*-

"""
Command helper module

Copyright © 2022 Roman Clavier

Get the list of available commands, their details, and other actions, using a command parser.
"""

import argparse
import io
import os
import subprocess
import commands

COMMANDS_LIST = {
    "-n": commands.NewCommand(),
    "-ruf": commands.RemoveUnusedFilesCommand(),
    "-s": commands.SeparatorCommand(),
    "-dc": commands.DecimalCharacterCommand(),
    "-mv": commands.MaxValueCommand(),
    "-aa": commands.AddAxisCommand(),
    "-aas": commands.AddAxesCommand(),
    "-at": commands.AxisTitleCommand(),
    "-albl": commands.AxisLabelsCommand(),
    # "-sa": commands.SynchronizeAxesCommand(),
    "-clra": commands.ClearAxisCommand(),
    "-ra": commands.RemoveAxisCommand(),
    "-al": commands.AddLineCommand(),
    "-cl": commands.ColorLineCommand(),
    "-ml": commands.MarkerLineCommand(),
    "-clrl": commands.ClearLineCommand(),
    "-rl": commands.RemoveLineCommand(),
    "-h": commands.HeaderCommand(),
    "-w": commands.WriteCommand(),
    "-ws": commands.WriteSeveralCommand(),
    "-l": commands.LineCommand(),
    "-lw": commands.LineWriteCommand(),
    "-lws": commands.LineWriteSeveralCommand(),
    "-ld": commands.LineDerivationCommand()
}


def get_command_codes(with_dashes=True):
    """
    Get the available command codes
    :param with_dashes: If True, returns ['-n', '-ruf', ...]', else ['n', 'ruf', ...]
    """
    return COMMANDS_LIST.keys() if with_dashes else list(map(lambda x: x[1:], COMMANDS_LIST.keys()))


def get_commands():
    """Get the available commands"""
    return COMMANDS_LIST.values()


def get_command(code: str):
    """
    Get command's details (description and args details).
    :param code: A string corresponding to a command. Example: '-n'
    :return: The corresponding command
    """
    return COMMANDS_LIST[code] if code in get_command_codes() else None


def validation(data_read: str):
    """
    Check if a command is valid.
    :return: None, [data] or err_message, None<br />A string corresponding to an error message if the data read is not valid, and an array with data already sorted.
    """
    data = data_read.split()
    err = None
    if len(data) == 0:
        return err, None
    data_build = None

    if data[0] in get_command_codes():
        data_build = COMMANDS_LIST[data[0]].build_data(data)
        if data_build is None:
            err = commands.build_error(COMMANDS_LIST[data[0]], data_read)
    else:
        err = f"Command not found: {data[0]}\nTo get the available commands, use: command_helper.py -l"
    return err, data_build


def main():
    """Main function"""
    print()

    if args.list:
        col_format = "{:<10}{:}"
        for command in get_commands():
            details_to_print = (command.code, command.arg, "\t| " + command.note)\
                if command.note else (command.code, command.arg)
            print(col_format.format(*details_to_print))

    elif args.details:
        command = get_command(f"-{args.details}")
        if command is None:
            print("Command not found!\nUse -l to get the list of available commands.")
        else:
            print(commands.build_details(command, "* "))  # "\U0001F784 "

    elif args.extract:

        def open_folder(file_created):
            print(f"File created: {file_created.name}")
            choices = ["y", "Y", "n", "N"]
            choice = ""
            while choice not in choices:
                choice = input("Open folder? [y], [Y], [n], [N] : ")
            if choice in ["y", "Y"]:
                subprocess.Popen(rf'explorer /select,{file_created.name}')

        file_path = os.path.join(os.getcwd(), args.extract)
        if args.full:
            with open(file_path, "w") as file:
                for command in get_commands():
                    file.write("\n" + commands.build_details(command, "* ") + "\n")
                    file.write("-" * 100)
                    file.write("\n")
                open_folder(file)

        else:
            col_format = "{:<10}{:}\n"
            code_list = []
            arg_list = []
            for command in get_commands():
                code_list.append(command.code)
                arg_list.append(command.arg)
                if command.note:
                    arg_list[-1] += f" | {command.note}"

            with open(file_path, "w") as file:
                for x in zip(code_list, arg_list):
                    file.write(col_format.format(*x))
                open_folder(file)

    elif args.full:
        print("The \"full\" (-f) option can only be used with the \"extraction\" (-e).\nUsage: command_helper.py -e filename.txt -f")

    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Command helper CLI",
        epilog="note:\n" +
               "The usage of each command is given as follows: -cmd [arg1:type] [arg2:type].\n" +
               "If an argument contains the star (*) character at the end, it indicates that it is additional. Example : -cmd [arg1:type] [arg2*:type]"
    )
    parser.add_argument("-l", "--list", action="store_true", help="get the list of available commands")
    parser.add_argument("-d", "--details", type=str, choices=get_command_codes(False), help="get the details of the given command")
    parser.add_argument("-e", "--extract", type=str, help="extract command details to a file")
    parser.add_argument("-f", "--full", action="store_true", help="full extraction (used with -e)")
    args = parser.parse_args()
    main()
