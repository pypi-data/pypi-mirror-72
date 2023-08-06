/*
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include "forkserver.h"
#include "game.h"

namespace tc2 {

GameSinglePlayer::GameSinglePlayer(
    const GameOptions& gameOptions,
    const GamePlayerOptions& player0,
    const GamePlayerOptions& player1) {      
  
 auto envVars = std::vector<EnvVar>{
      {"BWAPI_CONFIG_AUTO_MENU__GAME_TYPE",
       gameTypeName(gameOptions.gametype()),
       true},
      {"BWAPI_CONFIG_AUTO_MENU__SAVE_REPLAY", gameOptions.replaypath(), true},
      {"BWAPI_CONFIG_AUTO_MENU__MAP", gameOptions.map(), true},
      {"BWAPI_CONFIG_AUTO_MENU__RACE", player0.race(), true},
      {"OPENBW_ENABLE_UI",
       gameOptions.gui() ? "1" : "0",
       gameOptions.gui()}};
       
  if (!player0.name().empty()) {
    envVars.push_back({"BWAPI_CONFIG_AUTO_MENU__CHARACTER_NAME", player0.name(), true});
  }
  
  if (player1.race() != "") {
    envVars.push_back({"BWAPI_CONFIG_AUTO_MENU__ENEMY_RACE", player1.race(), true});
  }
  process_ = std::make_shared<OpenBwProcess>(std::move(envVars));
}

std::shared_ptr<torchcraft::Client> GameSinglePlayer::makeClient0() const {
  return makeTorchCraftClient(process_, torchcraft::Client::Options());
}

} // namespace tc2