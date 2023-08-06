# Copyright (c) 2017-present, Facebook, Inc.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

file(GLOB_RECURSE TC2_CPP_FILES *.cpp)
list(REMOVE_ITEM TC2_CPP_FILES ${CMAKE_CURRENT_SOURCE_DIR}/tc2main.cpp)
list(REMOVE_ITEM TC2_CPP_FILES ${CMAKE_CURRENT_SOURCE_DIR}/tc2lib.cpp)
list(APPEND TC2_INCLUDES
  "${CMAKE_SOURCE_DIR}/thirdparty/cereal/include"
  "${CMAKE_SOURCE_DIR}/thirdparty/prettyprint"
  "${CMAKE_SOURCE_DIR}/thirdparty/variant/include")
list(APPEND TC2LIB_LIBRARIES
  fmt
  glog
  ${PYTHON_LIBRARIES}
  pybind11
  torchcraft)
project(tc2lib)
pybind11_add_module(tc2lib "${TC2_CPP_FILES}" tc2lib.cpp)
target_include_directories(tc2lib SYSTEM PRIVATE "${TC2_INCLUDES}")
target_link_libraries(tc2lib PRIVATE "${TC2LIB_LIBRARIES}")
