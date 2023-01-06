set(target mylib_wrapper)

find_package(Python3 COMPONENTS Development REQUIRED)
find_package(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})

FIND_PACKAGE(PythonLibs)
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})

INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})

SET(CMAKE_SWIG_FLAGS "")

set(SWIG_SOURCES ../mylib/swig_conan_test.cpp swig_conan_test.i)

# SET_SOURCE_FILES_PR OPERTIES(${PROJECT_NAME}.i PROPERTIES CPLUSPLUS ON)
SET_SOURCE_FILES_PROPERTIES(${target}.i PROPERTIES SWIG_FLAGS "-includeall")
set_property(SOURCE ${target}.i PROPERTY CPLUSPLUS ON)
swig_add_library(${target} LANGUAGE python SOURCES ${SWIG_SOURCES})
target_include_directories(${target} PUBLIC ../../include)
swig_link_libraries(${target} ${PYTHON_LIBRARIES})

install(TARGETS ${target} DESTINATION python)
