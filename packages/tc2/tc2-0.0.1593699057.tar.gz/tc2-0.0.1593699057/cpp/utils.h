/*
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include "str.h"

namespace tc2 {
inline void setCurrentThreadName(std::string const& name) {
#ifdef __APPLE__
  pthread_setname_np(name.c_str());
#elif __linux__
  pthread_setname_np(pthread_self(), name.c_str());
#else
  // Unsupported
#endif
}
}