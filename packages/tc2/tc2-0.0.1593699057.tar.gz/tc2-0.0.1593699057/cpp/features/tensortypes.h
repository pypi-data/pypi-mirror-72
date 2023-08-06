/*
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#pragma once

// Shim for the PyTorch C++ API
namespace torch {
  constexpr int kI32 = 0;
  constexpr int kI64 = 1;
  constexpr int kF32 = 1;
}