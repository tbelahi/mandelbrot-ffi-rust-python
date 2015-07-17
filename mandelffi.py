#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
FFI wrapper to call mandelbrot set from a library written in Rust(src/lib.rs => tartget/release/libmandelbrot.so)
Writting the wrapper is copied from: https://github.com/urschrei/rust_bng.git
"""

#
# imports
#
import numpy as np
import matplotlib.pyplot as pl
import time
from ctypes import cdll, c_double, Structure, POINTER,  c_uint32, c_size_t,\
    c_void_p, cast

#
# wrapper around the library
#
libmandel = cdll.LoadLibrary('target/release/libmandelbrot.so')


class FFIArray(Structure):
    _fields_ = [("data", c_void_p),
                ("len", c_size_t)]

    # not sure if this one is useful
    @classmethod
    def from_param(cls, seq):
        return seq if isinstance(seq, cls) else cls(seq)

    def __init__(self, seq, data_type=c_double):
        array_type = data_type * len(seq)
        raw_seq    = array_type(*seq)
        self.data  = cast(raw_seq, c_void_p)
        self.len   = len(seq)


def void_array_to_list(array, _func, _args):
    return cast(array.data, POINTER(c_double * array.len))[0]

mandelbrot_ffi = libmandel.mandelffi
mandelbrot_ffi.argtypes = (c_size_t, c_uint32)
mandelbrot_ffi.restype  = FFIArray
mandelbrot_ffi.errcheck = void_array_to_list


# Since we defined void_array_to_list to overide the result from a FFIArray  and
#return the pointer (c_void_p) casted as POINTER(array of c_double)
# I define a new function to "consume" the pointer
def mandelbrot(SIZE, iterations):
    res_pointer = [res for res in mandelbrot_ffi(SIZE, iterations)]
    res_numpy_inline = np.array(res_pointer)
    res = res_numpy_inline.reshape((SIZE, SIZE))
    return res


# pure numpy implementation for the sake of timing the differences
# code from : https://scipy-lectures.github.io/intro/numpy/exercises.html
def compute_mandelbrot(N_max, some_threshold, nx, ny):
    # A grid of c-values
    x = np.linspace(-2.5, 1.5, nx)
    y = np.linspace(-2.0, 2.0, ny)

    c = x[:, np.newaxis] + 1j*y[np.newaxis, :]

    # Mandelbrot iteration

    z = c
    for j in xrange(N_max):
        z = z**2 + c

    mandelbrot_set = (abs(z) < some_threshold)

    return mandelbrot_set


#
# main
#
def main():
    SIZE = 1800
    iterations = 400
    t0 = time.time()
    mset = mandelbrot(SIZE, iterations)
    t1 = time.time()
    mset_purenumpy = compute_mandelbrot(iterations, 2.0, SIZE, SIZE)
    t2 = time.time()
    print "ellapsed times:"
    print " python + Rust FFI: ", t1-t0, " seconds"
    print " pure numpy       : ", t2-t1, " seconds"
    print "speed-up: ", (t2-t1)/(t1-t0), "x"
    pl.imshow(mset, cmap="gray")
    pl.title("Rust")
    pl.figure()
    pl.imshow(mset_purenumpy.T, cmap="gray")
    pl.title("Numpy")
    pl.show()

if __name__ == "__main__":
    main()
