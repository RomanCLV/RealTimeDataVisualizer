# -*- coding: utf-8 -*-

"""
Main module

Copyright © 2022 Roman Clavier

Python describing
"""

from datetime import datetime
import time
import re
import os
import signal
import argparse

import command_helper as helper

# Additional modules added in the __name__ == "__main__" bloc

global run
global fig

global is_connected
global serial_port
global com_ports
global com_ports_index
global port_delay
global last_read_data_time
global on_close_id

global base_path
global file_path
global created_files
global update_title_requested
global last_header
global all_headers

global remove_unused_files
global separator
global max_values
global decimal_character
global axes_synchronizer


def main():
    """The main function"""
    global run
    global fig

    global is_connected
    global serial_port
    global com_ports
    global com_ports_index
    global port_delay
    global last_read_data_time
    global on_close_id

    global base_path
    global file_path
    global created_files
    global update_title_requested
    global last_header
    global all_headers

    global remove_unused_files
    global separator
    global max_values
    global decimal_character
    global axes_synchronizer

    args = parser.parse_args()

    run = True
    fig = None

    is_connected = False
    serial_port = None
    com_ports = []
    com_ports_index = 0
    port_delay = None
    last_read_data_time = 0
    on_close_id = None

    base_path = os.path.join(os.getcwd(), "data")
    file_path = ""
    created_files = []
    update_title_requested = False
    last_header = []
    all_headers = []

    remove_unused_files = False
    max_values = None
    separator = ";"
    decimal_character = "."
    axes_synchronizer = []

    print()

    if args.port:
        for port in args.port:
            com_ports.append(port.strip())

    if args.file:
        get_ports(args.file)

    if len(com_ports) == 0:
        # print("No communication port specified.\n"
        #      "Try to read the ports.txt file.")
        get_ports("ports.txt")

    if len(com_ports) == 0:
        print("No communication port selected.\n"
              "To specify it (or them), you can:\n"
              "- create the file ports.txt and write the available ports you want\n"
              "- use main.py -p [PORT1 PORT2 ...] or main.py -f my_ports.txt (both commands can be combined)")
        input("Please press the Enter key to exit")
        exit(0)

    if args.delay is not None:
        if args.delay > 0:
            port_delay = args.delay
        else:
            print(f"The communication port delay must be a non-null positive integer. Given: {args.delay}")
            input("Please press the Enter key to exit")
            exit(-1)

    print("Available ports selected:")
    for port in com_ports:
        print(port)
    print()

    while run:
        if not is_connected:
            if fig:
                close_fig()

            if serial_port:
                disconnect()

            if com_ports_index >= len(com_ports) or com_ports_index < 0:
                com_ports_index = 0

            if connect(com_ports[com_ports_index]):
                last_read_data_time = time.time()
            else:
                com_ports_index += 1
        else:
            read()
        if fig:
            utils.refresh_plot(fig, 0.01)

    disconnect()
    close_fig()

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


def sigint_handler(sign, frame):
    """Catch KeyboardInterrupt"""
    global run
    run = False


def get_ports(filepath):
    """Try to get ports from the given file."""
    global com_ports

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            lines = file.readlines()
        for line in lines:
            item = line.strip()
            if item and item not in com_ports:
                com_ports.append(item)
    else:
        print(f"File not found: {filepath}")


def connect(com_name, baud_rate=9600, timeout=0.01):
    """
    Try to connect with the arduino
    :param com_name: Name of communication port
    :param baud_rate: Communication's frequency
    :param timeout: Timer before continue
    :return: void
    """
    global is_connected
    global serial_port

    try:
        serial_port = serial.Serial(com_name, baudrate=baud_rate, timeout=timeout)
        is_connected = True
        print(f"Connection success to: {serial_port.name} at baud rate: {serial_port.baudrate}\n")
    except serial.SerialException:
        is_connected = False
        print(f"Connection failed to: {com_name}")
        time.sleep(1)
    return is_connected


def disconnect():
    """Disconnect serial_port"""
    global serial_port
    if serial_port:
        print(f"\nClosing serial port: {serial_port.name}\n")
        serial_port.close()
        serial_port = None


def read():
    """
    Read data from Arduino card
    """
    global fig

    global is_connected
    global serial_port
    global com_ports_index
    global port_delay
    global last_read_data_time

    global file_path
    global remove_unused_files
    global last_header

    global update_title_requested
    global max_values
    global separator
    global decimal_character
    global axes_synchronizer

    try:
        data_read = serial_port.readline()

    except serial.SerialException as err:
        is_connected = False
        log(f"{type(err).__name__}: {err}")
        return

    if not data_read:
        if port_delay and time.time() - last_read_data_time > port_delay:
            is_connected = False
            com_ports_index += 1
        return
    else:
        last_read_data_time = time.time()

    for synchronizer in axes_synchronizer:
        synchronizer.try_synchronize()

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

            if fig:
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
            pos = data[1]
            title = data[2] if len(data) >= 3 else None
            x_label = data[3] if len(data) >= 4 else None
            y_label = data[4] if len(data) >= 5 else None
            add_axis(pos, title, x_label, y_label)

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
                    utils.synchronize_axes(ori_axis, axes)
                else:
                    axes_synchronizer.append(AxesSynchronizer(data[1], ori_axis, axes))

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

        case "-sl":
            utils.set_style(get_line(fig, data[1], data[2]), data[3])

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
            write_datas(list(map(lambda item: [str(item[0]), str(item[1])], data[3])))
            x = []
            y = []

            for dt in data[3]:
                x.append(dt[0])
                y.append(dt[1])
            utils.add_values(get_line(fig, data[1], data[2]), x, y, max_values)

        case "-ld":
            utils.compute_derivative(get_line(fig, data[1], data[2]),
                                     get_line(fig, data[3], data[4]),
                                     max_values,
                                     data[5] if len(data) == 6 else 1)

        case _:
            log(f"Unknown {data_decoded}")

    if update_title_requested and fig is not None:
        utils.set_title(fig, file_path)
        update_title_requested = False


def read_validation_error(cmd: str, message: str, data_err: str):
    """Print a message to indicate an error occurred"""
    log(f"Validation error:\n  Command: {cmd}\n  Message: {message}\n  Given: {data_err}")


def close_fig():
    """Close current fig"""
    global fig
    global on_close_id
    utils.close(fig, on_close_id)
    fig = None
    on_close_id = None


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


def add_axis(pos, title=None, x_label=None, y_label=None):
    """Add an axis"""
    global fig
    global on_close_id

    if fig is None:
        fig, on_close_id = utils.create_plot(window_title="Real time data visualizer", fig_title=file_path,
                                             close_event=on_close)

    utils.add_axis(fig, pos, title, x_label, y_label)


def add_multi_axis(row: int, column: int):
    """Set axis format"""
    global fig
    global on_close_id

    if fig:
        close_fig()

    fig = utils.add_multi_axis(row, column)
    on_close_id = utils.set_close_event(fig, on_close)
    utils.set_window_title(fig, "Real time data visualizer")
    utils.set_title(fig, file_path)


def remove_synchronizer_on(ori_axis):
    """Remove all the synchronizer having this reference axis."""
    global axes_synchronizer
    i = 0
    while i < len(axes_synchronizer):
        if axes_synchronizer[i].get_ori_axis() == ori_axis:
            axes_synchronizer.remove(axes_synchronizer[i])
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
    """Check if text matches with an int"""
    return re.match(r"^[-+]?\d+$", text)


def is_float(text: str):
    """Check if text matches with a float"""
    return re.match(r"[-+]?\d+(\.\d*)?$", text)


def write_datas(data: []):
    """
    Save the data given. Line are split by *separator*
    :param data: array of array of native type (int, bool, float, string, ...)
    :return: void
    """
    for line in data:
        if line:
            write_data(line)


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
            utils.synchronize_axes(self._ori_axis, self._axes)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)

    try:
        import serial
        import pyplot_utils as utils
    except ImportError as error:
        print(f"\n{type(error).__name__}: {error.msg}\n")
        print("To install all required packages/modules, use: python pip install -r requirements.txt\n")
        input("Please press the Enter key to exit")
        exit(-1)

    parser = argparse.ArgumentParser(description="main.py CLI")
    parser.add_argument("-p", "--port", type=str, nargs="+", help="set the communication ports.")
    parser.add_argument("-f", "--file", type=str, help="set the file containing all communication ports.")
    parser.add_argument("-d", "--delay", type=int,
                        help="set a delay (in seconds) to automatically change the communication port if no data is received, even if the connection to the port was successful.")
    main()
