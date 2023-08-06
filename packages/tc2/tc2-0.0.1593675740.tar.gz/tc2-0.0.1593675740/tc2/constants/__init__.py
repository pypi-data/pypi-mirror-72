from tc2 import tc2lib

# TC constants
TCCommands=tc2lib.Constants.commands
TCUnitCommands=tc2lib.Constants.unitcommandtypes
TCOpenBWCommands=tc2lib.Constants.openbwcommandtypes
TCUserCommands=tc2lib.Constants.usercommandtypes
TCOrders=tc2lib.Constants.orders
TCTechs=tc2lib.Constants.techtypes
TCUpgrades=tc2lib.Constants.upgradetypes
TCUnits=tc2lib.Constants.unittypes
TCBullets=tc2lib.Constants.bullettypes
TCWeapons=tc2lib.Constants.weapontypes
TCUnitSizes=tc2lib.Constants.unitsizes
TCDamages=tc2lib.Constants.dmgtypes
TCRaces=tc2lib.Constants.races
TCColors=tc2lib.Constants.colors
TCStaticValues=tc2lib.Constants.staticvalues
TCGameTypes = tc2lib.GameType

# Player identifiers
#
# "TCAgent" is the protagonist/agent from the perspective of the Gym interface.
# It always gets its own TorchCraft client (index == 0).
#
# "TCEnemy" is the antagonist/environment from the perspective of the Gym interface.
# If the environment is run in multi-player mode,
# it gets its own TorchCraft client (index == 1) and can receive commands.
# Otherwise, it is an idle computer-controlled player.
#
# TorchCraft (via BWAPI) assigns each player a player ID.
# In single-player, TCAgent is always player ID #0.
# But in multiplayer, either TCAgent or TCEnemy can be each of ID #0 or ID #1;
# the only way to tell is to inspect the TorchCraft game state.
#
# There is also a neutral player, who typically controls map elements like
# mineral patches, vespene geysers, map blockers, and critters.
# The neutral player never has its own TorchCraft client, can not receive commands,
# and always has player ID #-1.

TCNeutralPlayerId = -1
  
def other_player_id(player_id: int) -> int:
  """Returns the player ID of the opponent of the given player."""
  if player_id == 0: return 1
  if player_id == 1: return 0
  raise Exception("Unappropriate player_id for other()", player_id)  

class TCPlayer:
  def __init__(self, client_id: int):
    self.client_id = client_id
  def player_id(self, tcstate0) -> int:
    if (self.client_id == TCNeutralPlayerId): return TCNeutralPlayerId
    if (self.client_id == 0): return tcstate0.player_id
    return other_player_id(tcstate0.player_id)
  def other(self) -> 'TCPlayer':
    if self is TCAgent: return TCEnemy
    if self is TCEnemy: return TCAgent
    raise Exception("Unknown TCPlayer: ", self)
  def __repr__(self) -> str:
    return f'Player client #{self.client_id}'
    
TCAgent=TCPlayer(0)
TCEnemy=TCPlayer(1)
TCNeutral=TCPlayer(TCNeutralPlayerId)
TCPlayers=[TCAgent, TCEnemy]



