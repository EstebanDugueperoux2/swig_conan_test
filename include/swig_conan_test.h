#pragma once

#ifdef _WIN32
  #define swig_conan_test_EXPORT __declspec(dllexport)
#else
  #define swig_conan_test_EXPORT
#endif

swig_conan_test_EXPORT void swig_conan_test();
