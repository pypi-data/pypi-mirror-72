/*
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include "jitter.h"

#include <glog/logging.h>
#include <torchcraft/frame.h>

//#include "state.h"
//#include "unitsinfo.h"
//#include "utils.h"

#include <map>
#include <numeric>

namespace tc2 {

Position NoJitter::operator()(tcr::Unit const* u) const {
  return {u->x, u->y};
}

namespace {
Position findJitteredPosition(
    tcr::Unit const* u,
    std::map<Position, std::vector<tcr::Unit const*>> const& jitteredUnits,
    Rect const& crop,
    std::function<bool(tcr::Unit const*, tcr::Unit const*)> const& compatible) {
  Position pos(u->x, u->y);
  // we iterate over squares centered on the original position, increasing
  // the radius until we find a suitable position.
  Position v1(0, 1), v2(1, 0), v3(-1, 0), v4(0, -1);
  for (int r = 0; r <= std::max(crop.width(), crop.height()); ++r) {
    Position topLeft = pos - r;
    Position bottomRight = pos + r;
    // iterate on the border
    for (int i = 0; i < (2 * r) + 1; ++i) {
      Position P1 = topLeft + (v1 * i);
      Position P2 = topLeft + (v2 * i);
      Position P3 = bottomRight + (v3 * i);
      Position P4 = bottomRight + (v4 * i);
      for (const auto& p : {P1, P2, P3, P4}) {
        if (crop.contains(p) &&
            (jitteredUnits.count(p) == 0 ||
             std::accumulate(
                 jitteredUnits.at(p).begin(),
                 jitteredUnits.at(p).end(),
                 true,
                 [&compatible, &u](bool b, tcr::Unit const* v) {
                   return b && compatible(u, v);
                 }))) {
          return p;
        }
      }
    }
  }
  LOG(WARNING) << "Couldn't find jitter position for tcr::Unit "
          << u->id << " within crop " << crop
          << ". Dropping it.";
  return kInvalidPosition;
}
} // namespace

Jitter::Jitter(tc::State const* st, Rect const& crop, bool allowSameType) {
  // this map has key=position and value=units we have jittered there

  auto compatible = [allowSameType](tcr::Unit const* u, tcr::Unit const* v) {
    return allowSameType && u == v;
  };
  fillJitter(st, crop, compatible);
}

void Jitter::fillJitter(
    tc::State const* st,
    Rect const& crop,
    std::function<bool(tcr::Unit const*, tcr::Unit const*)> const& compatible) {
  std::map<Position, std::vector<tcr::Unit const*>> jitteredUnits;
  for (tcr::Unit const* unit : st->allUnits) {
    if (unit->isNeutral()) {
      continue;
    }
    auto p = findJitteredPosition(unit, jitteredUnits, crop, compatible);
    jitteredPos_[unit] = p;
    if (p != kInvalidPosition) {
      jitteredUnits[p].push_back(unit);
    }
  }
}

LayeredJitter::LayeredJitter(
    tc::State const* st,
    Rect const& crop,
    bool allowSameTypeAir,
    bool allowSameTypeGround) {
  auto compatible = [allowSameTypeAir, allowSameTypeGround](tcr::Unit const* u, tcr::Unit const* v) {
    if (u->burrowed() || v->burrowed()) {
      // we always allow to stack burrowed and not burrowed, but can't stack two
      // burrowed
      return !(u->burrowed() && v->burrowed());
    }
    if (u->flying() != v->flying()) {
      // flying and not flying, compatible
      return true;
    }
    if (u == v) {
      if (allowSameTypeAir && u->flying() && v->flying()) {
        return true;
      }
      if (allowSameTypeGround && !u->flying() && !v->flying()) {
        return true;
      }
    }
    return false;
  };
  fillJitter(st, crop, compatible);
}

Position Jitter::operator()(tcr::Unit const* u) const {
  if (jitteredPos_.count(u) == 0) {
    LOG(WARNING) << "Suspicious: no jitter information for tcr::Unit "
                 << u->id << ". Jitter might be out of date.";
    return {u->x, u->y};
  }
  return jitteredPos_.at(u);
}

} // namespace tc2
