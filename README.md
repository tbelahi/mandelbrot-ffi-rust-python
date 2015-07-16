little project to learn Rust and the FFI interfacing to python.

Most of it is inspired by http://sensitivecities.com/rust-python-ffi-bng-EN.html

Lesson learned: 
One needs to interface python and C and C and Rust. This doulbe sided wrapping is a bit tedious and requires to understand c types and pointers. Not easy for people not familiar with C.
The rust library runs at least twice faster. Numpy already does a good job at taking advantage of Fortran and C routines.
