import logging
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
import multiprocessing
import uuid
import traceback
from typing import Callable, Dict, List, Optional, Tuple, Union, overload
from gym.core import Env
from gym import spaces
import numpy
from tc2 import tc2lib, CommandType
from tc2.constants import *
from tc2.agents import do_nothing
from tc2.rules import reward
from tc2.tools import *

tech_bits = [1 << bit for bit in range(0, len(TCTechs.ids))]
upgrade_bits = [1 << bit for bit in range(0, len(TCUpgrades.ids))]
def make_player_feature(tcstate: tc2lib.State, player_id: int) -> numpy.ndarray:
  return [
    int(tcstate.player_info[player_id].race == TCRaces.Terran),
    int(tcstate.player_info[player_id].race == TCRaces.Protoss),
    int(tcstate.player_info[player_id].race == TCRaces.Zerg),
    int(tcstate.player_info[player_id].race == TCRaces.Unknown),
    int(tcstate.player_info[player_id].has_left),
    0 if player_id not in tcstate.frame.resources else tcstate.frame.resources[player_id].ore,
    0 if player_id not in tcstate.frame.resources else tcstate.frame.resources[player_id].gas,
    0 if player_id not in tcstate.frame.resources else tcstate.frame.resources[player_id].used_psi,
    0 if player_id not in tcstate.frame.resources else tcstate.frame.resources[player_id].total_psi
  ] + [int(tcstate.frame.resources[player_id].techs & bit > 0) for bit in tech_bits
  ] + [int(tcstate.frame.resources[player_id].upgrades & bit > 0) for bit in upgrade_bits]

def make_player_features(tcstate: tc2lib.State) -> numpy.ndarray:
  features = [make_player_feature(tcstate, player_id) for player_id in [tcstate.player_id, other_player_id(tcstate.player_id)]]
  output = numpy.array(features)
  return output
    
class TC2PlayerUnitFeatures:
  def __init__(self, tcstate: tc2lib.State, player_id: int):
    features = tc2lib.featurize_units(tcstate, player_id)
    self.ids = features.ids()
    self.data = features.data()
    self.positions = features.positions()

class TC2UnitFeatures:
  def __init__(self, tcstate: tc2lib.State):
    self.agent: TC2PlayerUnitFeatures = TC2PlayerUnitFeatures(tcstate, tcstate.player_id)
    self.enemy: TC2PlayerUnitFeatures = TC2PlayerUnitFeatures(tcstate, other_player_id(tcstate.player_id))
    self.neutral: TC2PlayerUnitFeatures = TC2PlayerUnitFeatures(tcstate, TCNeutralPlayerId)

class TC2Observation:
  def __init__(self, tcstate: tc2lib.State, features_map_static: numpy.ndarray):
    features_map_dynamic = tc2lib.featurize_map_dynamic(tcstate)
    features_map = features_map_static + features_map_dynamic
    self.players: numpy.ndarray = make_player_features(tcstate)
    self.map: numpy.ndarray = numpy.concatenate(features_map, axis = 0)    
    self.units: TC2UnitFeatures = TC2UnitFeatures(tcstate)
    self.raw = tcstate

class TC2Agent:
  def __init__(self, player: TCPlayer):
    self.player: TCPlayer = player
    self.client = None
    self.queued_commands: List[List[int]] = [[]]
    self.options: tc2lib.GamePlayerOptions = tc2lib.GamePlayerOptions()
    self.cvis: Optional[CVisDumper] = None

  def close(self) -> None:
    if self.client is None:
      return
    self.client.close()
    self.client = None
    if self.cvis is not None:
      try:
        self.cvis.write_trace()
      except NameError:
        # NameError: name 'open' is not defined
        # We can fail writing trace if this is called at exit
        pass
    self.cvis = None

class TC2Behavior:
  def __init__(self, behavior: Callable[[tc2lib.State], List[List[int]]]):
    self.on_frame = behavior

class TC2Game:
  def __init__(self, self_play: bool, options: tc2lib.GameOptions, agents: List[TC2Agent]):
    self._id: str = str(uuid.uuid4())
    self._tcgame = (tc2lib.GameMultiPlayer if self_play else tc2lib.GameSinglePlayer)(
      options,
      agents[TCAgent.client_id].options,
      agents[TCEnemy.client_id].options)
    self._loggers: Dict[str, logging.Logger] = {}

class TC2Env(Env):  # type: ignore
  metadata = {"render.modes": ["human"]}
  
  def __init__(self) -> None:
    self._game: Optional[TC2Game] = None
    self._out_of_game_loggers: Dict[str, logging.Logger] = {}
    self._log_level_cvis: int = logging.DEBUG
    self._log_level_stdout: int = logging.WARNING
    self._agents: Tuple[TC2Agent, TC2Agent] = (TC2Agent(TCAgent), TC2Agent(TCEnemy))
    self._behaviors: List[TC2Behavior] = [TC2Behavior(do_nothing), TC2Behavior(do_nothing)]
    self._options: tc2lib.GameOptions = tc2lib.GameOptions()
    self._static_features: Optional[numpy.ndarray] = None
    self.set_game_type(TCGameTypes.UseMapSettings)
    self.set_complete_observability(True)
    self.set_reward(reward.TC2RewardMicroContinuousCount())
    self.set_self_play(False)
    self.set_map('maps/2player64long.scm')
    self.set_gui(True)
    self.set_frame_delay(0)
    self.set_stepsize(1)
    self.set_name(TCAgent, 'Agent')
    self.set_name(TCEnemy, 'Enemy')
    self.set_race(TCAgent, TCRaces.Terran)
    self.set_race(TCEnemy, TCRaces.Terran)
    
  def __del__(self):
    self.close()

  ##################
  # Public Gym API #
  ##################
          
  def step(self, actions_agent: List[CommandType]=[], actions_enemy: List[CommandType]=[]) -> Tuple[TC2Observation, float, bool, dict]:
    """
    Standard Gym API method.
    Executes actions. Returns the new state.
    @action A list of TorchCraft commands.
    @returns A new TorchCraft state.
    """
    if self._agents[TCAgent.client_id].client is None: self.reset()
    self._before_step()
    for _ in range(self._stepsize):
      self._step_one_frame(actions_agent, actions_enemy)
    self._after_step()
    observation: TC2Observation = self.get_observation()
    reward: float = self._get_rewards()[TCAgent.client_id]
    done: bool = self._done()
    for player in TCPlayers:
      logger = self.get_logger(player)
      logger.log(logging.DEBUG, f'Got state for frame {self._get_tcstate(TCAgent).frame_from_bwapi}')
      if done:
        logger.log(logging.INFO, 'Episode complete. Rewards: ' + str(reward))
    self.action_space = self.get_action_space(observation)
    return observation, reward, done, {}
    
  def reset(self) -> None:
    """
    Standard Gym API method.
    Ends the current episode (if one is running) by calling close().
    Starts a new episode.

    @max_retries Game starts can fail under certain conditions; this argument indicates a number of times to retry starting
    """
    self.get_logger().log(logging.INFO, 'Resetting')
    self._assert_multiprocessing()
    try:
      self.close()
      self.get_logger().log(logging.DEBUG, 'Creating game')
      self.action_space = spaces.Box(low=0, high=0, shape=(0,0), dtype=numpy.float32)
      self._options.replaypath = ''
      self._before_reset()
      self._game = TC2Game(self._self_play, self._options, list(self._agents))
      self.get_logger().log(logging.DEBUG, 'Creating client 0')
      self._agents[0].client = self._game._tcgame.make_client0() # type: ignore
      self.get_logger().log(logging.DEBUG, 'Created client 0')
      if self._self_play:
        self.get_logger(TCEnemy).log(logging.DEBUG, 'Creating client 1')
        self._agents[1].client = self._game._tcgame.make_client1()  # type: ignore
        self.get_logger(TCEnemy).log(logging.DEBUG, 'Created client 1')

      # Add CheryVis replay if requested
      if self._options.replaypath != '':
        for agent, name in zip(self._agents, ['', 'Opponent']):
          if agent.client is not None:
            # TODO: FIXME: The global logger has already been created, add the CherryVis Hook
            cvis = CVisDumper(self._options.replaypath, name)
            cvis.add_logger(self.get_logger(agent.player), -1, self._log_level_cvis)
            agent.cvis = cvis

      self.set_frame_delay(self._delay_milliseconds)
      if (self._complete_observability):
        self._command([tc2lib.Constants.map_hack])
      self._command([tc2lib.Constants.set_cmd_optim, 1])
      self._after_reset()
      self.skip_frames_until_commands_executed()
    except:
      self.get_logger().error(traceback.format_exc())
      
  def render(self, mode: str='human') -> None:
    """
    Standard Gym API method.
    Unused, because rendering is controlled by OpenBW.
    See @set_gui().
    """
    pass
    
  def close(self) -> None:
    """
    Standard Gym API method.
    Ends the current episode (if one is running).
    """
    self.get_logger().log(logging.INFO, 'Closing environment')

    # If we are generating a replay, we want to properly end the game
    client = self._agents[TCAgent.client_id].client
    if client is not None and self._options.replaypath != '':
      for agent in self._agents:
        if agent.client is not None:
          agent.client.send([[int(tc2lib.Constants.commands.quit)]])
      while not client.state().game_ended:
        for a in self._agents:
          if a.client is not None:
            a.client.recv()
    for agent in self._agents:
      agent.close()
    self._game = None
    self._static_features = None

  ###########################
  # Public TC2-specific API #
  ###########################
  
  def get_logger(self, player: TCPlayer = TCAgent, unit_id: int = -1) -> logging.Logger:
    if self._game is None:
      # Out of game logging
      player = TCAgent
      assert(unit_id == -1)
      logger_name = 'gameNONE'
      loggers_dict = self._out_of_game_loggers
    else:
      unit_suffix = f'_u{unit_id}' if unit_id >= 0 else ''
      logger_name = f'game{self._game._id}_client{player.client_id}{unit_suffix}'
      loggers_dict = self._game._loggers

    if logger_name not in loggers_dict:
      logger = logging.getLogger(logger_name)
      logger.setLevel(logging.DEBUG)

      # Logging to stdout
      formatter = logging.Formatter(
        '%(asctime)s %(filename)s:%(lineno)s] %(levelname).1s - %(message)s'
      )
      ch = logging.StreamHandler()
      ch.setLevel(self._log_level_stdout)
      ch.setFormatter(formatter)
      logger.addHandler(ch)

      # Logging to cvis
      if self._game is not None:
        player_obj = self._agents[player.client_id]
        if player_obj.cvis is not None:
          player_obj.cvis.add_logger(logger, unit_id, self._log_level_cvis)

      loggers_dict[logger_name] = logger
    return loggers_dict[logger_name]
    
  def get_raw_state(self, player: TCPlayer = TCAgent) -> tc2lib.State:
    """
    Returns the raw TorchCraft state for the given player.
    """
    self._assert_player_controllable(player)
    client = self._agents[player.client_id].client
    assert(client is not None)
    return client.state()
    
  def get_observation(self, player: TCPlayer = TCAgent) -> TC2Observation:
    self._record_static_features()
    return TC2Observation(self.get_raw_state(player), self._static_features)

  def get_action_space(self, observation: TC2Observation) -> spaces.Space:
    return spaces.Box(low=1e-12, high=1e12, shape=command_tensor_shape(observation), dtype=numpy.float32)
    
  def set_self_play(self, value: bool) -> None:
    """
    Sets whether the next episode is self-play (ie. one agent controlling each player).
    Has no effect on any episode currently running.
    """
    # TODO: Ensure reasonable states whenever this is called
    self._self_play = value

  def set_game_type(self, value: TCGameTypes) -> None:
    """Sets the game type (eg. Melee, Custom)"""
    self._options.gametype = value

  def set_map(self, map_path: str) -> None:
    """
    Sets a map to use in the next episode.
    Has no effect on any episode currently running.
    """
    self._options.map = str(map_path)    
  def set_complete_observability(self, enabled: bool) -> None:
    """
    Sets whether to grant players complete observability.
    Has no effect on any episode currently running.
    """
    self._complete_observability = enabled
  def add_replay(self, path: str, cvis: bool = True) -> None:
    """
    Specifies where the replay for this game should be saved.
    """
    self._options.set_replaypath(path)
  def set_gui(self, enabled: bool) -> None:
    """
    Enables or disables graphics in the next episode.
    Has no effect on any episode currently running.
    """
    self._options.gui = bool(enabled)
  def set_frame_delay(self, delay_milliseconds: int) -> None:
    """
    Changes the game speed by specifying a delay in milliseconds between frames.
    0 (no delay between frames) is the fastest possible speed.
    24 (24ms delay between frames) is what humans usually use.
    In the StarCraft UI, 24ms is the speed named "fastest".
    """
    self._delay_milliseconds = delay_milliseconds
    self._command([tc2lib.Constants.set_speed, self._delay_milliseconds])
  def set_name(self, player: TCPlayer, name: str) -> None:
    """
    Specifies a name for a player.
    Player names appear in replays.
    """    
    self._assert_player(player)
    self._agents[player.client_id].options.name = name
  def set_race(self, player: TCPlayer, race: int) -> None:
    self._assert_player(player)
    self._agents[player.client_id].options.race = TCRaces.ids[race]
    
  @overload
  def set_behavior(self, player: TCPlayer, behavior: TC2Behavior) -> None: ...    
  @overload
  def set_behavior(self, player: TCPlayer, behavior: Callable[[TC2Observation], List[List[int]]]) -> None: ...  
  def set_behavior(self, player: TCPlayer, behavior) -> None:
    """
    Specifies a behavior for a controllable player.
    Player will automatically perform the behavior's actions in addition to any specified in step().
    """
    self._assert_player_controllable(player)
    self._behaviors[player.client_id] = behavior if isinstance(behavior, TC2Behavior) else TC2Behavior(behavior)
    
  def get_trace_dumper(self, player: TCPlayer) -> Optional[CVisDumper]:
    return self._agents[player.client_id].cvis  
  def set_log_level(self, stdout: Optional[int] = None, cvis: Optional[int] = None) -> None:
    """
    Sets logging verbosity level. Lower values means more logging
    Levels are numerical values (logging.DEBUG, ...)
    """
    if stdout is not None:
      self._log_level_stdout = stdout
    if cvis is not None:
      self._log_level_cvis = cvis
      
  def set_reward(self, rew: reward.TC2RewardAbstract) -> None:
    self._reward = rew

  def set_stepsize(self, stepsize: int) -> None:
    assert(stepsize > 0)
    self._stepsize = stepsize
    
  def skip_frames_until_commands_executed(self) -> None:
    """
    Skips (steps) through game frames until any queued commands would have been executed and reflected in the game state.
    
    Context:
    When you issue commands to StarCraft, there is a latency period before the game state reflects those commands:
    https://tl.net/blogs/519872-towards-a-good-sc-bot-p56-latency
    Most confusingly this affects kill() and spawn() commands.
    """
    delay_frames = 3 if self._self_play else 1
    for i in range(delay_frames):
      self._step_one_frame()

  ##################################
  # Final protected helper methods #
  ##################################
  
  def _assert_multiprocessing(self) -> None:
    process = multiprocessing.current_process().name
    # Known MyPy typechecking issue: Typeshed thinks the argument to get_start_method() is required:
    # https://github.com/python/mypy/issues/500
    start_method = multiprocessing.get_start_method() # type: ignore
    assert process == 'MainProcess' or start_method == 'spawn', """
      TorchCraft 2 can be run in subprocesses, but those subprocesses must be spawned, not forked.
      Call `multiprocessing.set_start_method('spawn')` prior to spawning new TorchCraft 2 processes."""      
  def _assert_player(self, player: TCPlayer) -> None:
    assert(player in [TCAgent, TCEnemy, TCNeutral]), f'Invalid player {player}. Valid players are {TCAgent}, {TCEnemy}, and {TCNeutral}.'
  def _assert_player_controllable(self, player: TCPlayer) -> None:
    self._assert_player(player)
    assert(player is not TCNeutral), 'The neutral player can not peform actions.'
    assert(player is TCAgent or (player is TCEnemy and self._self_play)), 'The enemy player can only perform actions in self-play mode.'
  def _get_tcstate(self, player: TCPlayer = TCAgent) -> tc2lib.State:
    self._assert_player(player)
    if self._agents[player.client_id].client is None:
      player = TCAgent
    agent = self._agents[player.client_id]
    assert(agent.client is not None)
    return agent.client.state()
  def _command(self, command: CommandType) -> None:
    self._command0(command)
    self._command1(command)
  def _command0(self, command: CommandType) -> None:
    self._agents[0].queued_commands.append(command)
  def _command1(self, command: CommandType) -> None:
    self._agents[1].queued_commands.append(command)
  def _spawn(self, player: TCPlayer, unit: int, x: int, y: int) -> None:
    self.get_logger(player).log(logging.DEBUG, f'Spawning a Unit-{unit} for player {player} at ({x}, {y})')
    player_id = player.player_id(self._get_tcstate())
    self._command0(command_spawn(player_id, unit, x, y)) #TODO
    self._reward.on_spawn(player_id, unit)
  def _kill(self, unit_id: int) -> None:
    self._command0(command_kill(unit_id))
  def _upgrade(self, player: TCPlayer, upgrade: int, level: int=1) -> None:
    self._assert_player(player)
    self._command0(command_upgrade(player.player_id(self._get_tcstate()), upgrade, level))  #TODO
  def _research(self, player: TCPlayer, tech: int, researched: bool=True) -> None:
    self._assert_player(player)
    self._command0(command_research(player.player_id(self._get_tcstate()), tech, researched))  #TODO
  def _record_static_features(self) -> None:
    assert(self._agents[0].client is not None)
    if self._static_features is None:
      self._static_features = tc2lib.featurize_map_static(self._agents[0].client.state())
  def _step_one_frame(self, actions_agent: List[CommandType]=[], actions_enemy: List[CommandType]=[]) -> None:
    """
    Advances the game one frame without invoking step hooks or generating an observation.
    Intended for manipulating the state in between fast-reset episodes.
    """
    commands = [agent.queued_commands for agent in self._agents]
    commands[TCAgent.client_id] += actions_agent
    commands[TCAgent.client_id] += self._behaviors[TCAgent.client_id].on_frame(self._get_tcstate(TCAgent))
    if (self._self_play):
      commands[TCEnemy.client_id] += actions_enemy
      commands[TCEnemy.client_id] += self._behaviors[TCEnemy.client_id].on_frame(self._get_tcstate(TCEnemy))
    for cmds, agent, player in zip(commands, self._agents, TCPlayers):
      if agent.client is not None:
        if agent.cvis is not None:
          agent.cvis.on_send(cmds)
        self.get_logger(player).log(logging.DEBUG, f'{player} sending commands: {str(cmds)}')
        agent.client.send(cmds)
        self.get_logger(player).log(logging.DEBUG, f'{player} sent commands')
        agent.queued_commands = [[]]
    for agent, player in zip(self._agents, TCPlayers):
      if agent.client is not None:
        self.get_logger(player).log(logging.DEBUG, f'{player} receiving state.')
        agent.client.recv()
        self.get_logger(player).log(logging.DEBUG, f'{player} received state.')
        if agent.cvis is not None:
          agent.cvis.step(agent.client.state())

  ################################
  # Protected hooks for override #
  ################################
  
  def _before_reset(self) -> None:
    """Invoked prior to constructing a new StarCraft game."""
    """Can be used to change OpenBW settings like GUI/no GUI, map, etc."""
    pass
  def _after_reset(self) -> None:
    """Invoked after constructing a new StarCraft game."""
    """Can be used to customize game state by specifying unit spawns."""
    pass
  def _before_step(self) -> None:
    """Invoked on each frame of the game, prior to advancing the state."""
    pass
  def _after_step(self) -> None:
    """Invoked on each frame of the game, after advancing the state."""
    pass
  def _get_rewards(self) -> List[float]:
    """Returns the reward for each player. The reward function is specified via set_reward()"""
    return self._reward.reward([self._get_tcstate(TCAgent), self._get_tcstate(TCEnemy)])
  def _done(self) -> bool:
    return (
      self._get_tcstate(TCAgent).game_ended
      or self._get_tcstate(TCAgent).game_won
      or (self._self_play and self._get_tcstate(TCEnemy).game_ended)
      or (self._self_play and self._get_tcstate(TCEnemy).game_won)
      or self._reward.done([self._get_tcstate(TCAgent), self._get_tcstate(TCEnemy)]))
