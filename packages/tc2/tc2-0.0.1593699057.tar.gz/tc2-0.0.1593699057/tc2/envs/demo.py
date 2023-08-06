from tc2.constants import *
from tc2.envs import TC2Env, TC2Behavior
from tc2 import tc2lib
from tc2.agents import attack_closest
from random import randint, sample

class TC2EnvDemo(TC2Env):
  """A simple demo environment that spawns random armies on a standard map and terminates after a few seconds."""

  def __init__(self) -> None:
    super().__init__()
    self.set_map('maps/4fightingspirit.scx')

  def _before_reset(self) -> None:
    self.set_self_play(True)

  def _after_reset(self) -> None:
    self.set_behavior(TCAgent, attack_closest)
    self.set_behavior(TCEnemy, attack_closest)
    units_all = [
      TCUnits.Terran_Marine,
      TCUnits.Terran_Vulture,
      TCUnits.Terran_Siege_Tank_Tank_Mode,
      TCUnits.Terran_Goliath,
      TCUnits.Terran_Ghost,
      TCUnits.Terran_Firebat,
      TCUnits.Terran_Wraith,
      TCUnits.Terran_Battlecruiser,
      TCUnits.Protoss_Zealot,
      TCUnits.Protoss_Archon,
      TCUnits.Protoss_Scout,
      TCUnits.Zerg_Zergling,
      TCUnits.Zerg_Hydralisk,
      TCUnits.Zerg_Mutalisk,
      TCUnits.Zerg_Ultralisk
    ]
    units_sampled = sample(units_all, 3)
    for i in range(len(units_sampled)):
      for _ in range(randint(2, 4)):
        self._spawn(TCAgent, units_sampled[i], 32*32+32*27, 32*32+32*32 + 32*4*(i - 1))
        self._spawn(TCEnemy, units_sampled[i], 32*32+32*37, 32*32+32*32 + 32*4*(i - 1))
    units_sampled = sample(units_all, 3)
    for i in range(len(units_sampled)):
      for _ in range(randint(2, 4)):
        self._spawn(TCAgent, units_sampled[i], 32*32+32*32 + 32*8*(i - 1), 32*40)
        self._spawn(TCEnemy, units_sampled[i], 32*32+32*32 + 32*8*(i - 1), 32*88)

  def _done(self) -> bool:
    return self._agents[TCAgent.client_id].client.state().frame_from_bwapi > 24 * 18 # type: ignore