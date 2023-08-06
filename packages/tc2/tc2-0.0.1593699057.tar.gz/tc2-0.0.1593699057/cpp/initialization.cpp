/*
 * Copyright (c) 2015-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 *
 * This is pretty much equivalent to the main executable, but instead of
 * connecting to a server we'll spin it up ourselves and play against another
 * bot.
 */

#include "initialization.h"
 
#include <csignal>
#include <glog/logging.h>
#include <torchcraft/client.h>
#include "forkserver.h"
#include "openbwprocess.h"

namespace tc2 {
  namespace {
    bool tc2initialized = false;
    
    void onSignalInt(int) {
      VLOG(0) << "SIGINT caught, shutting down...";
      VLOG(0) << "(press CTRL+C again to force exit now)";
      OpenBwProcess::preventFurtherProcesses();
      ForkServer::endForkServer();
      std::signal(SIGINT, SIG_DFL);
    }
  }
  void tc2initialize() {
    if (tc2initialized) return;
    tc2initialized = true;
    google::InitGoogleLogging("tc2");
    ForkServer::startForkServer();
    std::signal(SIGINT, onSignalInt);
  }
}