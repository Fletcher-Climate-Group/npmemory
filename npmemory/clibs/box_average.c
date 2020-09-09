/*
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
*/

// Sample code which takes an input n x m grid, and performs a box average.
// Note: It is expected that n mod k = 0, and m mod j = 0.

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>


void crash_logger(int error_code){
    // If program encounters a problem, crash
    // immediately to prevent memory corruption.

    printf("npmemory encountered an error in C module.\n");
    printf("Exiting with error code %d", error_code);
    exit(error_code);
}


int work_size(int xdim, int ydim, int xstep, int ystep){
    // Some bounds checking and modular arithmetic.

    if (xdim % xstep != 0){
        printf("Incompatible xstep specified: %d", xstep);
        crash_logger(-1);
    }

    if (ydim % ystep != 0){
        printf("Incompatible ystep specified: %d", ystep);
        crash_logger(-1);
    }

    int xgrid = xdim / xstep;
    int ygrid = ydim / ystep;

    int work_grid_size = xgrid * ygrid;

    return work_grid_size;
}


void box_average(void * np_ptr, int xdim, int ydim, int xstep, int ystep){
    // Passing a void pointer, which is then cast into a 1D float
    // array. Key thing to remember: All numpy ndarray objects are 1D
    // in C (in terms of how they are physically represented).

    // So, we have a 2D array in Python which is represented as a
    // flattened 1D array in C.

    float * box;
    box = (float*) np_ptr;

    // Array to store the intermediate results of the box average.
    int work_array_size = work_size(xdim, ydim, xstep, ystep);
    float * work_array = calloc(work_array_size, sizeof(float));

    int i, j;

    int work_x_max = xdim / xstep;
    int work_y_max = ydim / ystep;

    for (i = 0; i < xdim; i++){
        for (j = 0; j < ydim; j++){
            // Calculate work index
            int work_x = i / xstep;
            int work_y = j / ystep;
            int work_idx = work_x * work_y_max + work_y;
            int box_idx = i * ydim + j;

            work_array[work_idx] += box[box_idx];
        }
    }

    // Iterating over work array
    float subgrid_size = (float) (xstep * ystep);

    for (i = 0; i < work_x_max; i++){
        for (j = 0; j < work_y_max; j++){
            int work_idx = i * work_y_max + j;
            work_array[work_idx] = work_array[work_idx] / subgrid_size;
        }
    }

    // Now, assigning values based on corresponding work_idx
    for (i = 0; i < xdim; i++){
        for (j = 0; j < ydim; j++){
            int work_x = i / xstep;
            int work_y = j / ystep;
            int work_idx = work_x * work_y_max + work_y;
            int box_idx = i * ydim + j;
            box[box_idx] = work_array[work_idx];
        }
    }

    return;
}