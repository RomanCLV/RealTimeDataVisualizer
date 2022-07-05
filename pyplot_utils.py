# -*- coding: utf-8 -*-

"""
pyplot_utils module

Copyright © 2021 Roman Clavier

This module is helping to use the matplotlib.pyplot module
"""

import matplotlib.pyplot as plt
import numpy as np

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')

default_marker = "-o"


def init_plot():
    """Init"""
    # this is the call to matplotlib that allows dynamic plotting
    plt.ion()


def create_plot(window_title=None, fig_title=None, close_event=None):
    """Create a new plot"""

    # Cut your window in 2 rows and 1 column, and start a plot in the first part

    fig = plt.figure(figsize=(18, 10), dpi=80)  # default dpi = 100.0
    # fig = plt.figure(num=None, figsize=(18, 10), dpi=80, facecolor='white', edgecolor='red')

    if fig_title is not None:
        set_title(fig, fig_title)

    if window_title is not None:
        set_window_title(fig, window_title)

    if close_event is not None:
        set_close_event(fig, close_event)

    plt.show()
    return fig


def add_multi_axis(row, column):
    """
    Add multi axis
    :return: The new figure
    """

    result = plt.subplots(nrows=row, ncols=column)
    fig = result[0]
    fig.set_size_inches(18.5, 10.5)
    fig.set_dpi(80)

    plt.show()
    return fig


def set_close_event(fig, close_event):
    """Set event closing"""
    fig.canvas.mpl_connect("close_event", close_event)


def set_window_title(fig, title):
    """Set window title"""
    fig.canvas.manager.set_window_title(title)


def set_title(fig, title, fontsize=16):
    """Set fig's title"""
    fig.suptitle(title, fontsize=fontsize)


def refresh_plot(interval=0.01):
    """Refresh fig"""
    plt.pause(interval)


def clear_fig(fig):
    """Clear fig"""
    fig.clear()


def add_axis(fig, pos, title=None, xlabel=None, ylabel=None):
    """add axis"""
    # if pos is : 121
    # Cut your window in 1 row and 2 columns, and start a plot in the first part

    axis = fig.add_subplot(pos)

    # update plot label/title

    # plt.title(title)              # set the title of the last axis created
    # plt.xlabel(xlabel)            # set the x label of the last axis created
    # plt.ylabel(ylabel)            # set the y label of the last axis created

    if title is not None:
        set_axis_title(axis, title)

    if xlabel is not None:
        set_axis_xlabel(axis, xlabel)

    if ylabel is not None:
        set_axis_ylabel(axis, ylabel)

    return axis


def set_axis_title(axis, title):
    """Set axis' title"""
    # axis.title.set_text(title)
    axis.set_title(title)


def set_axis_label(axis, xlabel, ylabel):
    """Set axiss labels"""
    set_axis_xlabel(axis, xlabel)
    set_axis_ylabel(axis, ylabel)


def set_axis_xlabel(axis, xlabel):
    """Set axis' xlabel"""
    axis.set_xlabel(xlabel)


def set_axis_ylabel(axis, ylabel):
    """Set axis' ylabel"""
    axis.set_ylabel(ylabel)


def clear_axis(axis):
    """Clear an axis"""
    axis.clear()


def remove_axis(axis):
    """Remove axis"""
    axis.remove()


def add_line(axis, xvalue=None, yvalue=None):
    """add a line"""
    # create a variable for the line, so we can later update it
    if xvalue is None:
        xvalue = []
    if yvalue is None:
        yvalue = []
    return axis.plot(xvalue, yvalue, default_marker, alpha=0.8)[0]


def remove_line(line):
    """Remove a line"""
    line.axes.lines.remove(line)


def clear_line(line):
    """Clear line data"""
    line.set_xdata(np.empty(0))
    line.set_ydata(np.empty(0))


def set_color(line, color):
    """Set the line's color"""
    line.set_color(color)


def set_marker(line, marker):
    """Set the line's marker"""
    line.set_marker(None if marker == "None" else marker)


def add_values(line, x, y, max_values=None, margin_coef=0.95):
    """Add values to a line"""

    if max_values is None:
        x_data = np.append(line.get_xdata(), x)
        y_data = np.append(line.get_ydata(), y)
    else:
        if max_values < 1:
            raise ValueError("max_values is a positiv no-null integer")
        else:
            # manage size of data
            x_data = line.get_xdata()
            y_data = line.get_ydata()
            diff = len(x_data) - max_values
            if diff > 0:    # too many values
                x_data = x_data[diff:]
                y_data = y_data[diff:]
            x_data = np.append(x_data, x)
            y_data = np.append(y_data, y)

    x_min = np.min(x_data)
    x_max = np.max(x_data)
    y_min = np.min(y_data)
    y_max = np.max(y_data)

    x_lim_min, x_lim_max = line.axes.get_xlim()
    y_lim_min, y_lim_max = line.axes.get_ylim()

    x_lim_min *= margin_coef
    x_lim_max *= margin_coef
    y_lim_min *= margin_coef
    y_lim_max *= margin_coef

    marge_bound_coef = 0.10

    # check x bounds
    if x_min <= x_lim_min or x_max >= x_lim_max:
        std = np.std(x_data)
        if std == 0:
            std = 0.1

        if x_min <= x_lim_min and x_max < x_lim_max:        # just x min
            line.axes.set_xlim([x_min - std, x_lim_max + std * marge_bound_coef])
        elif x_min > x_lim_min and x_max >= x_lim_max:      # just x max
            if max_values is None:
                line.axes.set_xlim([x_lim_min - std * marge_bound_coef, x_max + std])
            else:
                line.axes.set_xlim([x_min - std * marge_bound_coef, x_max + std])
        else:                                               # both
            line.axes.set_xlim([x_min - std, x_max + std])

    # check y bounds
    if y_min <= y_lim_min or y_max >= y_lim_max:
        std = np.std(y_data)
        if std == 0:
            std = 0.1

        if y_min <= y_lim_min and y_max < y_lim_max:        # just y min
            line.axes.set_ylim([y_min - std, y_lim_max + std * marge_bound_coef])
        elif y_min > y_lim_min and y_max >= y_lim_max:      # just x max
            line.axes.set_ylim([y_lim_min - std * marge_bound_coef, y_max + std])
        else:                                               # both
            line.axes.set_ylim([y_min - std, y_max + std])

    line.set_xdata(x_data)
    line.set_ydata(y_data)


def get_line_derived(line, degree=1):
    """Get derived from a line"""
    return get_derived(get_xdata(line), get_ydata(line), degree)


def get_derived(x_data, y_data, degree=1):
    """
    Get derived value
    :param x_data: The x array
    :param y_data: The y array
    :param degree: The degree of derivation
    :return: Dy / Dx of the desired degree
    """
    if degree < 0:
        raise ValueError("Degree is positive or null : *degree* >= 0")
    if degree == 0:         # derivated function of degree 0 is itselft
        return y_data[-1]

    if len(x_data) <= degree:
        raise IndexError("Not enough value")

    if degree == 1:
        x0 = x_data[-2]
        x1 = x_data[-1]
        y0 = y_data[-2]
        y1 = y_data[-1]
        return (y1 - y0) / (x1 - x0)

    new_x_data = [None for _ in range(degree)]
    new_y_data = [None for _ in range(degree)]

    # take only the required values to compute the next recursion
    for i in range(degree):
        x0 = x_data[-2 - i]
        x1 = x_data[-1 - i]
        y0 = y_data[-2 - i]
        y1 = y_data[-1 - i]
        new_x_data[-1 - i] = x1
        new_y_data[-1 - i] = (y1 - y0) / (x1 - x0)

    return get_derived(new_x_data, new_y_data, degree - 1)


def get_data(line):
    """Get xdata and ydata"""
    return line.get_data()


def get_xdata(line):
    """get x_data"""
    return line.get_xdata()


def get_ydata(line):
    """get y_data"""
    return line.get_ydata()


def synchronize_axes(ori_axis, axes):
    """Synchronize the X axis dimensions with respect of the ori_axis dimensions."""
    x_min_ori, x_max_ori = ori_axis.get_xlim()
    for axis in axes:
        x_min, x_max = axis.get_xlim()

        if x_min != x_min_ori or x_max != x_max_ori:
            axis.set_xlim(x_min_ori, x_max_ori)
