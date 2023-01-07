[![create_conan_package](https://github.com/EstebanDugueperoux2/swig_conan_test/actions/workflows/main.yml/badge.svg)](https://github.com/EstebanDugueperoux2/swig_conan_test/actions/workflows/main.yml)

# swig_conan_test

```
conan new swig_conan_test/0.0.1 --template=cmake_lib

#Update CMakeLists.txt as in documented in :

- OUTDATED: https://www.swig.org/Doc4.1/SWIGDocumentation.html#Introduction_build_system 
- https://cmake.org/cmake/help/latest/module/UseSWIG.html

docker run --rm -ti -v ${PWD}:/home/conan/project conanio/gcc12-ubuntu18.04
cd project

conan create . \
    --profile:build .conan/profiles/gcc12 \
    --profile:host .conan/profiles/gcc12 \ 
    --build missing \
    -c tools.system.package_manager:mode=install \
    -c tools.system.package_manager:sudo=True


```

Works only with swig 4.0.2 but not with 4.1.0 release because of:

```
CMake Error at /home/estebandugueperoux/.conan/data/cmake/3.25.0/_/_/package/5c09c752508b674ca5cb1f2d327b5a2d582866c8/share/cmake-3.25/Modules/FindPackageHandleStandardArgs.cmake:230 (message):
  Could NOT find SWIG (missing: SWIG_DIR)
Call Stack (most recent call first):
  /home/estebandugueperoux/.conan/data/cmake/3.25.0/_/_/package/5c09c752508b674ca5cb1f2d327b5a2d582866c8/share/cmake-3.25/Modules/FindPackageHandleStandardArgs.cmake:600 (_FPHSA_FAILURE_MESSAGE)
  /home/estebandugueperoux/.conan/data/cmake/3.25.0/_/_/package/5c09c752508b674ca5cb1f2d327b5a2d582866c8/share/cmake-3.25/Modules/FindSWIG.cmake:153 (find_package_handle_standard_args)
  src/python/CMakeLists.txt:4 (find_package)
```