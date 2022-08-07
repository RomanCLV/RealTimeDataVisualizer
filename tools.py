# -*- coding: utf-8 -*-

"""
Module tools

Copyright © 2022 Roman Clavier

Python describing
"""

import re


def exit_program(code=0):
    input("Press enter to exit...")
    exit(code)


def is_int(text: str):
    """Check if text matches with an int"""
    return re.match(r"^[-+]?\d+$", text)


def is_float(text: str):
    """Check if text matches with a float"""
    return re.match(r"[-+]?\d+(\.\d*)?$", text)


def input_choices(message, choices=None):
    """
    Input with specified choices.
    :param message: Input message
    :param choices: Available choices. Can't contain None (but can contain "None"). If no choices specified, default choices are "yes" [y] and "no" [n].
    :return: a choice contained in the choices given | str
    """

    while choices and None in choices:
        choices.remove(None)

    if choices is None:
        choices = ["y", "n"]

    choice = None

    if len(choices) == 0:
        raise ValueError("Choices can't be empty!")

    choices_str = ""
    for index, item in enumerate(choices):
        if type(item) is not str:
            choices[index] = str(item)
        choices_str += f" [{item}]"

    while choice not in choices:
        choice = input(message + choices_str + ": ").lower()
    return choice


def input_validation(message):
    valid = False
    result = None
    while not valid:
        result = input(message)
        valid = input_choices("Confirm") == "y"
    return result
