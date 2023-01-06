cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

find_package(swig_conan_test CONFIG REQUIRED)

add_executable(example src/example.cpp)
target_link_libraries(example swig_conan_test::swig_conan_test)
