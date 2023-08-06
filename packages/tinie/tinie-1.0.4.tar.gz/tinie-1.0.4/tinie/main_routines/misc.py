#!/usr/bin/env python3
"""
Helper functions.
"""

import matplotlib.pyplot as plt
import numpy as np
import sys


def fd(x, T):
    """
    Fermi-Dirac distribution 1/[ exp(x/T) + 1 ]

    Parameters
    ----------
    x:         float,
               Energy.

    T:         float,
               Distribution broadening.
    """

    if T == 0.0:
        return 1.0 if x > 0 else 0.0
    else:
        return 1.0 / (np.exp(x / T) + 1)


def FT(x, T):
    """
    Thermal broadening function

    Parameters:
    -----------
    x:          float,
                Energy.

    T:          float,
                Distribution broadening.
    """

    if T == 0.0:
        ans = np.zeros(x.shape)
        ans[abs(x) <= np.finfo(x.dtype).eps] = 1.0
        return ans

    else:
        return 1.0 / (4 * T * np.cosh(x / (2 * T)) ** 2)


# Parser helper functions:


def isint(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


def isfloat(val):
    try:
        float(val)
        return True
    except ValueError:
        return False


def string_checker(val):
    if isint(val):
        val = int(val)

    elif isfloat(val):
        val = float(val)

    return val


def handle_function_string(fun):
    """Takes a string of the form 'f(a, [b, c], (d, e, f))'
    and breaks it down into its constituent parts."""
    try:
        if not isinstance(fun, str):
            raise ValueError("Error: input is not a string.")
        if "(" not in fun:
            raise ValueError("Error: no opening function call bracket.")
        if fun[-1] != ")":
            raise ValueError("Error: no closing function call bracket.")
    except ValueError as e:
        print(e)
        sys.exit(1)

    params = []
    fun = fun[0:-1]
    fun = fun.split("(", 1)
    params.append(fun[0])  # Appending the function call
    args = fun[1].split(",")  # Creating the argument list
    arg_append = True
    l = []

    for arg in args:
        if arg == "":
            break

        if arg[0] == "[" or arg[0] == "(":
            arg_append = False

            if arg[0] == "[":
                l.append(string_checker(arg.strip("[")))
                continue

            else:
                l.append(string_checker(arg.strip("(")))
                continue

        if arg_append:
            params.append(string_checker(arg))

        if arg[-1] == "]" or arg[-1] == ")":
            arg_append = True

            if arg[-1] == "]":
                l.append(string_checker(arg.strip("]")))

            else:
                l.append(string_checker(arg.strip(")")))
                l = tuple(l)

            params.append(l)
            l = []

    return params


def handle_list_string(lis):
    """Takes a string of the form '[a, [b, c], (d, e, f)]'
    and breaks it down into its constituent parts."""
    try:
        if not isinstance(lis, str):
            raise ValueError("Error: list not typed as a string.")
        if lis[0] != "[" and lis[0] != "(":
            raise ValueError("Error: opening bracket is not [ or (.")
        if lis[-1] != "]" and lis[-1] != ")":
            raise ValueError("Error: closing bracket is not ] or ).")
    except ValueError as e:
        print(e)
        sys.exit(1)

    tuple_type = False

    params = []
    if lis[0] == "[" and lis[-1] == "]":
        lis = lis.lstrip("[")
        lis = lis.rstrip("]")
    else:
        tuple_type = True
        lis = lis.lstrip("(")
        lis = lis.rstrip(")")
    lis = lis.split(",")
    arg_append = True
    l = []

    for arg in lis:

        if arg[0] == "[" or arg[0] == "(":
            arg_append = False

            if arg[0] == "[":
                l.append(string_checker(arg.strip("[")))
                continue

            else:
                l.append(string_checker(arg.strip("(")))
                continue

        if arg_append:
            params.append(string_checker(arg))

        if arg[-1] == "]" or arg[-1] == ")":
            arg_append = True

            if arg[-1] == "]":
                l.append(string_checker(arg.strip("]")))

            else:
                l.append(string_checker(arg.strip(")")))
                l = tuple(l)

            params.append(l)
            l = []

    if tuple_type:
        params = tuple(params)

    return params


# Helper functions for creating pretty 2D figures with matplotlib.


def axes_real_aspect_ratio_to_golden(ax):
    """ Sets axis size ratio to golden ratio """
    try:
        if ax.get_xscale() != "linear":
            raise ValueError("Error: only linear axes scales supported.")
        if ax.get_yscale() != "linear":
            raise ValueError("Error: only linear axes scales supported.")
    except ValueError as e:
        print(e)
        sys.exit(1)

    x = ax.get_xlim()
    y = ax.get_ylim()
    gr = (np.sqrt(5.0) + 1) / 2
    ax.set_aspect((x[1] - x[0]) / (y[1] - y[0]) / gr)


def get_figure(width=246, aspect=(np.sqrt(5.0) + 1) / 2.0):
    """
    Returns a matplotlib figure. Default values produces figure whose
    width is 246 pt, i.e, the PRL column width and aspect ~ golden ratio.

    Parameters
    ----------
    width       int/float, optional
                width of the figure in 'pt' units (1 pt ≈ 0.3528 mm)
                Defaults to 246 pt, i.e., the width of a single column in
                Physical Review Letters
    aspect      int/float
                Sets width/height to this value

    Returns
    -------
    fig         matplotlib.pyplot.Figure
    """
    try:
        if not isinstance(width, (int, float, np.floating)):
            raise ValueError("Error: type(width) is not int,float or np.floating [was %s]." % repr(type(width)))
        if not isinstance(aspect, (int, float, np.floating)):
            raise ValueError("Error: type(aspect) is not int,float or np.floating [was %s]." % repr(type(aspect)))
    except ValueError as e:
        print(e)
        sys.exit(1)

    width = width / 72.0  # in inches
    height = width / aspect

    return plt.figure(figsize=(width, height))
