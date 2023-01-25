set(target swig_conan_test)

find_package(Python3 COMPONENTS Development REQUIRED)
find_package(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})

FIND_PACKAGE(PythonLibs)
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})

INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})

# set(SWIG_SOURCES ../mylib/swig_conan_test.cpp swig_conan_test.i)

set(SWIG_SOURCES swig_conan_test.i)

set_property(SOURCE ${target}.i PROPERTY CPLUSPLUS ON)
set_property(SOURCE ${target}.i PROPERTY SWIG_MODULE_NAME swig_conan_test)

swig_add_library(${target} LANGUAGE python SOURCES ${SWIG_SOURCES})
set_property(TARGET ${target} PROPERTY SWIG_INCLUDE_DIRECTORIES ${CMAKE_SOURCE_DIR}/include)
target_link_libraries(${target} ${PYTHON_LIBRARIES} mylib)

install(TARGETS ${target} DESTINATION python)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/swig_conan_test.py" DESTINATION python)
