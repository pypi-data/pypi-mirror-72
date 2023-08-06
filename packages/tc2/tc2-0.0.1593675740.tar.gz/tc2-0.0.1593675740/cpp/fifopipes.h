/*
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#pragma once

#include <string>

namespace tc2 {
struct FifoPipes {
  std::string pipe0;
  std::string pipe1;

  FifoPipes();
  ~FifoPipes();

 private:
  std::string root_;
};
} // namespace tc2