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
import matplotlib.pyplot as plt

import npmemory


def build_report():

    test_dims = (1200,1000)

    random_array = np.random.rand(test_dims[0], test_dims[1])

    inc_x = 60
    inc_y = 25

    t0 = time.time()

    random_c_array = np.copy(random_array)

    npmemory.tools.arr_info(random_array, "random")

    npmemory.analysis.c_box_average(random_c_array, inc_x, inc_y)

    t1 = time.time()

    c_elapsed = t1 - t0
    npmemory.tools.arr_info(random_c_array, "c_after")
    print("Time elapsed:", c_elapsed)

    t2 = time.time()

    random_py_array = np.copy(random_array)

    npmemory.analysis.py_box_average(random_py_array, inc_x, inc_y)

    t3 = time.time()

    py_elapsed = t3 - t2
    npmemory.tools.arr_info(random_py_array, "py_after")
    print("Time elapsed Python:", py_elapsed)

    factor = py_elapsed / c_elapsed
    print(f"Speed differential: {factor:03}")

build_report()

