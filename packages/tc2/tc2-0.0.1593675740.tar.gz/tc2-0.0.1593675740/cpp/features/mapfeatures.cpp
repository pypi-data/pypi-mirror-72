/*
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include "features.h"

#include <cassert>
#include <fmt/ostream.h>
#include <glog/logging.h>

namespace tc2 {
namespace featureimpl {

namespace {

int constexpr kNumTerrainValues = 3;
auto constexpr kStandardMapSize = 512; // walk-tiles

void getIndexBounds(
    Rect& ir,
    int& axmin,
    int& axmax,
    int& aymin,
    int& aymax,
    Rect const& boundingBox,
    Rect const& mapRect) {
  // This is the region we are able to fill
  ir = boundingBox.intersected(mapRect);
  if (ir.empty()) {
    axmin = 1;
    axmax = 0;
    aymin = 1;
    aymax = 0;
    return;
  }
  // Index bounds on tensor
  axmin = ir.x - boundingBox.x;
  axmax = axmin + ir.w;
  aymin = ir.y - boundingBox.y;
  aymax = aymin + ir.h;
}

void extractStaticMapDataHelper(
    torch::TensorFloat tensor,
    Rect const& boundingBox,
    std::vector<uint8_t> const& data,
    Rect const& mapRect) {
  Rect ir;
  int axmin, axmax;
  int aymin, aymax;
  getIndexBounds(ir, axmin, axmax, aymin, aymax, boundingBox, mapRect);

  tensor.fill_(-1);
  auto a = tensor[0];
  for (int ay = aymin, wy = ir.y; ay < aymax; ay++, wy++) {
    auto row = a[ay];
    auto woff = wy * mapRect.w;
    for (int ax = axmin, wx = ir.x; ax < axmax; ax++, wx++) {
      row[ax] = data[woff + wx];
    }
  }
}

void fillBlocking(
    torch::TensorAccessorBase<float, 2> a,
    tcr::Unit* u,
    FeaturePositionMapper& mapper) {
  auto px = u->pixel_x;
  auto py = u->pixel_y;
  auto left = (px - u->getType()->dimensionLeft); // TODO: Units?
  auto top = (py - u->getType()->dimensionUp); // TODO: Units?
  auto right = (px + u->getType()->dimensionRight); // TODO: Units?
  auto bottom = (py + u->getType()->dimensionDown); // TODO: Units?
  for (auto y = top; y <= bottom; y++) {
    for (auto x = left; x <= right; x++) {
      auto mpos = mapper({x, y});
      if (mpos.x >= 0) {
        a[mpos.y][mpos.x] = 1;
      }
    }
  }
}

} // namespace

/**
 * Extracts a 2D tensor of ground height, which impacts vision and the
 * probability that a bullet attack will miss. Ignores the presence of doodads.
 *
 * * 0: Low ground
 * * 1: High ground
 * * 2: Very high ground
 *
 * See
 * https://bwapi.github.io/class_b_w_a_p_i_1_1_game.html#a94eb3e3fe7850078c2086638a46214be
 */
void extractGroundHeight(torch::TensorFloat tensor, tc::State const* state, Rect const& r) {
  Rect ir;
  int axmin, axmax;
  int aymin, aymax;
  auto mapRect = getRect(state);
  getIndexBounds(ir, axmin, axmax, aymin, aymax, r, mapRect);

  auto const& data = state->ground_height_data;
  tensor.fill_(-1);
  auto a = tensor[0];
  for (int ay = aymin, wy = ir.y; ay < aymax; ay++, wy++) {
    auto row = a[ay];
    auto woff = wy * mapRect.w;
    for (int ax = axmin, wx = ir.x; ax < axmax; ax++, wx++) {
      row[ax] = data[woff + wx] / 2;
    }
  }
}

/**
 * Extracts a 2D tensor of the presence of tall doodads, which impact vision
 * and the probability that a bullet attack will miss.
 *
 * * 0: No tall doodad
 * * 1: Tall doodad
 *
 * See
 * https://bwapi.github.io/class_b_w_a_p_i_1_1_game.html#a94eb3e3fe7850078c2086638a46214be
 */
void extractTallDoodad(torch::TensorFloat tensor, tc::State const* state, Rect const& r) {
  Rect ir;
  int axmin, axmax;
  int aymin, aymax;
  auto mapRect = getRect(state);
  getIndexBounds(ir, axmin, axmax, aymin, aymax, r, mapRect);

  auto const& data = state->ground_height_data;
  tensor.fill_(0);
  auto a = tensor[0];
  for (int ay = aymin, wy = ir.y; ay < aymax; ay++, wy++) {
    auto row = a[ay];
    auto woff = wy * mapRect.w;
    for (int ax = axmin, wx = ir.x; ax < axmax; ax++, wx++) {
      row[ax] = data[woff + wx] % 2;
    }
  }
}

/**
 * Extracts a 2D tensor of whether the terrain on a walktile is walkable by
 * ground units.
 *
 * See
 * https://bwapi.github.io/class_b_w_a_p_i_1_1_game.html#a91153ca71797617ce225adf28d508510
 */
void extractWalkability(torch::TensorFloat t, tc::State const* state, Rect const& r) {
  extractStaticMapDataHelper(
      t, r, state->walkable_data, getRect(state));
}

void extractBuildability(torch::TensorFloat t, tc::State const* state, Rect const& r) {
  extractStaticMapDataHelper(
      t, r, state->buildable_data, getRect(state));
}

void extractFogOfWar(torch::TensorFloat t, tc::State const* state, Rect const& r) {
  extractStaticMapDataHelper(
      t, r, state->visibility, getRect(state));
}

/**
 * 2D tensor representation of whether a tile has creep
 */
void extractCreep(torch::TensorFloat t, tc::State const* state, Rect const& r) {
  // TODO: Implement extractCreep()
}

/**
 * Extracts a 3D tensor of ground height, where each of the 3 ground heights
 * (plus "on the map") is a one-hot dimension. Ignores the presence of
 * doodads.
 *
 * See
 * https://bwapi.github.io/class_b_w_a_p_i_1_1_game.html#a94eb3e3fe7850078c2086638a46214be
 */
void extractOneHotGroundHeight(torch::TensorFloat tensor, tc::State const* state, Rect const& r) {
  Rect ir;
  int axmin, axmax;
  int aymin, aymax;
  auto mapRect = getRect(state);
  getIndexBounds(ir, axmin, axmax, aymin, aymax, r, mapRect);

  auto const& data = state->ground_height_data;
  // One channel for each possible values and one for off of map
  tensor.resize_({kNumTerrainValues + 1, tensor.size(1), tensor.size(2)});
  tensor.fill_(0);
  for (int ay = aymin, wy = ir.y; ay < aymax; ay++, wy++) {
    auto woff = wy * mapRect.w;
    for (int ax = axmin, wx = ir.x; ax < axmax; ax++, wx++) {
      auto channel = data[woff + wx] / 2;
      assert(channel <= 2 && channel >= 0);
      tensor[channel][ay][ax] = 1;
      tensor[kNumTerrainValues][ay][ax] = 1;
    }
  }
}

/**
 * Set tensor to '1' for every start location reported by TorchCraft.
 */
void extractStartLocations(torch::TensorFloat tensor, tc::State const* state, Rect const& r) {
  FeaturePositionMapper mapper(r, getRect(state));
  auto a = tensor[0];
  for (auto& pos : state->start_locations) {
    auto mpos = mapper({pos.x, pos.y});
    if (mpos.x >= 0) {
      a[mpos.y][mpos.x] = 1;
    }
  }
}

/**
 * Grid of X/Y coordinates.
 * Channel 0 for Y, channel 1 for X. Uniform stepping with 1/512
 */
void extractXYGrid(torch::TensorFloat tensor, tc::State const* state, Rect const& r) {
  Rect ir;
  int axmin, axmax;
  int aymin, aymax;
  auto mapRect = getRect(state);
  getIndexBounds(ir, axmin, axmax, aymin, aymax, r, mapRect);

  tensor.fill_(-1);
  auto constexpr stepx = 1.0f / kStandardMapSize;
  auto constexpr stepy = 1.0f / kStandardMapSize;
  float py = ir.y * stepy;
  for (int ay = aymin; ay < aymax; ay++, py += stepy) {
    float px = ir.x * stepx;
    for (int ax = axmin; ax < axmax; ax++, px += stepx) {
      tensor[0][ay][ax] = py;
      tensor[1][ay][ax] = px;
    }
  }
}

/**
 * Set tensor to '1' for every walktile occupied by resources.
 */
void extractResources(torch::TensorFloat tensor, tc::State const* state, Rect const& r) {
  auto mul = tc::BW::XYPixelsPerWalktile;
  auto pixR = Rect(r.x * mul, r.y * mul, r.w * mul, r.h * mul);
  auto mr = getRect(state);
  auto pixMapRect = Rect(mr.x * mul, mr.y * mul, mr.w * mul, mr.h * mul);
  FeaturePositionMapper mapper(pixR, pixMapRect);
  auto h = tensor.size(1);
  auto w = tensor.size(2);
  auto pxTensor = torch::zeros<float>({1, h * mul, w * mul});
  const auto accessor = pxTensor[0];
  for (auto* u : state->allUnits) {
    if (u->getType()->isResourceContainer) {
      fillBlocking(accessor, u, mapper);
    }
  }
  // TODO: Make sure we're handling everything properly
  //torch::adaptive_avg_pool2d_out(t, pxTensor, {h, w});
}

/**
 * Set tensor to '1' for every walktile occupied by a structure
 */
void extractHasStructure(torch::TensorFloat t, tc::State const* state, Rect const& r) {
  auto mul = tc::BW::XYPixelsPerWalktile;
  auto pixR = Rect(r.x * mul, r.y * mul, r.w * mul, r.h * mul);
  auto mr = getRect(state);
  auto pixMapRect = Rect(mr.x * mul, mr.y * mul, mr.w * mul, mr.h * mul);
  FeaturePositionMapper mapper(pixR, pixMapRect);
  auto h = t.size(1);
  auto w = t.size(2);
  auto pxTensor = torch::zeros<float>({1, h * mul, w * mul});
  const auto accessor = pxTensor[0];
  for (auto* u : state->allUnits) {
    if (!(u->getType()->isMinerals || u->getType()->isGas) &&
        (u->getType()->isBuilding || u->getType()->isSpecialBuilding)) {
      fillBlocking(accessor, u, mapper);
    }
  }
  // TODO: Make sure we're handling everything properly
  //torch::adaptive_avg_pool2d_out(t, pxTensor, {h, w});
}

} // namespace featureimpl
} // namespace tc2
