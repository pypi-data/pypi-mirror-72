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

#pragma once

#include "../game.h"
#include "../initialization.h"
#include "../openbwprocess.h"

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include "pyclient.h"
#include "pyconstants.h"
#include "pyreplayer.h"
#include "pystate.h"
#include "pyfeatures.h"

using namespace pybind11::literals;

void setPaths(std::string const& bwenv, std::string const& bwapilauncher, std::string const& mpq) {
  if (!bwenv.empty()) {
    tc2::OpenBwProcess::bwenv.paths = {bwenv};
  }
  if (!bwapilauncher.empty()) {
    tc2::OpenBwProcess::bwapilauncher.paths = {bwapilauncher};
  }
  if (!mpq.empty()) {
    tc2::OpenBwProcess::mpqFolder = mpq;
  }
}

/// tc2lib is the C++ API providing access to OpenBW
PYBIND11_MODULE(tc2lib, m) {
  m.doc() = R"pbdoc(
      tc2lib documentation
  )pbdoc";
#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif

  // TorchCraft bindings
  tc2::tc2initialize();
  torchcraft::init();
  init_replayer(m);
  init_constants(m);
  init_state(m);
  init_client(m);
  init_tc2features(m);

  m.def("set_paths",
    &setPaths,
    pybind11::arg("bwenv") = "",
    pybind11::arg("bwapilauncher") = "",
    pybind11::arg("mpq") = "",
    "Sets various paths (bwenv, bwapilauncher, mpq)"
  );

  // GameType
  // StarCraft game mode
  pybind11::enum_<tc2::GameType>(m, "GameType")
    .value("Melee", tc2::GameType::Melee)
    .value("UseMapSettings", tc2::GameType::UseMapSettings)
    .export_values();

  // GamePlayerOptions
  // Specifies options for a specific player
  pybind11::class_<tc2::GamePlayerOptions>(m, "GamePlayerOptions")
    .def(pybind11::init<>())
    .def_readwrite("name", &tc2::GamePlayerOptions::name_)
    .def_readwrite("race", &tc2::GamePlayerOptions::race_);

  // GameOptions
  // Settings for StarCraft game operation and mode
  pybind11::class_<tc2::GameOptions>(m, "GameOptions")
    .def(pybind11::init<>())
    .def_readwrite("map", &tc2::GameOptions::map_)
    .def_readwrite("replaypath", &tc2::GameOptions::replaypath_)
    .def_readwrite("gui", &tc2::GameOptions::gui_)
    .def_readwrite("gametype", &tc2::GameOptions::gametype_)
    .def("set_map", &tc2::GameOptions::set_map)
    .def("get_map", &tc2::GameOptions::get_map)
    .def("set_replaypath", &tc2::GameOptions::set_replaypath)
    .def("get_replaypath", &tc2::GameOptions::get_replaypath)
    .def("set_gui", &tc2::GameOptions::set_gui)
    .def("get_gui", &tc2::GameOptions::get_gui)
    .def("set_gametype", &tc2::GameOptions::set_gametype)
    .def("get_gametype", &tc2::GameOptions::get_gametype);

  // GameSinglePlayer
  // Runs single-player (built-in opponent) games
  pybind11::class_<tc2::GameSinglePlayer>(m, "GameSinglePlayer")
    .def(pybind11::init<
      const tc2::GameOptions&,
      const tc2::GamePlayerOptions&,
      const tc2::GamePlayerOptions&>())
    .def("make_client0", &tc2::GameSinglePlayer::makeClient0, pybind11::return_value_policy::move);

  // GameMultiPlayer
  // Runs multi-player (controllable opponent) games
  pybind11::class_<tc2::GameMultiPlayer>(m, "GameMultiPlayer")
    .def(pybind11::init<
      const tc2::GameOptions&,
      const tc2::GamePlayerOptions&,
      const tc2::GamePlayerOptions&>())
    .def("make_client0", &tc2::GameMultiPlayer::makeClient0, pybind11::return_value_policy::move)
    .def("make_client1", &tc2::GameMultiPlayer::makeClient1, pybind11::return_value_policy::move);
}

