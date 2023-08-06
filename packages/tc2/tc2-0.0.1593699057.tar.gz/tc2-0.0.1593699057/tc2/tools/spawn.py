from tc2 import tc2lib, CommandType

def command_spawn(player: int, unit: int, x: int, y: int) -> CommandType:
  return [
    int(tc2lib.Constants.command_openbw),
    int(tc2lib.Constants.openbwcommandtypes.SpawnUnit),
    int(player),
    int(unit),
    int(x),
    int(y)]
    
def command_kill(id: int) -> CommandType:
  return [
    int(tc2lib.Constants.command_openbw),
    int(tc2lib.Constants.openbwcommandtypes.KillUnit),
    int(id)]

def command_upgrade(player: int, upgrade: int, level: int=1) -> CommandType:
  return [
    int(tc2lib.Constants.command_openbw),
    int(tc2lib.Constants.openbwcommandtypes.SetPlayerUpgradeLevel),
    int(player),
    int(upgrade),
    int(level)]
    
def command_research(player: int, tech: int, researched: bool=True) -> CommandType:
  return [
    int(tc2lib.Constants.command_openbw),
    int(tc2lib.Constants.openbwcommandtypes.SetPlayerResearched),
    int(player),
    int(tech),
    int(researched)]
