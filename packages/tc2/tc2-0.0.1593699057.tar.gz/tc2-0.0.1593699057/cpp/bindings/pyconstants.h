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

#include "camelcase.h"

// We have to use a class for BetterEnums
template <typename Enum, typename F>
void setEnumDict(pybind11::module& module, const std::string& name, F nameToKey) {
  pybind11::module submodule = module.def_submodule(name.c_str());
  pybind11::dict byName;
  pybind11::dict byId;
  for (auto value : Enum::_values()) {
    auto valueName = value._to_string();
    auto valueId = value._to_integral();
    auto str = nameToKey(valueName);
    byName[pybind11::str(str)] = pybind11::int_(valueId);
    byId[pybind11::int_(valueId)] = pybind11::str(str);
    submodule.attr(pybind11::str(str)) = pybind11::int_(valueId);
  }
  submodule.attr("names") = byName;
  submodule.attr("ids") = byId;
}

template <typename Enum>
void setEnumDict(pybind11::module& module, const std::string& name) {
  setEnumDict<Enum>(module, name, [](const std::string& s) { return s; });
}

template <typename Enum>
std::vector<int32_t> getEnumVector(std::vector<Enum> v) {
  std::vector<int32_t> lst;
  for (size_t i = 0; i < v.size(); ++i) {
    lst.push_back(v[i]._to_integral());
  }
  return lst;
}

template <typename T>
pybind11::dict getStaticValues(const T m[]) {
  namespace tcb = torchcraft::BW;
  pybind11::dict dict;
  for (auto unitType : tcb::UnitType::_values()) {
    if (unitType._to_integral() == tcb::UnitType::MAX) {
      continue;
    }
    dict[pybind11::str(unitType._to_string())] = m[unitType];
    dict[pybind11::int_(unitType._to_integral())] = m[unitType];
  }
  return dict;
}

void init_constants(pybind11::module& torchcraft) {
  namespace tcb = torchcraft::BW;
  namespace tcbd = torchcraft::BW::data;

  pybind11::module constants = torchcraft.def_submodule("Constants");
  setEnumDict<tcb::Command>(constants, "commands", fromCamelCaseToLower);
  for (auto command : tcb::Command::_values()) {
    constants.attr(fromCamelCaseToLower(command._to_string()).c_str()) = command._to_integral();
  }
  setEnumDict<tcb::UnitCommandType>(constants, "unitcommandtypes");
  setEnumDict<tcb::OpenBWCommandType>(constants, "openbwcommandtypes");
  setEnumDict<tcb::UserCommandType>(constants, "usercommandtypes");
  setEnumDict<tcb::Order>(constants, "orders");
  setEnumDict<tcb::TechType>(constants, "techtypes");
  setEnumDict<tcb::UpgradeType>(constants, "upgradetypes");
  setEnumDict<tcb::UnitType>(constants, "unittypes");
  setEnumDict<tcb::BulletType>(constants, "bullettypes");
  setEnumDict<tcb::WeaponType>(constants, "weapontypes");
  setEnumDict<tcb::UnitSize>(constants, "unitsizes");
  setEnumDict<tcb::DamageType>(constants, "dmgtypes");
  setEnumDict<tcb::Race>(constants, "races");
  setEnumDict<tcb::Color>(constants, "colors");

  pybind11::dict produces, producedby;
  for (auto unitType : tcb::UnitType::_values()) {
    auto unitTypeId = unitType._to_integral();
    if (unitTypeId == tcb::UnitType::MAX) {
      continue;
    }
    auto unitProductions = tcb::unitProductions(unitType);
    if (!unitProductions.empty()) {
      produces[pybind11::int_(unitTypeId)] = getEnumVector(std::move(unitProductions));
    }
    for (auto producer : unitProductions) {
      producedby[pybind11::int_(unitTypeId)] = pybind11::int_(producer._to_integral());
    }
  }
  constants.attr("produces") = produces; // Dict of UnitType: [productions]
  constants.attr("producedby") = producedby; // Dict of UnitType: producedBy

  pybind11::dict commandToOrder;
  for (auto command : tcb::UnitCommandType::_values()) {
    auto order = tcb::commandToOrders(command);
    if (!order.empty()) {
      commandToOrder[pybind11::int_(command._to_integral())] = getEnumVector(std::move(order));
    }
  }
  constants.attr("command2order") = commandToOrder;

  std::unordered_map<int32_t, std::vector<int32_t>> orderToCommand;
  for (auto command : tcb::UnitCommandType::_values()) {
    for (auto order : tcb::commandToOrders(command)) {
      auto orderId = order._to_integral();
      if (orderToCommand.find(orderId) == orderToCommand.end()) {
        orderToCommand[orderId] = std::vector<int32_t>();
      }
      orderToCommand[orderId].push_back(command._to_integral());
    }
  }
  constants.attr("order2command") = orderToCommand;

  constants.def("isbuilding", [](int32_t id) { return tcb::isBuilding(tcb::UnitType::_from_integral(id)); });
  constants.def("isworker", [](int32_t id) { return tcb::isWorker(tcb::UnitType::_from_integral(id)); });
  constants.def("ismineralfield", [](int32_t id) { return tcb::isMineralField(tcb::UnitType::_from_integral(id)); });
  constants.def("isgasgeyser", [](int32_t id) { return tcb::isGasGeyser(tcb::UnitType::_from_integral(id)); });

  pybind11::dict sv;
  sv["canAttack"] = getStaticValues(tcbd::CanAttack);
  sv["dimensionRight"] = getStaticValues(tcbd::DimensionRight);
  sv["height"] = getStaticValues(tcbd::Height);
  sv["isMineralField"] = getStaticValues(tcbd::IsMineralField);
  sv["canProduce"] = getStaticValues(tcbd::CanProduce);
  sv["isRefinery"] = getStaticValues(tcbd::IsRefinery);
  sv["isResourceDepot"] = getStaticValues(tcbd::IsResourceDepot);
  sv["regeneratesHP"] = getStaticValues(tcbd::RegeneratesHP);
  sv["isCloakable"] = getStaticValues(tcbd::IsCloakable);
  sv["isTwoUnitsInOneEgg"] = getStaticValues(tcbd::IsTwoUnitsInOneEgg);
  sv["isSpellcaster"] = getStaticValues(tcbd::IsSpellcaster);
  sv["supplyRequired"] = getStaticValues(tcbd::SupplyRequired);
  sv["airWeapon"] = getStaticValues(tcbd::AirWeapon);
  sv["buildScore"] = getStaticValues(tcbd::BuildScore);
  sv["maxAirHits"] = getStaticValues(tcbd::MaxAirHits);
  sv["isPowerup"] = getStaticValues(tcbd::IsPowerup);
  sv["isBeacon"] = getStaticValues(tcbd::IsBeacon);
  sv["mineralPrice"] = getStaticValues(tcbd::MineralPrice);
  sv["isInvincible"] = getStaticValues(tcbd::IsInvincible);
  sv["requiredTech"] = getStaticValues(tcbd::RequiredTech);
  sv["dimensionDown"] = getStaticValues(tcbd::DimensionDown);
  sv["canBuildAddon"] = getStaticValues(tcbd::CanBuildAddon);
  sv["dimensionLeft"] = getStaticValues(tcbd::DimensionLeft);
  sv["producesLarva"] = getStaticValues(tcbd::ProducesLarva);
  sv["armor"] = getStaticValues(tcbd::Armor);
  sv["isMechanical"] = getStaticValues(tcbd::IsMechanical);
  sv["isBuilding"] = getStaticValues(tcbd::IsBuilding);
  sv["supplyProvided"] = getStaticValues(tcbd::SupplyProvided);
  sv["sightRange"] = getStaticValues(tcbd::SightRange);
  sv["gasPrice"] = getStaticValues(tcbd::GasPrice);
  sv["maxHitPoints"] = getStaticValues(tcbd::MaxHitPoints);
  sv["width"] = getStaticValues(tcbd::Width);
  sv["tileWidth"] = getStaticValues(tcbd::TileWidth);
  sv["isHero"] = getStaticValues(tcbd::IsHero);
  sv["seekRange"] = getStaticValues(tcbd::SeekRange);
  sv["buildTime"] = getStaticValues(tcbd::BuildTime);
  sv["isCritter"] = getStaticValues(tcbd::IsCritter);
  sv["requiresPsi"] = getStaticValues(tcbd::RequiresPsi);
  sv["isSpecialBuilding"] = getStaticValues(tcbd::IsSpecialBuilding);
  sv["groundWeapon"] = getStaticValues(tcbd::GroundWeapon);
  sv["isFlyer"] = getStaticValues(tcbd::IsFlyer);
  sv["size"] = getStaticValues(tcbd::Size);
  sv["isNeutral"] = getStaticValues(tcbd::IsNeutral);
  sv["maxShields"] = getStaticValues(tcbd::MaxShields);
  sv["hasPermanentCloak"] = getStaticValues(tcbd::HasPermanentCloak);
  sv["topSpeed"] = getStaticValues(tcbd::TopSpeed);
  sv["tileHeight"] = getStaticValues(tcbd::TileHeight);
  sv["isRobotic"] = getStaticValues(tcbd::IsRobotic);
  sv["dimensionUp"] = getStaticValues(tcbd::DimensionUp);
  sv["destroyScore"] = getStaticValues(tcbd::DestroyScore);
  sv["spaceProvided"] = getStaticValues(tcbd::SpaceProvided);
  sv["tileSize"] = getStaticValues(tcbd::TileSize);
  sv["haltDistance"] = getStaticValues(tcbd::HaltDistance);
  sv["isAddon"] = getStaticValues(tcbd::IsAddon);
  sv["canMove"] = getStaticValues(tcbd::CanMove);
  sv["isFlyingBuilding"] = getStaticValues(tcbd::IsFlyingBuilding);
  sv["maxEnergy"] = getStaticValues(tcbd::MaxEnergy);
  sv["isDetector"] = getStaticValues(tcbd::IsDetector);
  sv["isOrganic"] = getStaticValues(tcbd::IsOrganic);
  sv["spaceRequired"] = getStaticValues(tcbd::SpaceRequired);
  sv["isFlagBeacon"] = getStaticValues(tcbd::IsFlagBeacon);
  sv["isWorker"] = getStaticValues(tcbd::IsWorker);
  sv["isBurrowable"] = getStaticValues(tcbd::IsBurrowable);
  sv["cloakingTech"] = getStaticValues(tcbd::CloakingTech);
  sv["isResourceContainer"] = getStaticValues(tcbd::IsResourceContainer);
  sv["acceleration"] = getStaticValues(tcbd::Acceleration);
  sv["isSpell"] = getStaticValues(tcbd::IsSpell);
  sv["requiresCreep"] = getStaticValues(tcbd::RequiresCreep);
  sv["armorUpgrade"] = getStaticValues(tcbd::ArmorUpgrade);
  sv["maxGroundHits"] = getStaticValues(tcbd::MaxGroundHits);
  sv["turnRadius"] = getStaticValues(tcbd::TurnRadius);
  sv["getRace"] = getStaticValues(tcbd::GetRace);

  constants.attr("staticvalues") = sv;

  pybind11::dict totalPrices, totalMineralPrice, totalGasPrice;
  for (auto u : tcbd::TotalMineralPrice) {
    totalMineralPrice[pybind11::int_(u.first._to_integral())] = u.second;
  }
  for (auto u : tcbd::TotalGasPrice) {
    totalGasPrice[pybind11::int_(u.first._to_integral())] = u.second;
  }
  totalPrices["mineral"] = totalMineralPrice;
  totalPrices["gas"] = totalGasPrice;
}