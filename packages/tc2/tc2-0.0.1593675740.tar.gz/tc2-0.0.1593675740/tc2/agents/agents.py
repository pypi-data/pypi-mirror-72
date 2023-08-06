from typing import List, Tuple
from tc2 import CommandType, tc2lib
from tc2.tools import *
from tc2.constants import *

def do_nothing(tcstate: tc2lib.State) -> List[CommandType]:
  if not isinstance(tcstate, tc2lib.State):
    raise TypeError(f"tcstate argument should be of type tc2lib.State, got {tcstate}")
  return []
  
def our_units(tcstate: tc2lib.State) -> List:
  if not isinstance(tcstate, tc2lib.State):
    raise TypeError(f"tcstate argument should be of type tc2lib.State, got {tcstate}")
  player = tcstate.player_id
  units = tcstate.units
  return units[player] if player in units else []
  
def enemy_units(tcstate: tc2lib.State) -> List:
  if not isinstance(tcstate, tc2lib.State):
    raise TypeError(f"tcstate argument should be of type tc2lib.State, got {tcstate}")
  player_id = other_player_id(tcstate.player_id)
  units = tcstate.units
  return units[player_id] if player_id in units else []

def neutral_units(tcstate: tc2lib.State) -> List:
  if not isinstance(tcstate, tc2lib.State):
    raise TypeError(f"tcstate argument should be of type tc2lib.State, got {tcstate}")
  return tcstate.units[TCNeutral.player_id(tcstate)]

def hold_position(tcstate: tc2lib.State) -> List[CommandType]:
  if not isinstance(tcstate, tc2lib.State):
    raise TypeError(f"tcstate argument should be of type tc2lib.State, got {tcstate}")
  units_ours = our_units(tcstate)
  return [
    command_hold_position(unit)
    for unit in units_ours
    if not unit.holding_position]

def attack_middle(tcstate: tc2lib.State) -> List[CommandType]:
  if not isinstance(tcstate, tc2lib.State):
    raise TypeError(f"tcstate argument should be of type tc2lib.State, got {tcstate}")
  middle_x = tcstate.map_size[0] / 2
  middle_y = tcstate.map_size[1] / 2
  units_ours = our_units(tcstate)
  return [
    command_attack_position(unit, middle_x, middle_y)
    for unit in units_ours
    if unit.idle]

def distance_squared(a: Tuple[float, float], b: Tuple[float, float]) -> float:
  return (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])
  
def unit_distance_center_squared(a, b) -> float:
  return distance_squared((a.x, a.y), (b.x, b.y))
  
def can_attack(attacker, target) -> bool:
  if (attacker.type in [TCUnits.Terran_Bunker, TCUnits.Protoss_Carrier]): return True
  if (attacker.type == TCUnits.Protoss_Reaver and not target.flying): return True
  return attacker.airATK > 0 if target.flying else attacker.groundATK > 0

def attack_closest_enemy(attacker, enemies: List) -> List[CommandType]:
  valid_targets = list(filter(lambda target: can_attack(attacker, target), enemies))
  if valid_targets:
    # Attack the closest valid target
    target = min(valid_targets, key = lambda target: unit_distance_center_squared(attacker, target))    
    return [command_attack_unit(attacker, target)] if attacker.command.targetId != target.id else []
  elif enemies and attacker.idle:
    # Attack the position of the enemy closest to the centroid of enemies
    centroid = (
      sum(map(lambda enemy: enemy.x, enemies)) / len(enemies),
      sum(map(lambda enemy: enemy.y, enemies)) / len(enemies))
    target_unit = min(enemies, key = lambda target: distance_squared(centroid, (target.y, target.y))) 
    return [command_attack_position(attacker, target_unit.x, target_unit.y)]
  else:
    # Do nothing
    return []
    
def gather_closest_resource(gatherer, resources: List) -> List[CommandType]:
  if resources:
    resource = min(resources, key = lambda target: unit_distance_center_squared(gatherer, target))
    return [command_gather(gatherer, resource)]
  else:
    return []

def attack_closest(tcstate) -> List[CommandType]:
  units_ours = our_units(tcstate)
  units_enemy = enemy_units(tcstate)
  commands = [attack_closest_enemy(unit, units_enemy) for unit in units_ours]
  output = [item for sublist in commands for item in sublist]
  return output
  
def gather_closest(tcstate) -> List[CommandType]:
  units_ours = our_units(tcstate)
  resources = list(filter(
    lambda unit: unit.visible and unit.type in [
      TCUnits.Resource_Mineral_Field,
      TCUnits.Terran_Refinery,
      TCUnits.Protoss_Assimilator,
      TCUnits.Zerg_Extractor],
    enemy_units(tcstate) + neutral_units(tcstate)))
  commands = [
    gather_closest_resource(unit, resources)
    for unit in units_ours
    if unit.idle]
  output = [item for sublist in commands for item in sublist]
  return output