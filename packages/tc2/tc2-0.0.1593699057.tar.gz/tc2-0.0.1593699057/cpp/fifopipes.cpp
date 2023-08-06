/*
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include "fifopipes.h"
#include "fsutils.h"
#include <glog/logging.h>

#ifndef WITHOUT_POSIX
#include <sys/stat.h>
#include <unistd.h>
#endif

namespace tc2 {

FifoPipes::FifoPipes() {
#ifndef WITHOUT_POSIX
  root_ = mktempd();
  pipe0 = root_ + "/0";
  pipe1 = root_ + "/1";
  if (mkfifo(pipe0.c_str(), 0666) != 0) {
    LOG(ERROR) << "Cannot create named pipe at " << pipe0;
    rmrf(root_);
    throw std::system_error(errno, std::system_category());
  }
  if (mkfifo(pipe1.c_str(), 0666) != 0) {
    LOG(ERROR) << "Cannot create named pipe at " << pipe1;
    rmrf(root_);
    throw std::system_error(errno, std::system_category());
  }
#else
  throw std::runtime_error("Not available for Windows");
#endif // !WITHOUT_POSIX
}

FifoPipes::~FifoPipes() {
#ifndef WITHOUT_POSIX
  rmrf(root_);
#endif // !WITHOUT_POSIX
}

} // namespace tc2