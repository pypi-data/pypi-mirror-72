from tc2.constants import *
from tc2.envs import *
from tc2.rules import *
from random import randint, sample

class TC2EnvSymmetrical_Base(TC2Env):
  """Spawns a simple symmetrical battle"""
  def _before_reset(self):
    self.set_map('maps/empty64.scm')
  def _after_reset(self):
    final_counts = self._unit_counts() if callable(self._unit_counts) else self._unit_counts
    for unit_count in final_counts:
      for i in range(unit_count[0]):
        self._spawn(TCAgent, unit_count[1], 32*28, 32*32)
        self._spawn(TCEnemy, unit_count[1], 32*34, 32*32)
  def _unit_counts(self):
    raise NotImplementedError()

class TC2EnvAsymmetrical_Base(TC2Env):
  """Spawns a simple asymmetrical battle"""
  def _before_reset(self):
    self.set_map('maps/empty64.scm')    
  def _after_reset(self):
    final_counts = self._unit_counts() if callable(self._unit_counts) else self._unit_counts
    for unit_count in final_counts[0]:
      for i in range(unit_count[0]):
        self._spawn(TCAgent, unit_count[1], 32*28, 32*32)
    for unit_count in final_counts[1]:
      for i in range(unit_count[0]):
        self._spawn(TCEnemy, unit_count[1], 32*34, 32*32)
  def _unit_counts(self):
    raise NotImplementedError()

class TC2Env5Marine(TC2EnvSymmetrical_Base):
  """Five Marines vs. five Marines"""
  def _unit_counts(self):
    return [(5, TCUnits.Terran_Marine)]

class TC2Env5Zealot(TC2EnvSymmetrical_Base):
  """Five Zealots vs. five Zealots"""
  def _unit_counts(self):
    return [(5, TCUnits.Protoss_Zealot)]

class TC2Env5Mutalisk(TC2EnvSymmetrical_Base):
  """Five Mutalisks vs. five Mutalisks"""
  def _unit_counts(self):
    return [(5, TCUnits.Zerg_Mutalisk)]

class TC2Env3to7Marine(TC2EnvSymmetrical_Base):
  """Each side gets the same random number of Marines between 3 and 7"""
  def _unit_counts(self):
    return [(randint(3, 7), TCUnits.Terran_Marine)]

class TC2Env3to7Zealot(TC2EnvSymmetrical_Base):
  """Each side gets the same random number of Zealots between 3 and 7"""
  def _unit_counts(self):
    return [(randint(3, 7), TCUnits.Protoss_Zealot)]

class TC2Env3to7Mutalisk(TC2EnvSymmetrical_Base):
  """Each side gets the same random number of Mutalisks between 3 and 7"""
  def _unit_counts(self):
    return [(randint(3, 7), TCUnits.Zerg_Mutalisk)]

class TC2EnvVultureZealot(TC2EnvAsymmetrical_Base):
  def __init__(self):
    self.vultures = 1
    self.zealots = 1
    super().__init__()
  """The agent controls a Vulture against an enemy Zealot. The Zealot wins a direct fight, but the Vulture can win by kiting."""
  def _unit_counts(self):
    return [[(self.vultures, TCUnits.Terran_Vulture)], [(self.zealots, TCUnits.Protoss_Zealot)]]

class TC2EnvWraith2Hydralisks(TC2EnvAsymmetrical_Base):
  """The agent controls a Wraith against enemy Hydralisks. The Hydralisks win a direct fight, but the Wraith can win by kiting."""
  def _unit_counts(self):
    return [[(1, TCUnits.Terran_Wraith)], [(2, TCUnits.Zerg_Hydralisk)]]

class TC2EnvMutalisk3Scourge(TC2EnvAsymmetrical_Base):
  """The agent controls a Mutalisk against enemy Scourge. The Scourge win a direct fight, but the Mutalisk can win by kiting."""
  def _unit_counts(self):
    return [[(1, TCUnits.Zerg_Mutalisk)], [(3, TCUnits.Zerg_Scourge)]]

class TC2EnvMarineZealot(TC2EnvAsymmetrical_Base):
  def __init__(self):
    self.marines = 2
    self.zealots = 1
    super().__init__()
  """The agent controls two Marines against an enemy Zealot. The Zealot wins a direct fight, but the Marines can win by kiting."""
  def _unit_counts(self):
    return [[(self.marines, TCUnits.Terran_Marine)], [(self.zealots, TCUnits.Protoss_Zealot)]]

class TC2EnvMacro_Base(TC2Env):
  """The agent starts with a normal Terran base (a Command Center and four SCV workers)"""
  def __init__(self):
    super().__init__()
    self.set_map('maps/2player64long.scm')
    self._complete_observability = True
    self._options.gametype = tc2lib.GameType.Melee
  def _done(self):
    return super()._done() or self._agents[TCAgent.client_id].client.state().frame_from_bwapi >= 24 * 60 * 3  # type: ignore

class TC2EnvFullGame(TC2EnvMacro_Base):
  def __init__(self):
    super().__init__()
    self.set_reward(TC2RewardFullGameBinary())
  def _done(self):
    return super()._done() or self._agents[TCAgent.client_id].client.state().frame_from_bwapi >= 24 * 60 * 60  # type: ignore

class TC2EnvGather(TC2EnvMacro_Base):
  def __init__(self):
    super().__init__()
    self.set_reward(TC2RewardResources())
    
class TC2EnvTrainWorkers(TC2EnvMacro_Base):
  def __init__(self):
    super().__init__()
    self.set_reward(TC2RewardWorkerCount())    
    
class TC2EnvTrainMarines(TC2EnvMacro_Base):
  def __init__(self):
    super().__init__()
    self.set_reward(TC2RewardMarineCount())