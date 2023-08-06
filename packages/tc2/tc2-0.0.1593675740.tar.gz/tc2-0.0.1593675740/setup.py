# Copyright (c) 2017-present, Facebook, Inc.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import re
import sys
import sysconfig
import platform
import subprocess
from pathlib import Path

from setuptools import setup, Extension, find_namespace_packages
from setuptools.command.build_ext import build_ext
from setuptools.command.install_scripts import install_scripts
from distutils.version import LooseVersion
from setuptools.command.test import test as TestCommand


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: " +
                ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(
                re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.join(os.path.dirname(self.get_ext_fullpath(ext.name)), "tc2"))
        cmake_args = [
            # CMake sets the folders containing the libraries in the binaries RPATH upon build, so we can find them at run-time
            # Upon `install`, cmake clears the RPATH in the binaries, so they can use system-wide libraries (/usr/lib...)
            # However, if we do that, libraries installed with conda are lost (because they are not in system-wide directories)
            # Let's rather keep RPATH for all librairies outside of the build tree
            # See https://gitlab.kitware.com/cmake/community/-/wikis/doc/cmake/RPATH-handling#always-full-rpath
            '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=TRUE',
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
            '-DCMAKE_INSTALL_PREFIX=' + extdir,
            '-DPYTHON_EXECUTABLE=' + sys.executable,
            '-DPython3_ROOT_DIR=' + str(Path(sys.executable).parent.parent.absolute()),
            '-DPython3_FIND_STRATEGY=LOCATION' # ... even if we find a newer version somewhere else in the system
        ]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += [
                '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(
                    cfg.upper(), extdir)
            ]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get('CXXFLAGS', ''), self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(
            ['cmake', ext.sourcedir] + cmake_args,
            cwd=self.build_temp,
            env=env)
        subprocess.check_call(
            ['cmake', '--build', '.'] + build_args, cwd=self.build_temp)
        subprocess.check_call(
            ['cmake', '--build', '.', '--target', 'install'],
            cwd=self.build_temp)

# Find version number in __init__
init_str = Path("tc2/__init__.py").read_text()
match = re.search(r"^__version__ = \"(?P<version>[\w\.]+?)\"", init_str, re.MULTILINE)
assert match is not None, "Could not find version in tc2/__init__.py"
version = match.group("version")


setup(
    name='tc2',
    version=version,
    author='Facebook AI Research',
    author_email='xxxxx@fb.com',
    description='A fast and easy way to run StarCraft: Brood War as a Gym environment.',
    license='MIT',
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    ext_modules=[CMakeExtension('tc2lib')],
    cmdclass=dict(build_ext=CMakeBuild),
    install_requires=[
        'gym', 'numpy', 'pybind11',
        'requests', 'unzip-aes', # For tc2-setup
        'zstandard', # for cherryvis dump
        # And `apt-get install -y cmake libsdl2-dev libzmq3-dev`
    ],
    zip_safe=False,
    packages=find_namespace_packages(include=['*tc2*'], exclude=['*test*']),
    package_data={"hiplot": ["py.typed"]},
    scripts=['scripts/tc2-setup'],
)
