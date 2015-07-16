extern crate libc;
extern crate num;

use libc::{size_t, uint32_t, c_void, c_float};
use num::complex::{Complex64};
use std::iter;
use std::mem;

#[test]
fn it_works() {
    let x = mandelbrot(400,20);
    assert!(x.len() == 400);
    assert!(x[0].len() == 400);
    assert!(x[0][0] == 0.0);
}

#[repr(C)]
pub struct Array {
    data: *const c_void,
    len: size_t,
}

impl Array {
    fn from_vec<T>(mut vec: Vec<T>) -> Array {
        vec.shrink_to_fit();

        let array = Array{
            data: vec.as_ptr() as *const libc::c_void,
            len: vec.len() as libc::size_t,
        };

        mem::forget(vec);

        array
    }
}

#[no_mangle]
pub extern fn mandelbrot(SIZE:usize, maxiteration:i32) -> Vec<Vec<f64>> {
    let x = (0..SIZE).map(|i| -2.5 + (i as f64)*(4.0/(SIZE-1) as f64 )).collect::<Vec<f64>>();
    let y = (0..SIZE).map(|i| -2.0 + (i as f64)*(4.0/(SIZE-1) as f64 )).collect::<Vec<f64>>();

    let res_row = iter::repeat(0f64).take(SIZE).collect::<Vec<f64>>();
    let mut res = iter::repeat(res_row).take(SIZE).collect::<Vec<Vec<f64>>>();

    for i in 0..SIZE {
        for j in 0..SIZE{
            let c_real = x[j];
            let c_imag = y[i];
            let mut z_real = x[j];
            let mut z_imag = y[i];
            let mut z_real_2 = z_real*z_real;
            let mut z_imag_2 = z_imag*z_imag;
            for k in 0..(maxiteration as usize) {
                z_imag = 2.0*z_real*z_imag + c_imag;
                z_real = z_real_2 -z_imag_2 + c_real;
                z_real_2 = z_real*z_real;
                z_imag_2 = z_imag*z_imag;
                }
            if ((z_real*z_real + z_imag*z_imag) < 2.0*2.0) && (!(z_real.is_nan() || z_imag.is_nan())) {
                res[i][j] = 10.0;
            }
            else {
                res[i][j] = 0.0;
             }
            }

        };
    
    return res
}

#[no_mangle]
pub extern fn mandelffi(N:size_t, maxit:uint32_t ) -> Array {
//pub extern fn mandelffi(N:size_t, maxit:uint32_t ) -> uint32_t {
    let res = mandelbrot(N as usize, maxit as i32);
    let mut res_flat = iter::repeat(0f64).take((N*N) as usize).collect::<Vec<f64>>();
    let SIZE = N as usize;
    for i in 0..SIZE {
        for j in 0..SIZE {
            let index = i*(N as usize)+j;
            res_flat[index] = res[i][j];
        }
    }
    Array::from_vec(res_flat)
}
