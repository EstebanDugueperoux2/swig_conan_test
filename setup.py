# from setuptools import Extension, setup
# from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as build_ext_orig
import os
import glob
from distutils.command.install_data import install_data
import os
import pathlib
import pkg_resources
import platform
import re
from pathlib import Path
from setuptools import find_packages, setup, Extension
# from setuptools.command.build_ext import build_ext
from setuptools.command.install import install
from setuptools.command.install_lib import install_lib
from setuptools.command.install_scripts import install_scripts
import shutil
import struct
import sys
from typing import List, Set
from wheel.bdist_wheel import bdist_wheel

# Inspired from:
# - https://pypi.org/project/cmake-setuptools/
# - https://stackoverflow.com/questions/42585210/extending-setuptools-extension-to-use-cmake-in-setup-py
# - https://github.com/TylerGubala/blenderpy/blob/master/setup.py

class ConanExtension(Extension):
    """
    setuptools.Extension for conan
    """
    def __init__(self, name):
        # don't invoke the original build_ext for this special extension
        super().__init__(name, sources=[])

class build_ext(build_ext_orig):

    def run(self):
        for ext in self.extensions:
            self.launch_conan(ext)
        super().run()

    def launch_conan(self, ext):

#         # example of cmake args
#         # config = 'Debug' if self.debug else 'Release'

        cwd = Path().absolute()

        output_dir = Path(self.get_finalized_command('build_py').build_lib)

        build_temp = Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        extdir = Path(self.get_ext_fullpath(ext.name))
        extdir.mkdir(parents=True, exist_ok=True)

        # self.spawn(["conan", "install", ".",
        #             "--build", "missing",
        #             "--profile:build", ".conan/profiles/gcc12",
        #             "--profile:host", ".conan/profiles/gcc12",
        #             ])
        # self.spawn(["conan", "build", "."])


        self.spawn(["pwd"])
        self.spawn(["ls", "-la", str(cwd)])
        self.spawn(["ls","-la", str(build_temp)])
        self.spawn(["conan", "install", str(cwd),
                    # "--install-folder={}".format(build_temp / 'build'),
                    "--build", "missing",
                    "--profile:build", ".conan/profiles/gcc12",
                    "--profile:host", ".conan/profiles/gcc12",
                    ])
        self.spawn(["ls", "-la"])
        self.spawn(["ls", "-la", "build"])
        self.spawn(["conan", "build", str(cwd), 
                # '--source-folder={}'.format(cwd),
                # '--build-folder={}'.format(build_temp / 'build'),
                # '--package-folder={}'.format(build_temp / 'package')
                ])
        self.spawn(["conan", "export-pkg", "--force", str(cwd)])
        # self.spawn(["conan", "imports", str(cwd),
        #         '--install-folder={}'.format(build_temp / 'build'),
        #         '--import-folder={}'.format(build_temp / 'package')
        #         ])

        # Once the binaries have been installed in the package dir, we copy the needed file to
        # output_dir for setuptools to install them.
        package_dir = build_temp / 'build/Release/src/swig_conan_test/'
        module_dir = output_dir / 'jupy'
        for py_file in glob.glob(str(package_dir / 'python' / '*.py')):
            shutil.copy2(py_file, str(module_dir))
        for lib_file in glob.glob(str(package_dir / 'lib' / '*.so*')):
            shutil.copy2(lib_file, str(module_dir), follow_symlinks=False)
        for lib_file in glob.glob(str(package_dir / '*.pyd')):
            shutil.copy2(lib_file, str(module_dir))
        # shutil.copy2(str(package_dir / 'README.md'), str(module_dir))


class CMakeExtension(Extension):
    """
    An extension to run the cmake build
    """

    def __init__(self, name, sources=[]):

        super().__init__(name = name, sources = sources)

class InstallCMakeLibsData(install_data):
    """
    Just a wrapper to get the install data into the egg-info
    """

    def run(self):
        """
        Outfiles are the libraries that were built using cmake
        """

        # There seems to be no other way to do this; I tried listing the
        # libraries during the execution of the InstallCMakeLibs.run() but
        # setuptools never tracked them, seems like setuptools wants to
        # track the libraries through package data more than anything...
        # help would be appriciated

        # self.outfiles = self.distribution.data_files
        print("InstallCMakeLibsData")
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            self.warn("current file: "+str(f))

class InstallCMakeLibs(install_lib):
    """
    Get the libraries from the parent distribution, use those as the outfiles
    Skip building anything; everything is already built, forward libraries to
    the installation step
    """

    def run(self):
        """
        Copy libraries from the bin directory and place them as appropriate
        """

        self.announce("Moving library files", level=3)
        print("InstallCMakeLibs")
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            self.warn("current file: "+str(f))
        # We have already built the libraries in the previous build_ext step

        self.skip_build = True

        bin_dir = ""
        # self.distribution.bin_dir

        # libs = [os.path.join(bin_dir, _lib) for _lib in 
        #         os.listdir(bin_dir) if 
        #         os.path.isfile(os.path.join(bin_dir, _lib)) and 
        #         os.path.splitext(_lib)[1] in [".dll", ".so"]
        #         and not (_lib.startswith("python") or _lib.startswith("bpy"))]

        # for lib in libs:

        #     shutil.move(lib, os.path.join(self.build_dir,
        #                                   os.path.basename(lib)))

        # Mark the libs for installation, adding them to 
        # distribution.data_files seems to ensure that setuptools' record 
        # writer appends them to installed-files.txt in the package's egg-info
        #
        # Also tried adding the libraries to the distribution.libraries list, 
        # but that never seemed to add them to the installed-files.txt in the 
        # egg-info, and the online recommendation seems to be adding libraries 
        # into eager_resources in the call to setup(), which I think puts them 
        # in data_files anyways. 
        # 
        # What is the best way?

        # self.distribution.data_files = [os.path.join(self.install_dir, 
        #                                              os.path.basename(lib))
        #                                 for lib in libs]

        # # Must be forced to run after adding the libs to data_files

        # self.distribution.run_command("install_data")

        super().run()

class InstallBlenderScripts(install_scripts):
    """
    Install the scripts available from the "version folder" in the build dir
    """

    def run(self):
        """
        Copy the required directory to the build directory and super().run()
        """

        self.announce("Moving scripts files", level=3)
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            self.warn("current file: "+str(f))

        # self.skip_build = True

        # bin_dir = self.distribution.bin_dir

        # scripts_dirs = [os.path.join(bin_dir, _dir) for _dir in
        #                 os.listdir(bin_dir) if
        #                 os.path.isdir(os.path.join(bin_dir, _dir))]

        # for scripts_dir in scripts_dirs:

        #     dst_dir = os.path.join(self.build_dir,
        #                            os.path.basename(scripts_dir))

        #     # Mostly in case of weird things happening during build
        #     if os.path.exists(dst_dir):
                
        #         if os.path.isdir(dst_dir): 

        #             shutil.rmtree(dst_dir)

        #         elif os.path.isfile(dst_dir):

        #             os.remove(dst_dir)

        #     # Copy the blender scripts directory

        #     shutil.copytree(scripts_dir,
        #                     os.path.join(self.build_dir,
        #                              os.path.basename(scripts_dir)))

        # # Mark the scripts for installation, adding them to 
        # # distribution.scripts seems to ensure that the setuptools' record 
        # # writer appends them to installed-files.txt in the package's egg-info

        # self.distribution.scripts = scripts_dirs

        super().run()

class CMakeBuild(bdist_wheel):
    """Create custom build 
    """

    def run(self):
        print("bdist_wheel.run? :)")
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            self.warn("current file: "+str(f))
        bdist_wheel.run(self)
        # super().run()
    # user_options = bdist_wheel.user_options + [
    #     ("bpy-prebuilt=", None, "Location of prebuilt bpy binaries"),
    #     ("bpy-cmake-configure-args=", None, "Custom CMake options")
    # ]

    # def initialize_options(self):
    #     """Allows for `cmake_extension_prebuild_dir`
    #     """

    #     super().initialize_options()
    #     self.bpy_prebuilt = None
    #     self.bpy_cmake_configure_args = None

class BuildCMakeExt(build_ext):
    """
    Builds using cmake instead of the python setuptools implicit build
    """
    # user_options = build_ext.user_options + [
    #     ("bpy-prebuilt=", None, "Location of prebuilt bpy binaries"),
    #     ("bpy-cmake-configure-args=", None, "Custom CMake options")
    # ]

    # def initialize_options(self):
    #     """Allows for `cmake_extension_prebuild_dir`
    #     """

    #     super().initialize_options()
    #     self.bpy_prebuilt = None
    #     self.bpy_cmake_configure_args = None

    # def finalize_options(self):
    #     """Grab options from previous call to `build`
    #     This is required to get the options passed into --build-options
    #     during bdist_wheel creation
    #     """

    #     super().finalize_options()

    #     self.set_undefined_options('bdist_wheel',
    #                                ('bpy_prebuilt', 'bpy_prebuilt'),
    #                                ('bpy_cmake_configure_args',
    #                                 'bpy_cmake_configure_args')
    #                                )

    def run(self):
        """
        Perform build_cmake before doing the 'normal' stuff
        """

        os.makedirs(str(pathlib.Path(self.build_temp).absolute()), 
                    exist_ok=True)

        print("BuildCMakeExt? :)")
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            self.warn("current file: "+str(f))
        for extension in self.extensions:

            extension_path = pathlib.Path(self.get_ext_fullpath(extension.name))

            if isinstance(extension,CMakeExtension):

                self.announce(f"Preparing the build environment for CMake "
                              f"extension: \"{extension.name}\"", level=3)

        super().run()

class BuildSDist(build_ext):

    def run(self):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            self.warn("current file: "+str(f))

class PrepareMetadataForBuildWheel(build_ext):

    def run(self):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            self.warn("current file: "+str(f))

setup(
    name='swig_conan_test',
    version='0.0.1',
    # packages=find_packages(),
    # packages=['swig_conan_test'],
    ext_modules=[CMakeExtension(name="swig_conan_test")],
    # ext_modules=[ConanExtension('swig_conan_test')],
    # include_package_data=True,
    cmdclass={
        # 'egg_info': egg_info,
        # 'sdist': sdist,
        # 'egg_info': egg_info,
        # 'check': check,
        # 'bdist_wheel': bdist_wheel,
        # 'build': build,
        # 'build_py': build_py,
        'build_ext': build_ext,
        'install': install,
        'install_lib': install_lib,
        # 'install_egg_info': install_egg_info,
        'install_scripts': install_scripts

        #   'bdist_wheel': CMakeBuild,
        #   'build_ext': BuildCMakeExt,
        #   'install_lib': InstallCMakeLibs,
        #   'install_scripts': InstallBlenderScripts

        #   'prepare_metadata_for_build_wheel': PrepareMetadataForBuildWheel,
        #   'build_sdist': BuildSDist,
        #   'install_data': InstallCMakeLibsData,
          },
    # cmdclass={
    #     'build_ext': build_ext,
    # }
)