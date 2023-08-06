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
 
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include "pyclient.h"
#include "pyconstants.h"
#include "pyreplayer.h"
#include "pystate.h"

#include "../features/geometry.h"
#include "../features/features.h"
#include "../features/unitsfeatures.h"

namespace {

  inline std::vector<pybind11::array_t<float>> featurizePlainAll(torchcraft::State* state, std::vector<tc2::PlainFeatureType> featureTypes) {
    tc2::Rect bounds(0, 0, state->mapWidth(), state->mapHeight());
    std::vector<pybind11::array_t<float>> output;
    for (auto featureType : featureTypes) {
      auto featureData = tc2::featurizePlain(state, featureType, bounds);
      output.push_back(*(featureData.tensor.array));
    }    
    return output;
  }
  inline tc2::UnitFeatureData featurizeUnits(torchcraft::State* state, int playerId) {
    tc2::UnitStatFeaturizer featurizer;
    auto units = state->units[playerId];
    std::vector<torchcraft::Unit const*> unitPointers;
    for (auto& unit : units) { unitPointers.push_back(&unit); }
    return featurizer.extract(state, unitPointers);
  }
}

void init_tc2features(pybind11::module& m) {
  tc2::features::initialize();
  
  pybind11::class_<tc2::UnitFeatureData>(m, "UnitFeatureData")
    .def(pybind11::init<>())
    .def("ids", [](const tc2::UnitFeatureData& data) { return *(data.ids.array); })
    .def("positions", [](const tc2::UnitFeatureData& data) { return *(data.positions.array); })
    .def("data", [](const tc2::UnitFeatureData& data) { return *(data.data.array); });

  m.def("featurize_ground_height", [](torchcraft::State* state) { return featurizePlainAll(state, { tc2::PlainFeatureType::GroundHeight }); });
  m.def("featurize_walkability", [](torchcraft::State* state) { return featurizePlainAll(state, { tc2::PlainFeatureType::Walkability }); });
  m.def("featurize_buildability", [](torchcraft::State* state) { return featurizePlainAll(state, { tc2::PlainFeatureType::Buildability }); });
  m.def("featurize_fog", [](torchcraft::State* state) { return featurizePlainAll(state, { tc2::PlainFeatureType::FogOfWar }); });
  m.def("featurize_creep", [](torchcraft::State* state) { return featurizePlainAll(state, { tc2::PlainFeatureType::Creep }); });
  m.def("featurize_tall_doodad", [](torchcraft::State* state) { return featurizePlainAll(state, { tc2::PlainFeatureType::TallDoodad }); });
  m.def("featurize_ground_height_onehot", [](torchcraft::State* state) { return featurizePlainAll(state, { tc2::PlainFeatureType::OneHotGroundHeight }); });
  m.def("featurize_start_locations", [](torchcraft::State* state) { return featurizePlainAll(state, { tc2::PlainFeatureType::StartLocations }); });
  m.def("featurize_xygrid", [](torchcraft::State* state) { return featurizePlainAll(state, { tc2::PlainFeatureType::XYGrid }); });
  m.def("featurize_resources", [](torchcraft::State* state) { return featurizePlainAll(state, { tc2::PlainFeatureType::Resources }); });
  m.def("featurize_structures", [](torchcraft::State* state) { return featurizePlainAll(state, { tc2::PlainFeatureType::HasStructure }); });
  m.def("featurize_units", [](torchcraft::State* state, int playerId) { return featurizeUnits(state, playerId); });
  m.def("featurize_map_dynamic", [](torchcraft::State* state) { return featurizePlainAll(state, {
    tc2::PlainFeatureType::Creep,
    // Disabled temporarily for performance
    //tc2::PlainFeatureType::HasStructure, // Maybe doesn't work -- is all 0 on frame 0 (Expected if it counts resources);
    //tc2::PlainFeatureType::FogOfWar, // Crashes    
  }); });
  m.def("featurize_map_static", [](torchcraft::State* state) { return featurizePlainAll(state, {
    tc2::PlainFeatureType::Walkability,
    tc2::PlainFeatureType::Buildability,
    tc2::PlainFeatureType::OneHotGroundHeight,
    tc2::PlainFeatureType::StartLocations, // Didn't work at last check due to using pooling -- double check
    tc2::PlainFeatureType::XYGrid,
    tc2::PlainFeatureType::Resources, // Didn't work at last check due to using pooling -- double check
  }); });
}