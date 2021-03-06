"""
Copyright © 2020 Daniel Hogg

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
“Software”), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import sys
import ctypes
import pkg_resources

import numpy as np

import npmemory.tools

# Must import .dll or .so here (or .dylib for OSX)
ANALYSIS_BINARY = None

if sys.platform == 'linux' or sys.platform == 'linux2':
    ANALYSIS_BINARY = pkg_resources.resource_filename('npmemory.clibs', 'box_average.so')
elif sys.platform == 'darwin':
    ANALYSIS_BINARY = pkg_resources.resource_filename('npmemory.clibs', 'box_average.dylib')
elif sys.platform == 'win32':
    ANALYSIS_BINARY = pkg_resources.resource_filename('npmemory.clibs', 'box_average.dll')
else:
    raise OSError(f"Operating system not supported: {sys.platform}")


c_executable = ctypes.CDLL(ANALYSIS_BINARY)
box_average = c_executable.box_average



def c_box_average(np_array, x_inc, y_inc, debug=False):
    """
    Call C routine from CDLL to accelerate box average.
    """

    # Ensure float32 input

    # TODO: Insert type check

    shape = np_array.shape
    
    if len(shape) != 2:
        raise ValueError("Incorrect grid dimensions.")

    x_dim = shape[0]
    y_dim = shape[1]

    # Mandatory conversion to pointers via ctypes
    np_ptr = ctypes.c_void_p(np_array.ctypes.data)
    x_len = ctypes.c_int(x_dim)
    y_len = ctypes.c_int(y_dim)
    c_x_inc = ctypes.c_int(x_inc)
    c_y_inc = ctypes.c_int(y_inc)

    box_average(np_ptr, x_len, y_len, c_x_inc, c_y_inc)



def py_box_average(np_array, x_inc, y_inc, debug=False):
    """
    Box averaging, written in pure Python
    """

    shape = np_array.shape
    
    if len(shape) != 2:
        raise ValueError("Incorrect grid dimensions.")

    x_dim = shape[0]
    y_dim = shape[1]

    x_grid = x_dim // x_inc
    y_grid = y_dim // y_inc

    work_array = np.zeros((x_grid, y_grid), dtype=float)

    for x in range(0, x_dim):
        for y in range(0, y_dim):
            work_x = int(x // x_inc)
            work_y = int(y // y_inc)
            work_array[work_x][work_y] += np_array[x][y]

    subgrid_size = x_inc * y_inc

    for i in range(0, x_grid):
        for j in range(0, y_grid):
            work_array[i][j] = work_array[i][j] / subgrid_size

    for x in range(0, x_dim):
        for y in range(0, y_dim):
            work_x = int(x // x_inc)
            work_y = int(y // y_inc)
            np_array[x][y] = work_array[work_x][work_y]

    if debug:
        npmemory.tools.arr_info(np_array, "np_array")

    return np_array
