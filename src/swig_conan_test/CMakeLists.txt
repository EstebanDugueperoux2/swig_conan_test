set(target swig_conan_test)

find_package(Python3 COMPONENTS Development REQUIRED)
find_package(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})

FIND_PACKAGE(PythonLibs)
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})

INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})

set(SWIG_SOURCES ../mylib/swig_conan_test.cpp swig_conan_test.i)

set_property(SOURCE ${target}.i PROPERTY CPLUSPLUS ON)
set_property(SOURCE ${target}.i PROPERTY SWIG_MODULE_NAME swig_conan_test)
swig_add_library(${target} LANGUAGE python SOURCES ${SWIG_SOURCES})
target_include_directories(${target} PUBLIC ../../include)
swig_link_libraries(${target} ${PYTHON_LIBRARIES})

install(TARGETS ${target} DESTINATION python)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/swig_conan_test.py" DESTINATION python)
