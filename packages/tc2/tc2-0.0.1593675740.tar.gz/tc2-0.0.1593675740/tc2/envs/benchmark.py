from tc2.constants import *
from tc2.envs import TC2Env
from tc2.rules import *
from random import randint, sample
from typing import List, Tuple
import itertools


class TC2EnvMoveToBeaconReward(TC2RewardAbstract):
  def __init__(self):
    self._wins = 0
  def add_win(self) -> None:
    self._wins += 1
  def reward(self, tcstates) -> List[float]:
    return [self._wins, 0]
  def done(self, tcstates) -> bool:
    return tcstates[0].frame_from_bwapi >= 16 * 120 # PySC2 MoveToBeacon is defined at 120 seconds but 16 FPS, unlike the 24 FPS standard for SC1

class TC2EnvMoveToBeacon(TC2Env):
  """
  Reproduction of the MoveToBeacon scenario from PySC2
  See https://github.com/deepmind/pysc2/blob/master/docs/mini_games.md
  """
  def __init__(self) -> None:
    super().__init__()
    self.walker_type = TCUnits.Terran_Civilian
    self.beacon_type = TCUnits.Zerg_Overlord
    self._reward: TC2EnvMoveToBeaconReward

  def _before_reset(self) -> None:
    self.set_map('maps/empty64.scm')
    self.set_complete_observability(True)
    self.set_reward(TC2EnvMoveToBeaconReward())
  def _random_pixel(self):
    return randint(32 * 3, 32 * 61)
  def _within_distance(self, a: Tuple[int, int], b: Tuple[int, int], distance_max: int) -> bool:
    distance_squared = (a[0] - b[0]) ** 2 + (a[1] - b[1])  ** 2
    distance_max_squared = distance_max ** 2
    return distance_squared <= distance_max_squared    
  def _reset_beacon(self) -> None:
    units = list(itertools.chain.from_iterable(self.get_raw_state().units.values()))
    for unit in units:
      self._kill(unit.id)
    a = None
    b = None
    # Note that this distance check is in pixels
    while a is None or self._within_distance(a, b, 32 * 4):
      a = (self._random_pixel(), self._random_pixel())
      b = (self._random_pixel(), self._random_pixel())
    self._spawn(TCAgent, self.walker_type, a[0], a[1])
    self._spawn(TCEnemy, self.beacon_type, b[0], b[1])
    self.skip_frames_until_commands_executed()
  def _after_step(self) -> None:
    units = list(itertools.chain.from_iterable(self.get_raw_state().units.values()))
    walker = next((unit for unit in units if unit.type == self.walker_type), None)
    beacon = next((unit for unit in units if unit.type == self.beacon_type), None)
    # Note that this distance check is in walktiles (8x8 pixels)
    if walker is not None and beacon is not None and self._within_distance((walker.x, walker.y), (beacon.x, beacon.y), 8 * 2):
      self._reward.add_win()
      self._reset_beacon()
      
  def _after_reset(self) -> None:
    self._reset_beacon()