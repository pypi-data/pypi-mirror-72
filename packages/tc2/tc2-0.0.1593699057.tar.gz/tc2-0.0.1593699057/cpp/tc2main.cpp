/*
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 *
 * This is pretty much equivalent to the main executable, but instead of
 * connecting to a server we'll spin it up ourselves and play against another
 * bot.
 */

#include "game.h"

void demo() {
  using namespace tc2;
  GameOptions optionsGame;
  GamePlayerOptions optionsPlayer0;
  GamePlayerOptions optionsPlayer1;
  GameSinglePlayer game(optionsGame, optionsPlayer0, optionsPlayer1);
}

int main (int argc, char* argv[]) {
  demo();
}
