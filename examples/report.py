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

import time
import ctypes

import numpy as np

import npmemory


def print_report(py_time, c_time, py_array, c_array):

    print("Time elapsed C routine:", c_time)
    print("Time elapsed Python:", py_time)

    abs_error_array = np.abs(py_array - c_array)

    npmemory.tools.arr_info(abs_error_array, "error_array")

    # Note, these computations oculd also be done using np.float64 - that
    # is also an option. This would result in a lower floating_point_tolerance
    # (i.e. more precise results).

    floating_point_tolerance = 0.00001
    print("Floating point tolerance:", floating_point_tolerance)

    if abs_error_array.max() < floating_point_tolerance:
        print("Success: Grid results are consistent between Python and C methods up to floating-point tolerance.")
    else:
        print("Failed: Python and C methods return different results - check implementation.")

    factor = py_time / c_time
    print(f"Speed differential: {factor:03}")


def build_report():

    test_dims = (1200,1000)

    random_array_64 = np.random.rand(test_dims[0], test_dims[1])

    random_array = np.float32(random_array_64)

    inc_x = 60
    inc_y = 25

    t0 = time.time()

    random_c_array = np.copy(random_array)
    npmemory.analysis.c_box_average(random_c_array, inc_x, inc_y)

    t1 = time.time()

    c_elapsed = t1 - t0

    t2 = time.time()

    random_py_array = np.copy(random_array)
    py_box = npmemory.analysis.py_box_average(random_py_array, inc_x, inc_y)

    t3 = time.time()

    py_elapsed = t3 - t2

    print_report(py_elapsed, c_elapsed, py_box, random_c_array)


build_report()

