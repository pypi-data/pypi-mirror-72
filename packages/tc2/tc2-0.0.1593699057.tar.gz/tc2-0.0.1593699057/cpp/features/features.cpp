/*
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include "features.h"

//#include "state.h"

#include <glog/logging.h>

namespace tc2 {

// Feature extractor proto-types
namespace featureimpl {

// for user features
void noop(torch::TensorFloat, tc::State const*, Rect const&) {}
// mapfeatures.cpp
void extractGroundHeight(torch::TensorFloat, tc::State const*, Rect const&);
void extractWalkability(torch::TensorFloat, tc::State const*, Rect const&);
void extractOneHotGroundHeight(torch::TensorFloat, tc::State const*, Rect const&);
void extractBuildability(torch::TensorFloat, tc::State const*, Rect const&);
void extractTallDoodad(torch::TensorFloat, tc::State const*, Rect const&);
void extractStartLocations(torch::TensorFloat, tc::State const*, Rect const&);
void extractXYGrid(torch::TensorFloat, tc::State const*, Rect const&);
void extractResources(torch::TensorFloat, tc::State const*, Rect const&);
void extractHasStructure(torch::TensorFloat, tc::State const*, Rect const&);
void extractFogOfWar(torch::TensorFloat, tc::State const*, Rect const&);
void extractCreep(torch::TensorFloat, tc::State const*, Rect const&);

} // namespace featureimpl

namespace {

struct PlainFeatureInfo {
  using Function = std::function<void(torch::TensorFloat, tc::State const*, Rect const&)>;

  char const* name;
  Function fn;
  int numChannels;
};

std::unordered_map<int, PlainFeatureInfo>& featureRegistry() {
  static std::unordered_map<int, PlainFeatureInfo> reg;
  return reg;
}

int featureTypeValue(AnyFeatureType type) {
  int value;
  type.match(
      [&](PlainFeatureType t) { value = static_cast<int>(t); },
      [&](CustomFeatureType t) { value = static_cast<int>(t); });
  return value;
}

} // namespace

namespace features {

void initialize() {
#define ADD_PLAIN_FEATURE(NAME, FN, NUM_CHANNELS)                             \
  do {                                                                        \
    featureRegistry()[static_cast<int>(PlainFeatureType::NAME)].name = #NAME; \
    featureRegistry()[static_cast<int>(PlainFeatureType::NAME)].fn = FN;      \
    featureRegistry()[static_cast<int>(PlainFeatureType::NAME)].numChannels = \
        NUM_CHANNELS;                                                         \
  } while (0)

  ADD_PLAIN_FEATURE(GroundHeight, &featureimpl::extractGroundHeight, 1);
  ADD_PLAIN_FEATURE(
      OneHotGroundHeight, &featureimpl::extractOneHotGroundHeight, 4);
  ADD_PLAIN_FEATURE(Walkability, &featureimpl::extractWalkability, 1);
  ADD_PLAIN_FEATURE(Buildability, &featureimpl::extractBuildability, 1);
  ADD_PLAIN_FEATURE(FogOfWar, &featureimpl::extractFogOfWar, 1);
  ADD_PLAIN_FEATURE(Creep, &featureimpl::extractCreep, 1);
  ADD_PLAIN_FEATURE(StartLocations, &featureimpl::extractStartLocations, 1);
  ADD_PLAIN_FEATURE(XYGrid, &featureimpl::extractXYGrid, 2);
  ADD_PLAIN_FEATURE(TallDoodad, &featureimpl::extractTallDoodad, 1);
  ADD_PLAIN_FEATURE(Resources, &featureimpl::extractResources, 1);
  ADD_PLAIN_FEATURE(HasStructure, &featureimpl::extractHasStructure, 1);

#undef ADD_PLAIN_FEATURE
}

} // namespace features

bool FeatureDescriptor::operator==(FeatureDescriptor const& other) const {
  int value1 = -1;
  type.match(
      [&](PlainFeatureType t) { value1 = static_cast<int>(t); },
      [&](CustomFeatureType t) { value1 = static_cast<int>(t); });
  int value2 = -1;
  other.type.match(
      [&](PlainFeatureType t) { value2 = static_cast<int>(t); },
      [&](CustomFeatureType t) { value2 = static_cast<int>(t); });

  return value1 == value2 && name == other.name &&
      numChannels == other.numChannels;
}

int FeatureData::numChannels() const {
  if (tensor.defined()) {
    return tensor.size(0);
  }
  return 0;
}

Rect FeatureData::boundingBox() const {
  return Rect(offset, tensor.size(2) * scale, tensor.size(1) * scale);
}

FeatureData featurizePlain(
    tc::State const* state,
    PlainFeatureType type,
    Rect boundingBox) {
  if (boundingBox.empty()) {
    boundingBox = getRect(state);
  }

  auto& reg = featureRegistry();

  Rect crop = boundingBox;
  int nchannels = 0;
  //for (auto& type : types) 
  {
    auto it = reg.find(static_cast<int>(type));
    if (it == reg.end()) {
      throw std::runtime_error(
          "Unknown feature with ID " + std::to_string(static_cast<int>(type)));
    }
    auto& info = it->second;

    int nchan = info.numChannels;
    if (nchan < 0) {
      throw std::runtime_error("Cannot extract variable-length feature");
    }
    nchannels += nchan;
  }

  FeatureData ret;
  ret.tensor = torch::zeros<float>({nchannels, crop.height(), crop.width()});
  ret.scale = 1;
  ret.offset.x = crop.left();
  ret.offset.y = crop.top();
  // for (auto& type : types)
  {
    auto it = reg.find(static_cast<int>(type));
    assert(it != reg.end()); // ensured in loop above
    auto& info = it->second;

    int nchan = info.numChannels;
    info.fn(ret.tensor, state, crop);
    ret.desc.emplace_back(type, info.name, nchan);
  }
  return ret;
}

} // namespace tc2
