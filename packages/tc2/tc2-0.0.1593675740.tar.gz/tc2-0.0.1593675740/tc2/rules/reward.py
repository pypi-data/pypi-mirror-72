from collections import defaultdict
from tc2.constants import *
from typing import *

def eliminated_from_micro(tcstates, player_id: int) -> bool:
  """Elimination criterion for micro scenarios, where players have units but usually no buildings"""
  units = [len(tcstate.units[player_id]) for tcstate in tcstates]
  return max(units) == 0

def terminate_timeout(tcstates, seconds: int = 120) -> bool:
  return tcstates[TCAgent.client_id].frame_from_bwapi > 24 * seconds

def terminate_elimination_micro(tcstates):
  # Delay briefly to ensure that units have had a chance to spawn
  if tcstates[TCAgent.client_id].frame_from_bwapi < 3: return False
  agent_player_id = tcstates[TCAgent.client_id].player_id
  player_ids = [agent_player_id, other_player_id(agent_player_id)]
  return any(eliminated_from_micro(tcstates, player_id) for player_id in player_ids)

def reward_binary_micro(tcstates, player_id: int):
  if eliminated_from_micro(tcstates, player_id):
    return 0.0
  if eliminated_from_micro(tcstates, other_player_id(player_id)):
    return 1.0    
  return 0.0

class TC2RewardAbstract:
  def __init__(self) -> None:
    pass
  def on_spawn(self, player_id: int, unit) -> None:
    pass
  def reward(self, tcstates) -> List[float]:
    raise Exception("The reward function is unimplemented")  
  def done(self, tcstates) -> bool:
    raise Exception("The termination function is unimplemented")

class TC2RewardMicroBinary(TC2RewardAbstract):
  """A binary (0/1) reward function, which terminates after one minute or when a player has no remaining units."""
  def reward(self, tcstates) -> List[float]:
    agent_player_id = tcstates[TCAgent.client_id].player_id
    player_ids = [agent_player_id, other_player_id(agent_player_id)]
    return [reward_binary_micro(tcstates, player_id) for player_id in player_ids]
  def done(self, tcstates) -> bool:
    return terminate_timeout(tcstates) or terminate_elimination_micro(tcstates)

class TC2RewardMicroContinuousCount(TC2RewardMicroBinary):
  """A continuous reward function which measures how many units were defeated or retained."""
  def __init__(self) -> None:
    self._units_total: Dict[int, float] = defaultdict(float)
  def on_spawn(self, player_id: int, unit) -> None:
    if player_id not in self._units_total:
      self._units_total[player_id] = 0.0
    self._units_total[player_id] += 1.0
  def reward(self, tcstates) -> List[float]:
    """
    Reward = 50% binary reward, 25% units retained, 25% units defeated
    The reward is structured so that winning is always better than losing, no matter how many units were retained or defeated
    """
    def player_reward(player_id: int) -> float:
      opponent_id = other_player_id(player_id)
      units_retained = len(tcstates[player_id].units[player_id])
      units_defeated = len(tcstates[opponent_id].units[opponent_id])
      reward_binary = reward_binary_micro(tcstates, player_id)
      reward_retained = min(1.0, units_retained / max(1.0, self._units_total[player_id]))
      reward_defeated = 1.0 - min(1.0, units_defeated / max(1.0, self._units_total[opponent_id]))
      return 0.5 * reward_binary + 0.25 * reward_retained + 0.25 * reward_defeated
    agent_player_id = tcstates[TCAgent.client_id].player_id
    player_ids = [agent_player_id, other_player_id(agent_player_id)]
    return [player_reward(player_id) for player_id in player_ids]

class TC2RewardFullGameBinary(TC2RewardAbstract):
  """
  A binary (0/1) reward function, which terminates using the standard StarCraft termination condition:
  a player has no remaining buildings
  """  
  def _is_alive(self, tcstates, player_id: int) -> bool:
    return any(TCStaticValues['isBuilding'][unit.type] for unit in tcstates[player_id].units[player_id])
  def reward(self, tcstates) -> List[float]:
    agent_player_id = tcstates[TCAgent.client_id].player_id
    player_ids = [agent_player_id, other_player_id(agent_player_id)]
    alive: List[float] = [self._is_alive(tcstates, player_id) for player_id in player_ids]
    return [0.0 for player_id in player_ids] if all(alive) else alive
  def done(self, tcstates) -> bool:
    return max(self.reward(tcstates)) > 0

class TC2RewardResources(TC2RewardAbstract):
  def __init__(self, seconds: int = 180):
    self.seconds = seconds
  def reward(self, tcstates) -> List[float]:
    return [
      tcstate.frame.resources[tcstate.player_id].ore
      + tcstate.frame.resources[tcstate.player_id].gas
      for tcstate in tcstates]
  def done(self, tcstates) -> bool:
    return terminate_timeout(tcstates, seconds = self.seconds)
    
class TC2RewardUnitCount(TC2RewardAbstract):
  """A continuous reward function which measures how many (matching) units the player has at the end of the episode."""
  def __init__(self, seconds: int = 180, unit_criterion: Callable = lambda x: True):
    self.seconds = seconds
    self.unit_criterion = unit_criterion
  def reward(self, tcstates) -> List[float]:
    agent_player_id = tcstates[TCAgent.client_id].player_id
    return [len([unit for unit in tcstates[agent_player_id].units[agent_player_id] if self.unit_criterion(unit)]), 0]
  def done(self, tcstates) -> bool:
    return terminate_timeout(tcstates, seconds = self.seconds)
    
class TC2RewardWorkerCount(TC2RewardUnitCount):
  def __init__(self, seconds: int = 180):
    super().__init__(seconds = seconds, unit_criterion = (lambda unit: TCStaticValues['isWorker'][unit.type]))
    
class TC2RewardMarineCount(TC2RewardUnitCount):
  def __init__(self, seconds: int = 180):
    super().__init__(seconds = seconds, unit_criterion = (lambda unit: unit.type == TCUnits.Terran_Marine))