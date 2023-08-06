/*
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include "game.h"
#include "utils.h"

#ifndef WITHOUT_POSIX
#include <sys/stat.h>
#include <unistd.h>
#endif

#include "fsutils.h"

#include <fmt/format.h>
#include <glog/logging.h>

namespace tc2 {

GameMultiPlayer::GameMultiPlayer(
    GameOptions const& gameOptions,
    GamePlayerOptions const& player0,
    GamePlayerOptions const& player1) {
#ifdef WITHOUT_POSIX
  throw std::runtime_error("Not available for windows");
#else
  process0_ = std::make_shared<OpenBwProcess>(std::vector<EnvVar>{
      {"OPENBW_ENABLE_UI",
       gameOptions.gui() ? "1" : "0",
       gameOptions.gui()},
      {"OPENBW_LAN_MODE", "FILE", true},
      {"OPENBW_FILE_READ", pipes_.pipe0, true},
      {"OPENBW_FILE_WRITE", pipes_.pipe1, true},
      {"BWAPI_CONFIG_AUTO_MENU__AUTO_MENU", "LAN", true},
      {"BWAPI_CONFIG_AUTO_MENU__GAME_TYPE",
       gameTypeName(gameOptions.gametype()),
       true},
      {"BWAPI_CONFIG_AUTO_MENU__MAP", gameOptions.map(), true},
      {"BWAPI_CONFIG_AUTO_MENU__RACE", player0.race(), true},
      {"BWAPI_CONFIG_AUTO_MENU__CHARACTER_NAME",
       player0.name().empty() ? "Agent" : player0.name(), true},
      {"BWAPI_CONFIG_AUTO_MENU__SAVE_REPLAY", gameOptions.replaypath(), true},
  });
  process1_ = std::make_shared<OpenBwProcess>(std::vector<EnvVar>{
      {"OPENBW_ENABLE_UI", "0", true},
      {"OPENBW_LAN_MODE", "FILE", true},
      {"OPENBW_FILE_READ", pipes_.pipe1, true},
      {"OPENBW_FILE_WRITE", pipes_.pipe0, true},
      {"BWAPI_CONFIG_AUTO_MENU__AUTO_MENU", "LAN", true},
      {"BWAPI_CONFIG_AUTO_MENU__GAME_TYPE",
       gameTypeName(gameOptions.gametype()),
       true},
      {"BWAPI_CONFIG_AUTO_MENU__MAP", gameOptions.map(), true},
      {"BWAPI_CONFIG_AUTO_MENU__RACE", player1.race(), true},
      {"BWAPI_CONFIG_AUTO_MENU__CHARACTER_NAME",
       player1.name().empty() ? "Enemy" : player1.name(), true},
  });
#endif // WITHOUT_POSIX
}

std::shared_ptr<torchcraft::Client> GameMultiPlayer::makeClient0() {
  return makeTorchCraftClient(process0_, torchcraft::Client::Options());
}

std::shared_ptr<torchcraft::Client> GameMultiPlayer::makeClient1() {
  return makeTorchCraftClient(process1_, torchcraft::Client::Options());
}

} // namespace tc2