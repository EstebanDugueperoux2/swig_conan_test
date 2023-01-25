%module swig_conan_test
// %{
// /* Put header files here or function declarations like below */
// extern void swig_conan_test();
// %}

// extern void swig_conan_test();

%{
#include "swig_conan_test.h"
%}

// Make SWIG look into this header:
%include "swig_conan_test.h"