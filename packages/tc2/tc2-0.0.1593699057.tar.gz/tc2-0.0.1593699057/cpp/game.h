/*
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#pragma once

#include "arguments.h"
#include "fifopipes.h"
#include "initialization.h"
#include "openbwprocess.h"

#include <torchcraft/client.h>

#include <memory>
#include <string>

namespace tc2 {

enum GameType {
  Melee,
  UseMapSettings,
};

struct GameOptions {
  GameOptions() {};
  TC2_ARG(std::string, map);
  TC2_ARG(std::string, replaypath);
  TC2_ARG(bool, gui) = false;
  TC2_ARG(GameType, gametype) = GameType::UseMapSettings;
};

struct GamePlayerOptions {
  GamePlayerOptions(): race_("") {};
  TC2_ARG(std::string, race);
  TC2_ARG(std::string, name);
};

class GameMultiPlayer {
 public:
  GameMultiPlayer(
      const GameOptions& gameOptions,
      const GamePlayerOptions& player0,
      const GamePlayerOptions& player1);

  std::shared_ptr<torchcraft::Client> makeClient0();
  std::shared_ptr<torchcraft::Client> makeClient1();

 protected:
  FifoPipes pipes_;
  std::shared_ptr<OpenBwProcess> process0_;
  std::shared_ptr<OpenBwProcess> process1_;
};

class GameSinglePlayer {
 public:
  GameSinglePlayer(
      const GameOptions& gameOptions,
      const GamePlayerOptions& player0,
      const GamePlayerOptions& player1);
  GameSinglePlayer(GameSinglePlayer&&) = default;

  std::shared_ptr<torchcraft::Client> makeClient0() const;

 protected:
  std::shared_ptr<OpenBwProcess> process_;
  GameSinglePlayer() = default;
};


inline char const* gameTypeName(GameType type) {
  switch (type) {
    case GameType::Melee:
      return "MELEE";
    case GameType::UseMapSettings:
      return "USE_MAP_SETTINGS";
    default:
      break;
  }
  throw std::runtime_error("Unknown game type");
};

int constexpr kSelfPlayTimeoutMs = 60000;

inline std::shared_ptr<torchcraft::Client> makeTorchCraftClient(
    std::shared_ptr<OpenBwProcess> process,
    torchcraft::Client::Options opts) {

  auto client = std::make_shared<torchcraft::Client>();
  if (!process->connect(client.get(), kSelfPlayTimeoutMs)) {
    throw std::runtime_error(
        std::string("Error establishing connection: ") + client->error());
  }

  // Perform handshake
  std::vector<std::string> upd;
  if (!client->init(upd, opts)) {
    throw std::runtime_error(
        std::string("Error initializing connection: ") + client->error());
  }

  return client;
}


} // namespace tc2
