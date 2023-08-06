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

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <torchcraft/state.h>

#define READPAIR(TYP, VAR) \
  [](TYP* self) { return pybind11::make_tuple(self->VAR[0], self->VAR[1]); }

#define WRITEPAIR(TYP, VAR, INNER)             \
  [](TYP* self, std::pair<INNER, INNER> VAR) { \
    self->VAR[0] = VAR.first;                  \
    self->VAR[1] = VAR.second;                 \
  }

#define RWPAIR(TYP, VAR, INNER) READPAIR(TYP, VAR), WRITEPAIR(TYP, VAR, INNER)

void init_state(pybind11::module& torchcraft) {
  using namespace torchcraft;
  pybind11::class_<State> state(torchcraft, "State");
  pybind11::class_<State::Position>(state, "Position")
      .def(pybind11::init<>())
      .def(pybind11::init<int, int>())
      .def_readwrite("x", &State::Position::x)
      .def_readwrite("y", &State::Position::y);

  pybind11::class_<State::PlayerInfo>(state, "PlayerInfo")
      .def(pybind11::init<>())
      .def("__repr__", [](State::PlayerInfo& self) {
        return fmt::format("Player #{} {} ({})",
          self.id,
          self.name,
          self.is_enemy ? "Enemy" : self.id < 0 ? "Neutral" : "Myself");
      })
      .def_readwrite("id", &State::PlayerInfo::id)
      .def_property(
          "race",
          [](State::PlayerInfo* self) { return self->race._to_integral(); },
          [](State::PlayerInfo* self, int val) {
            self->race = BW::Race::_from_integral(val);
          })
      .def_readwrite("name", &State::PlayerInfo::name)
      .def_readwrite("is_enemy", &State::PlayerInfo::is_enemy)
      .def_readwrite("has_left", &State::PlayerInfo::has_left);

  state
    .def(pybind11::init<>())
    .def_readwrite("lag_frames", &State::lag_frames)
    .def_property_readonly(
        "map_size",
        [](State* self) {
          return pybind11::make_tuple(self->map_size[0], self->map_size[1]);
        })
    .def_readwrite("ground_height_data", &State::ground_height_data)
    .def_readwrite("walkable_data", &State::walkable_data)
    .def_readwrite("buildable_data", &State::buildable_data)
    .def_readwrite("map_name", &State::map_name)
    .def_readwrite("map_title", &State::map_title)
    .def_readwrite("start_locations", &State::start_locations)
    .def_readwrite("player_info", &State::player_info)
    .def_readwrite("player_id", &State::player_id)
    .def_readwrite("neutral_id", &State::neutral_id)
    .def_readwrite("replay", &State::replay)
    .def_readwrite("deaths", &State::deaths)
    .def_readwrite("frame_from_bwapi", &State::frame_from_bwapi)
    .def_readwrite("game_ended", &State::game_ended)
    .def_readwrite("game_won", &State::game_won)
    .def_readwrite("img_mode", &State::img_mode)
    .def_property("screen_position", RWPAIR(State, screen_position, int))
    .def_readwrite("visibility", &State::visibility)
    .def_property("visibility_size", RWPAIR(State, visibility_size, int))
    .def_readwrite("image", &State::image)
    .def_property("image_size", RWPAIR(State, image_size, int))
    .def_readwrite("units", &State::units)
    .def_readwrite("all_units", &State::allUnits)
    .def_readonly("frame", &State::frame)
    .def("reset", &State::reset)
    .def("clone", [](State* self) { return new State(*self); });
}