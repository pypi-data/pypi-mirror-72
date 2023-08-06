# Copyright (c) 2017-present, Facebook, Inc.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
project(tc2)
cmake_minimum_required(VERSION 3.10 FATAL_ERROR)

list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")
set(OPENBW_DIR "${PROJECT_SOURCE_DIR}/thirdparty/openbw")
set(OPENBW_ENABLE_UI ON CACHE BOOL "" FORCE)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON) #Required for OpenBW and thus for everything
set(BWAPI_INCLUDE_DIR "${PROJECT_SOURCE_DIR}/thirdparty/openbwapi/bwapi/include")
set(BWAPI_DIR "${CMAKE_CURRENT_BINARY_DIR}")
#TorchCraft's BWEnv uses find_library() for BWAPI_LIBRARY/BWAPIClient_LIBRARY
#which runs before they exist, so we pre-populate them here.
set(BWAPI_LIBRARY "BWAPILIB")
set(BWAPIClient_LIBRARY "${BWAPI_DIR}/lib/libBWAPIClient.a")
set(ZSTD_USE_STATIC_RUNTIME ON)
set(ZSTD_BUILD_PROGRAMS OFF)
set(ZSTD_LIBRARY libzstd_static)
set(ZSTD_INCLUDE_DIR "${PROJECT_SOURCE_DIR}/thirdparty/zstd/lib")
set(OPENBWAPI_BUILD_STATIC_LIBS ON CACHE BOOL "Build OpenBWAPI statically" FORCE)

find_package(Python3 COMPONENTS Interpreter Development NumPy)
message("Python3_FOUND: ${Python3_FOUND}")
message("Python3_Interpreter_FOUND: ${Python3_Interpreter_FOUND}")
message("Python3_EXECUTABLE: ${Python3_EXECUTABLE}")
message("Python3_INTERPRETER_ID: ${Python3_INTERPRETER_ID}")
message("Python3_STDLIB: ${Python3_STDLIB}")
message("Python3_STDARCH: ${Python3_STDARCH}")
message("Python3_SITELIB: ${Python3_SITELIB}")
message("Python3_SITEARCH: ${Python3_SITEARCH}")
message("Python3_Development_FOUND: ${Python3_Development_FOUND}")
message("Python3_INCLUDE_DIRS: ${Python3_INCLUDE_DIRS}")
message("Python3_LIBRARIES: ${Python3_LIBRARIES}")
message("Python3_LIBRARY_DIRS: ${Python3_LIBRARY_DIRS}")
message("Python3_RUNTIME_LIBRARY_DIRS: ${Python3_RUNTIME_LIBRARY_DIRS}")
message("Python3_VERSION: ${Python3_VERSION}")
message("Python3_NumPy_FOUND: ${Python3_NumPy_FOUND}")
message("Python3_NumPy_INCLUDE_DIRS: ${Python3_NumPy_INCLUDE_DIRS}")
message("Python3_NumPy_VERSION: ${Python3_NumPy_VERSION}")
set(PYBIND11_PYTHON_VERSION, "${Python3_VERSION}")
set(PYBIND11_INCLUDE_DIR "${Python3_INCLUDE_DIRS}")
set(PYTHON_INCLUDE_DIRS "${Python3_INCLUDE_DIRS}")

# Don't let PyBind try to find Python on its own (that's our job)
# See https://github.com/pybind/pybind11/blob/master/tools/FindPythonLibsNew.cmake
# See https://github.com/pybind/pybind11/blob/a6355b00f84d997a9ddcf209b6464447432be78a/tools/pybind11Tools.cmake
set(PYTHONLIBS_FOUND "${Python3_FOUND}")
set(PYTHON_MODULE_EXTENSION ".so") # Need this to vary by OS

add_subdirectory(thirdparty/fmt EXCLUDE_FROM_ALL)
add_subdirectory(thirdparty/glog EXCLUDE_FROM_ALL)
add_subdirectory(thirdparty/openbwapi EXCLUDE_FROM_ALL)
add_subdirectory(thirdparty/pybind EXCLUDE_FROM_ALL)
add_subdirectory(thirdparty/torchcraft EXCLUDE_FROM_ALL)
add_subdirectory(thirdparty/torchcraft/BWEnv EXCLUDE_FROM_ALL)
add_subdirectory(thirdparty/zstd/build/cmake EXCLUDE_FROM_ALL)
add_subdirectory(cpp)

add_dependencies(tc2lib BWEnv BWAPILauncher)
add_dependencies(BWEnv BWAPIClient)

# Ensure that tc2lib (The pybind module compiled from C++) is available for import
file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/__init__.py" "")
file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/cpp/__init__.py" "")

# Install `BWAPILauncher` binary
install(SCRIPT ${CMAKE_CURRENT_BINARY_DIR}/thirdparty/openbwapi/bwapi/BWAPILauncher/cmake_install.cmake)
