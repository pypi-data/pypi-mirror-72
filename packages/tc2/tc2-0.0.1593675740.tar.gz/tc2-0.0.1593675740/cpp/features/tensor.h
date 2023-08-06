/*
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <stdexcept>

#include "tensortypes.h"

// Shim for the PyTorch C++ API
// The intent is to use TorchCraftAI's featurizers with minimal modification.
namespace torch {
  
  template <typename Value>
  class Tensor {
   public:
    // PyBind's numpy array type.
    // API is undocumented, but here's the source:
    // https://github.com/pybind/pybind11/blob/9bb3313162c0b856125e481ceece9d8faa567716/include/pybind11/numpy.h#L509
    std::shared_ptr<pybind11::array_t<Value>> array;    

   protected:
    std::vector<int64_t> indices;
    /// Throw an exception if this tensor hasn't been indexed into deep enough to map to a single value.
    void assertSingleValue() const;
    const Value& singleValue() const;
    Value& singleValue();
   public:
    bool defined() const;
    int64_t size(int64_t dimension) const;
    void fill_(Value filling);
    Tensor<Value> resize_(std::vector<int64_t> dimensions);
    void zero_() { fill_(0); }
    Tensor<Value> operator[](int64_t index) const;
    Tensor<Value> operator=(Value value);
    Tensor<Value> operator+=(Value value);
    operator Value() const;
  };

  template<typename T> Tensor<T> empty(std::vector<ssize_t> dimensions);
  template<typename T> Tensor<T> zeros(std::vector<ssize_t> dimensions);

  template<typename Value, int64_t B> struct TensorAccessorBase : public Tensor<Value> {
    TensorAccessorBase(Tensor<Value> t): Tensor<Value>(t) {}
    operator Tensor<Value>() const {
      return Tensor<Value>(*this);
    }
  };
  typedef Tensor<float> TensorFloat;
  typedef Tensor<int32_t> TensorInt32;
  typedef Tensor<int64_t> TensorInt64;
} // namespace torch

// Definitions

namespace torch {

  namespace {
    int64_t maybeWrapDimension(int64_t dimension, int64_t dimensionCountAfter) {
      if (dimensionCountAfter <= 0) {
        dimensionCountAfter = 1; // this will make range [-1, 0]
      }
      int64_t min = -dimensionCountAfter;
      int64_t max = dimensionCountAfter - 1;
      if (dimension < min || dimension > max) {
        throw std::runtime_error("Dimension out of range");
      }
      if (dimension < 0) dimension += dimensionCountAfter;
      return dimension;
    }
  }

  template<typename Value>
  void Tensor<Value>::assertSingleValue() const {
    if (indices.size() < array->ndim()) {
      throw std::runtime_error("Didn't index deep enough into Tensor before converting to data type");
    }
  }

  template<typename Value>
  const Value& Tensor<Value>::singleValue() const {
    assertSingleValue();
    // Trying to call a variadic function using a dynamic number of arguments :(
    switch(indices.size()) {
      case 0: return *array->data(0);
      case 1: return *array->data(indices[0]);
      case 2: return *array->data(indices[0], indices[1]);
      case 3: return *array->data(indices[0], indices[1], indices[2]);
      case 4: return *array->data(indices[0], indices[1], indices[2], indices[3]);
      case 5: return *array->data(indices[0], indices[1], indices[2], indices[3], indices[4]);
      case 6: return *array->data(indices[0], indices[1], indices[2], indices[3], indices[4], indices[5]);
      default: throw std::runtime_error("The switch statement for calling array->data with variadic arguments needs more cases");
    }
  }

  template<typename Value>
  Value& Tensor<Value>::singleValue() {
    assertSingleValue();
    // Trying to call a variadic function using a dynamic number of arguments :(
    switch(indices.size()) {
      case 0: return *array->mutable_data(0);
      case 1: return *array->mutable_data(indices[0]);
      case 2: return *array->mutable_data(indices[0], indices[1]);
      case 3: return *array->mutable_data(indices[0], indices[1], indices[2]);
      case 4: return *array->mutable_data(indices[0], indices[1], indices[2], indices[3]);
      case 5: return *array->mutable_data(indices[0], indices[1], indices[2], indices[3], indices[4]);
      case 6: return *array->mutable_data(indices[0], indices[1], indices[2], indices[3], indices[4], indices[5]);
      default: throw std::runtime_error("The switch statement for calling array->mutable_data with variadic arguments needs more cases");
    }
  }

  template<typename Value>
  bool Tensor<Value>::defined() const {
    return bool(array);
  }

  template<typename Value>
  int64_t Tensor<Value>::size(int64_t dimension) const {
    return array->shape(dimension);
  }

  template<typename Value>
  void Tensor<Value>::fill_(Value value) {
    // TODO: Speed up by vectorizing
    // This could probably be supported by invoking NumPy C API methods on the raw NumPy store:
    // https://github.com/pybind/pybind11/blob/9424d5d27731e3c7333e7295b545ee8722054c73/include/pybind11/pytypes.h#L1284
    auto size = array->size();
    auto data = array->mutable_data();
    for (pybind11::ssize_t i = 0; i < size; ++i) {
      data[i] = value;
    }
  }

  template<typename Value>
  Tensor<Value> Tensor<Value>::resize_(std::vector<int64_t> dimensions) {
    array->resize(dimensions, false);
    return *this;
  }

  template<typename Value>
  Tensor<Value> Tensor<Value>::operator[](int64_t index) const {
    Tensor<Value> output(*this);
    output.indices.push_back(index);
    return output;
  }

  template<typename Value>
  Tensor<Value> Tensor<Value>::operator=(Value value) { 
    assertSingleValue();
    singleValue() = value;
    return *this;
  }

  template<typename Value>
  Tensor<Value> Tensor<Value>::operator+=(Value value) {      
    assertSingleValue();
    singleValue() += value;
    return *this;
  }

  template<typename Value>
  Tensor<Value>::operator Value() const {
    assertSingleValue();
    return Value(singleValue());
  }

  template<typename Value>
  Tensor<Value> empty(std::vector<ssize_t> dimensions) {
    Tensor<Value> output;
    pybind11::array::ShapeContainer shapeContainer(dimensions);
    output.array = std::make_shared<pybind11::array_t<Value>>(shapeContainer);
    output.array->resize(dimensions);
    return output;
  }

  template<typename Value>
  Tensor<Value> zeros(std::vector<ssize_t> dimensions) {
    Tensor<Value> output = empty<Value>(dimensions);
    output.fill_(0);
    return output;
  }
} // namespace torch