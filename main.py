# -*- coding: utf-8 -*-

"""
Main module

Copyright © 2021 Roman Clavier

Python describing
"""

from datetime import datetime
import time
import re
import serial
import os
import signal

import pyplot_utils
import pyplot_utils as utils
import command_helper as helper

global run

global base_path
global file_path
global created_files
global remove_unused_files
global update_title_requested
global separator
global decimal_character

global serialport
global is_connected
global last_header
global all_headers

global fig
global max_values
global axes_synchronizers


def main():
    """The main function"""
    global run
    global base_path
    global file_path
    global created_files
    global remove_unused_files
    global update_title_requested
    global separator
    global decimal_character

    global is_connected
    global last_header
    global all_headers
    global fig
    global max_values
    global axes_synchronizers

    run = True
    base_path = os.path.join(os.getcwd(), "data")
    file_path = ""
    created_files = []
    remove_unused_files = False
    update_title_requested = False
    separator = ";"
    decimal_character = "."
    is_connected = False
    last_header = []
    all_headers = []
    fig = None
    max_values = None
    axes_synchronizers = []

    while run:
        if not is_connected:
            connect()
        else:
            read()
        if fig is not None:
            utils.refresh_plot(0.01)

    if remove_unused_files:
        for filepath in created_files:
            if os.path.getsize(filepath) == 0:
                os.remove(filepath)
            else:
                with open(filepath, "r") as file:
                    content = file.readlines()
                if len(content) == 1 and content[0] in all_headers:
                    os.remove(filepath)


def on_close(event):
    """On close event"""
    global run
    run = False


def sigint_handler(signal, frame):
    """Catch KeyboardInterrupt"""
    global run
    run = False


def connect(com_name="COM3", baudrate=9600, timeout=0.01):
    """
    Try to connect with the arduino
    :param com_name: Name of communication port
    :param baudrate: Communication's frequence
    :param timeout: Timer before continue
    :return: void
    """
    global is_connected
    global serialport

    try:
        serialport = serial.Serial(com_name, baudrate=baudrate, timeout=timeout)
        is_connected = True
        print(f"Connection success to: {com_name} at baudrate: {baudrate}")
    except serial.SerialException:
        is_connected = False
        print(f"Connection failed to: {com_name}")
        time.sleep(1)


def read():
    """
    Read data from Arduino card
    """
    global serialport
    global is_connected
    global file_path
    global remove_unused_files
    global update_title_requested
    global separator
    global decimal_character

    global last_header
    global fig
    global max_values
    global axes_synchronizers

    try:
        data_read = serialport.readline()
    except serial.SerialException:
        is_connected = False
        log("Cannot read data")
        return

    for axes_synchronizer in axes_synchronizers:
        axes_synchronizer.try_synchronize()

    if not data_read:
        return

    data_decoded = data_read.decode("ascii").strip()
    if len(data_decoded) == 0:
        return

    if data_decoded[0] == "-":
        err, data = helper.validation(data_decoded)
        if not file_path and data[0] != "-n":
            print("Not initialized")
            return
    else:
        log(data_decoded)
        return

    if err:
        print(f"Error:\n{err}\n")
        return

    if len(data) == 0:
        return

    match data[0]:
        case "-n":
            if len(data) == 2:
                remove_unused_files = data[1]

            utils.init_plot()

            if fig is not None:
                utils.clear_fig(fig)
            create_file()

        case "-ruf":
            remove_unused_files = data[1]

        case "-s":
            separator = data[1]

        case "-dc":
            decimal_character = data[1]

        case "-mv":
            max_values = data[1]

        case "-aa":
            if fig is None:
                fig = utils.create_plot(window_title="Real time data visualizer", fig_title=file_path, close_event=on_close)
            title = data[2] if len(data) >= 3 else None
            xlabel = data[3] if len(data) >= 4 else None
            ylabel = data[4] if len(data) >= 5 else None
            utils.add_axis(fig, data[1], title, xlabel, ylabel)

        case "-aas":
            add_multi_axis(data[1], data[2])

        case "-at":
            utils.set_axis_title(get_axis(fig, data[1]), data[2])

        case "-albl":
            utils.set_axis_label(get_axis(fig, data[1]), data[2], data[3])

        case "-sa":
            ori_axis = get_axis(fig, data[2])
            if data[1] == -1:
                remove_synchronizer_on(ori_axis)
            else:
                axes_index = data[3] if len(data[3]) != 0 else list(range(1, len(fig.axes) + 1)).remove(data[2])
                axes = []
                for i in axes_index:
                    axes.append(get_axis(fig, i))
                pass
                if data[1] == 0:
                    pyplot_utils.synchronize_axes(ori_axis, axes)
                else:
                    axes_synchronizers.append(AxesSynchronizer(data[1], ori_axis, axes))

        case "-clra":
            utils.clear_axis(get_axis(fig, data[1]))

        case "-ra":
            axis = get_axis(fig, data[1])
            remove_synchronizer_on(axis)
            utils.remove_axis(axis)

        case "-al":
            line = utils.add_line(get_axis(fig, data[1]))
            if len(data) > 2:
                utils.set_color(line, data[2])

        case "-cl":
            utils.set_color(get_line(fig, data[1], data[2]), data[3])

        case "-ml":
            utils.set_marker(get_line(fig, data[1], data[2]), data[3])

        case "-clrl":
            utils.clear_line(get_line(fig, data[1], data[2]))

        case "-rl":
            utils.remove_line(get_line(fig, data[1], data[2]))

        case "-h":
            write_header(data[1:])

        case "-w":
            write_data(data[1:])

        case "-ws":
            write_datas(data[1])

        case "-l":
            x, y = [[float(x) for (i, x) in enumerate(data[3:]) if i % 2 == 0],
                    [float(y) for (i, y) in enumerate(data[3:]) if i % 2 != 0]]
            utils.add_values(get_line(fig, data[1], data[2]), x, y, max_values)

        case "-lw":
            write_data([str(data[3]), str(data[4])])
            utils.add_values(get_line(fig, data[1], data[2]), data[3], data[4], max_values)

        case "-lws":
            write_datas(list(map(lambda dt: [str(dt[0]), str(dt[1])], data[3])))
            x, y = [[dt[0] for (i, dt) in enumerate(data[3])],
                    [dt[1] for (i, dt) in enumerate(data[3])]]
            utils.add_values(get_line(fig, data[1], data[2]), x, y, max_values)

        case "-ld":
            derived(get_line(fig, data[3], data[4]),
                    get_line(fig, data[1], data[2]),
                    data[5] if len(data) == 6 else 1)

        case _:
            log(f"Unknow {data_decoded}")

    if update_title_requested and fig is not None:
        utils.set_title(fig, file_path)
        update_title_requested = False


def read_validation_error(cmd: str, message: str, data_err: str):
    """Print a message to indicate an error occured"""
    log(f"Validation error:\n  Command: {cmd}\n  Message: {message}\n  Given: {data_err}")


def get_axis(figure, axis_index: int):
    """Get an axis"""
    return figure.axes[get_index(axis_index)]


def get_line(figure, axis_index: int, line_index: int):
    """Get a line"""
    return get_axis(figure, axis_index).lines[get_index(line_index)]


def get_index(data):
    """Get index"""
    return int(data) - 1


def create_file():
    """
    Create a new file
    :return: void
    """
    global file_path
    global created_files
    global update_title_requested

    now = datetime.now()
    dt_string = now.strftime("%Y_%d_%m-%H_%M_%S")
    file_path = os.path.join(base_path, f"{dt_string}.txt")

    if not os.path.exists(base_path):
        os.mkdir(base_path)

    if not os.path.exists(file_path):
        with open(file_path, "x") as file:
            created_files.append(file.name)
            log(f"New file: {file.name}")
    else:
        log("File's already existing")
    update_title_requested = True


def add_multi_axis(row: int, column: int):
    """Set axis format"""
    global fig
    fig = utils.add_multi_axis(row, column)
    utils.set_close_event(fig, on_close)
    utils.set_window_title(fig, "Real time data visualizer")
    utils.set_title(fig, file_path)


def remove_synchronizer_on(ori_axis):
    """Remove all the synchronizers having this reference axis."""
    global axes_synchronizers
    i = 0
    while i < len(axes_synchronizers):
        if axes_synchronizers[i].get_ori_axis() == ori_axis:
            axes_synchronizers.remove(axes_synchronizers[i])
            i -= 1
        i += 1


def write_header(header=None):
    """
    Save the header given
    :param header: array of string
    :return: void
    """
    global file_path
    global last_header
    global all_headers

    if header is None:
        header = []

    if not os.path.exists(file_path):
        create_file()

    if len(header) > 0:
        last_header = header
        all_headers.append(separator.join(header) + "\n")
        try_write(separator.join(header) + "\n")
    else:
        log("without header")


def write_data(data: []):
    """
    Save the data given
    :param data: array of native type (int, bool, float, string, ...)
    :return: void
    """
    global file_path
    global separator
    global decimal_character

    if not os.path.exists(file_path):
        global last_header
        create_file()
        write_header(last_header)

    for i in range(len(data)):
        if decimal_character != '.' and not is_int(data[i]) and is_float(data[i]):
            data[i] = data[i].replace('.', decimal_character)

    try_write(separator.join(data) + "\n", rewrite_header_if_error=True)


def try_write(data: str, try_count=1, rewrite_header_if_error=False):
    """Try to write into the current file. If a PermissionError is raised, a new file is created."""
    global file_path
    if try_count > 5:
        raise PermissionError

    try:
        with open(file_path, "a") as file:
            file.write(data)
    except PermissionError:
        create_file()
        global last_header
        if rewrite_header_if_error and len(last_header) > 0:
            try_write(last_header, try_count + 1)
        try_write(data, try_count + 1)


def is_int(text: str):
    """Check is text matchs with an int"""
    return re.match(r"^[-+]?\d+$", text)


def is_float(text: str):
    """Check is text matchs with a float"""
    return re.match(r"[-+]?\d+(\.\d*)?$", text)


def write_datas(data: []):
    """
    Save the data given. Line are splited by *separator*
    :param data: array of array of native type (int, bool, float, string, ...)
    :return: void
    """
    for line in data:
        if line:
            write_data(line)


def derived(ori_line: pyplot_utils.plt.Line2D, derived_line: pyplot_utils.plt.Line2D, degree: int):
    """Add all missing derivative values to have the same number of points as the main line"""
    ori_xdata, ori_ydata = utils.get_data(ori_line)
    derived_xdata = utils.get_xdata(derived_line)

    if len(derived_xdata) > len(ori_xdata):
        pyplot_utils.clear_line(derived_line)

    if len(derived_xdata) == 0:
        diff = len(ori_xdata)
    else:
        index_equal = 1
        # Try to find the last derived x in the original list
        while ori_xdata[-index_equal] != derived_xdata[-1] and index_equal <= len(ori_xdata):
            index_equal += 1
        if index_equal >= len(ori_xdata):  # If no match
            diff = len(ori_xdata)
        else:
            diff = index_equal - 1  # We go back 1 because we started at 1

    new_x = [None for _ in range(diff)]
    new_y = [None for _ in range(diff)]

    for i in range(0, diff):
        start_index = -diff - degree + i
        if start_index < -len(ori_xdata):
            continue
        end_index = -diff + i + 1
        if end_index == 0:
            x_to_add = ori_xdata[start_index:]
            y_to_add = ori_ydata[start_index:]
        else:
            x_to_add = ori_xdata[start_index:end_index]
            y_to_add = ori_ydata[start_index:end_index]
        try:
            y = utils.get_derived(x_to_add, y_to_add, degree)
            # only if y computed, new_x and new_y are feed
            new_x[i] = x_to_add[-1]
            new_y[i] = y
        except IndexError:  # if not enough data to build a derived
            pass

    new_x = [x for x in new_x if x is not None]
    new_y = [y for y in new_y if y is not None]
    if len(new_x) > 0:
        utils.add_values(derived_line, new_x, new_y, max_values)


def log(data: str):
    """
    Log the data.
    :param data: any | string
    :return: void
    """
    print(data)


class AxesSynchronizer:
    """Axes Synchronizer"""

    def __init__(self, timeout: float, ori_axis, axes: []):
        self._timeout = timeout
        self._last_refresh = time.time()
        self._ori_axis = ori_axis
        self._axes = axes

    def get_ori_axis(self):
        """Get oriAxis"""
        return self._ori_axis

    def try_synchronize(self):
        """Try to synchronize axes dimensions"""
        if time.time() - self._last_refresh >= self._timeout:
            self._last_refresh = time.time()
            pyplot_utils.synchronize_axes(self._ori_axis, self._axes)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    main()
