/*
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include "unitsfeatures.h"

#include <algorithm>
#include <cassert>
#include <mutex>

namespace tc2 {

int constexpr UnitTypeFeaturizer::kNumUnitTypes;
int constexpr UnitFlagsFeaturizer::kNumUnitFlags;
int constexpr UnitStatFeaturizer::kNumChannels;

UnitFeatureData UnitAttributeFeaturizer::extract(
    tc::State const* state,
    std::vector<tcr::Unit const*> const& units,
    Rect const& boundingBox) {
  UnitFeatureData data;
  if (boundingBox.empty()) {
    data.boundingBox = getRect(state);
  } else {
    data.boundingBox = boundingBox;
  }

  data.ids = torch::zeros<int32_t>({int(units.size())});
  data.positions = torch::zeros<int32_t>({int(units.size()), 2});
  data.data = torch::zeros<float>({int(units.size()), numChannels});
  if (units.empty()) {
    return data;
  }

  FeaturePositionMapper mapper(data.boundingBox, getRect(state));
  auto& jr = *jitter.get();
  auto ai = data.ids;
  auto ap = data.positions;
  auto ad = data.data;
  int n = 0;
  for (auto& unit : units) {
    // Determine resulting position by jittering and mapping to desired bounding
    // box.
    auto pos = mapper(jr(unit));
    if (pos.x >= 0) {
      ai[n] = unit->id;
      ap[n][0] = pos.y;
      ap[n][1] = pos.x;
      extractUnit(ad[n], unit);
      n++;
    }
  }

  if (n > 0) {
    data.positions.resize_({n, data.positions.size(1)});
    data.data.resize_({n, data.data.size(1)});
  } else {
    // undefined means empty
    data.positions = torch::TensorInt32();
    data.data = torch::TensorFloat();
  }
  return data;
}

UnitFeatureData UnitAttributeFeaturizer::extract(
    tc::State const* state,
    Rect const& boundingBox) {
  auto units = state->allUnits;
  std::vector<torchcraft::Unit const*> unitPointers(units.size());
  std::copy(units.begin(), units.end(), std::back_inserter(unitPointers));
  return extract(state, unitPointers, boundingBox);
}

UnitFeatureData UnitAttributeFeaturizer::extract(
    tc::State const* state,
    UnitFilter filter,
    Rect const& boundingBox) {
  auto const& src = state->allUnits;
  std::vector<tcr::Unit const*> units(src.size());
  auto it = std::copy_if(src.begin(), src.end(), units.begin(), filter);
  units.resize(std::distance(units.begin(), it));
  return extract(state, units, boundingBox);
}

FeatureData UnitAttributeFeaturizer::toSpatialFeature(UnitFeatureData const& data, SubsampleMethod pooling) const {
  FeatureData ret;
  toSpatialFeature(&ret, data, pooling);
  return ret;
}

void UnitAttributeFeaturizer::toSpatialFeature(FeatureData* dest, UnitFeatureData const& data, SubsampleMethod pooling) const {
  if (data.data.defined() && int(data.data.size(1)) != numChannels) {
    throw std::runtime_error(
        "Found wrong number of channels. Wrong data instance?");
  }

  if (!dest->tensor.defined()) {
    dest->tensor = torch::zeros<float>(
        {numChannels, data.boundingBox.height(), data.boundingBox.width()});
  } else {
    dest->tensor.resize_(
        {numChannels, data.boundingBox.height(), data.boundingBox.width()});
    dest->tensor.zero_();
  }
  dest->desc.clear();
  dest->desc.emplace_back(type, name, numChannels);
  dest->scale = 1;
  dest->offset.x = data.boundingBox.left();
  dest->offset.y = data.boundingBox.top();

  if (!data.positions.defined() || !data.data.defined()) {
    return;
  }

  auto numEntries = int(data.data.size(0));
  auto racc = dest->tensor;
  auto pacc = const_cast<torch::TensorInt32&>(data.positions);
  auto dacc = const_cast<torch::TensorFloat&>(data.data);
  for (auto i = 0; i < numEntries; i++) {
    auto y = pacc[i][0];
    auto x = pacc[i][1];
    auto srcit = dacc[i];
    if (pooling == SubsampleMethod::Sum) {
      for (auto j = 0; j < numChannels; j++) {
        racc[j][y][x] += srcit[j];
      }
    } else if (pooling == SubsampleMethod::Max) {
      for (auto j = 0; j < numChannels; j++) {
        racc[j][y][x] = std::max(racc[j][y][x], srcit[j]);
      }
    } else {
      throw std::runtime_error("Unsupported subsample method");
    }
  }
}

FeatureData UnitTypeFeaturizer::toOneHotSpatialFeature(
    UnitFeatureData const& data,
    int unitValueOffset,
    std::unordered_map<int, int> const& channelValues) const {
  if (data.data.defined() && int(data.data.size(1)) != 1) {
    throw std::runtime_error(
        "toOneHotSpatialFeature only works with single channel features.");
  }

  // The number of specified one-hot values +1 for 'other'
  auto numOneHotChannels = int(channelValues.size() + 1);

#ifndef NDEBUG
  // Verify that the assigned channel numbers match feature tensor size
  for (auto const& channelVal : channelValues) {
    assert(channelVal.second < numOneHotChannels);
  }
#endif // NDEBUG

  FeatureData dest;
  dest.tensor = torch::zeros<float>(
      {numOneHotChannels, data.boundingBox.height(), data.boundingBox.width()});
  dest.desc.emplace_back(type, name, numOneHotChannels);
  dest.scale = 1;
  dest.offset.x = data.boundingBox.left();
  dest.offset.y = data.boundingBox.top();

  if (!data.positions.defined() || !data.data.defined()) {
    return dest;
  }

  auto numEntries = int(data.data.size(0));
  auto racc = dest.tensor;
  auto pacc = const_cast<torch::TensorInt32&>(data.positions);
  auto dacc = const_cast<torch::TensorFloat&>(data.data)[0];
  for (auto i = 0; i < numEntries; i++) {
    auto y = pacc[i][0];
    auto x = pacc[i][1];

    // The unit type is modified based on
    auto val = dacc[i] - unitValueOffset;
    auto channel = channelValues.find(val);
    if (channel == channelValues.end()) {
      // If value not in channel map, add to other
      racc[numOneHotChannels - 1][y][x] += 1.0;
    } else {
      racc[channel->second][y][x] += 1.0;
    }
  }

  return dest;
}

void UnitStatFeaturizer::extractUnit(TensorDest acc, tcr::Unit const* u) {
  auto ind = 0;
  acc[ind++] = u->pixel_x / 512.;
  acc[ind++] = u->pixel_y / 512.;
  acc[ind++] = u->velocityX / 5.;
  acc[ind++] = u->velocityY / 5.;
  acc[ind++] = u->health / 100.;
  acc[ind++] = u->shield / 100.;
  acc[ind++] = u->energy / 100.;
  acc[ind++] = u->groundCD / 15.;
  acc[ind++] = u->airCD / 15.;
  acc[ind++] = u->armor / 10.;
  acc[ind++] = u->shieldArmor / 10.;
  acc[ind++] = u->groundATK / 10.;
  acc[ind++] = u->airATK / 10.;
  acc[ind++] = u->groundRange / 10.;
  acc[ind++] = u->airRange / 10.;

  auto armorType = u->size == tc::BW::UnitSize::Small
      ? 0
      : u->size == tc::BW::UnitSize::Medium ? 1 : 2;
  acc[ind + armorType] = 1;
  ind += 3;

  auto gDmgType =
      u->groundDmgType == tc::BW::DamageType::Concussive
      ? 0
      : u->groundDmgType == tc::BW::DamageType::Explosive ? 1
                                                                         : 2;
  acc[ind + gDmgType] = 1;
  ind += 3;

  auto aDmgType = u->airDmgType == tc::BW::DamageType::Concussive
      ? 0
      : u->airDmgType == tc::BW::DamageType::Explosive ? 1 : 2;
  acc[ind + aDmgType] = 1;
  ind += 3;

  for (auto flag = 0; flag < tc2::UnitFlagsFeaturizer::kNumUnitFlags;
       flag++) {
    acc[ind++] = (u->flags & (1 << flag)) ? 1 : 0;
  }
}

} // namespace tc2
