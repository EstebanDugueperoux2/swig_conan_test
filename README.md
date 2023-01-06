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
