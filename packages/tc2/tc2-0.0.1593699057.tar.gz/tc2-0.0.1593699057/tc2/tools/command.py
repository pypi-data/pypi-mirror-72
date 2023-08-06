import numpy
from typing import *
from tc2 import tc2lib, CommandType
from tc2.constants import *

def command_attack_unit(unit, target) -> CommandType:
  return [
    int(tc2lib.Constants.command_unit),
    int(unit.id),
    int(tc2lib.Constants.unitcommandtypes.Attack_Unit),
    int(target.id)]

def command_attack_position(unit, x: int, y: int) -> CommandType:
  return [
    int(tc2lib.Constants.command_unit),
    int(unit.id),
    int(tc2lib.Constants.unitcommandtypes.Attack_Move),
    int(-1),
    int(x),
    int(y)]

def command_move(unit, x: int, y: int) -> CommandType:
  return [
    int(tc2lib.Constants.command_unit),
    int(unit.id),
    int(tc2lib.Constants.unitcommandtypes.Move),
    int(-1),
    int(x),
    int(y)]

def command_hold_position(unit) -> CommandType:
  return [
    int(tc2lib.Constants.command_unit),
    int(unit.id),
    int(tc2lib.Constants.unitcommandtypes.HoldPosition)]

def command_gather(unit, target) -> CommandType:
  return [
    int(tc2lib.Constants.command_unit),
    int(unit.id),
    int(tc2lib.Constants.unitcommandtypes.Gather),
    int(target.id)]

def command_draw_unit_circle(unit, radius: int, color: int=255) -> CommandType:
  return [
    int(TCCommands.draw_unit_circle),
    int(unit.id),
    int(radius),
    int(color)]

class CommandTensorShapeError(ValueError): pass
class CommandTensorUnitDimensionError(ValueError): pass
class CommandTensorCommandDimensionError(ValueError): pass

non_type_columns = 3 # Target ID + Target X + Target Y

def commandtype_columns() -> int:
  """The number of columns used to represent TCUnitCommands"""
  return len(TCUnitCommands.ids)

def buildtype_columns() -> int:
  """The number of columns used to store possible Unit/Tech/Upgrade types"""
  return len(TCUnits.ids) + len(TCTechs.ids) + len(TCUpgrades.ids)

def command_tensor_shape(observation) -> Tuple[int, int]:
  """Returns the expected shape of a command tensor for a given observation"""
  return (len(observation.units.agent.ids), non_type_columns + commandtype_columns() + buildtype_columns())

def tensor_to_commands(observation, command_tensor: numpy.ndarray) -> List[CommandType]:
  """Converts a Units x [One-hot command, one-hot type ID, Target ID, Target X, Target Y] tensor to TorchCraft commands"""

  # Verify appropriate dimensions
  expected_shape = command_tensor_shape(observation)

  if len(command_tensor.shape) != 2:
    raise CommandTensorShapeError(
      "The command tensor should be two dimensional: [# of units in the unit features] x [features]. Should be {} but was {}"
        .format(expected_shape,  command_tensor.shape))
  if command_tensor.shape[0] != expected_shape[0]:
    raise CommandTensorUnitDimensionError(
      "The length of the first dimension of the command tensor should equal the number of units you have. Should be {} but was {}"
        .format(expected_shape[0], command_tensor.shape[0]))
  if command_tensor.shape[1] != expected_shape[1]:
    raise CommandTensorCommandDimensionError(
      "The length of the second dimension of the command tensor should equal the number of features. Should be {} but was {}"
        .format(expected_shape[1], command_tensor.shape[1]))

  # Convert the tensor to commands
  commands_output: List[CommandType] = []
  for unit_index in range(0, expected_shape[0]):
    unit_id = observation.units.agent.ids[unit_index]
    unit_tensor = command_tensor[unit_index]
    target_id = unit_tensor[0]
    target_x = unit_tensor[1]
    target_y = unit_tensor[2]
    command_id = numpy.argmax(unit_tensor[non_type_columns : non_type_columns + commandtype_columns()])
    build_id = numpy.argmax(unit_tensor[non_type_columns + commandtype_columns():])
    if build_id >= len(TCUnits.ids):
      # It's not a unit type; it's a tech or upgrade type
      build_id -= len(TCUnits.ids)
      if build_id >= len(TCTechs.ids):
        # It's not a tech type; it's an upgrade type
        build_id -= len(TCTechs.ids)
    commands_output += [[
      int(tc2lib.Constants.command_unit),
      int(unit_id),
      int(command_id),
      #int(build_id),
      int(target_id),
      int(target_x),
      int(target_y)]]
  return commands_output
