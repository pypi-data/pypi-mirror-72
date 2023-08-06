from gym.envs.registration import register
import platform
import sys
from pathlib import Path
from typing import NewType, List, Optional, Union

# Verify Python version
if sys.version_info[0] < 3 or "64bit" not in platform.architecture()[0]:
    raise AssertionError('TorchCraft2 requires 64-bit Python version 3+')

# tc2lib is the C++ backend for tc2. it needs to be compiled for the same minor
# version of Python. For example, a Python 3.6 tc2lib won't work in Python 3.7.
#
# Attempting to import a version-mismatched tc2lib fails with a generic
# (and unhelpful) message about the module being missing.
# So let's provide a more helpful error message.

try:
  # Try importing tc2 as an installed package
  from . import tc2lib
  bwenv_path = Path(tc2lib.__file__).parent / "BWEnv"
  bwapilauncher_path = Path(tc2lib.__file__).parent / "bin" / "BWAPILauncher"
except ImportError as error:
  message = f"""Failed to import TorchCraft2\'s backend, tc2lib.

It may be missing, or has been compiled for a different Python version.
1. If you are on the tc2 github repository, you should install tc2 with `pip install -e .`
2. Check the Python version indicated by tc2lib\'s file name.
For example, `tc2lib.cpython-36m-x86_64-linux-gnu.so` indicates Python 3.6.
You\'re running: Python {sys.version}.

Upstream error:
{error}
  """
  raise ImportError(message)


def check_mpq_path(mpq_path: Path) -> None:
  for mpq_file in ["Patch_rt.mpq", "BrooDat.mpq", "StarDat.mpq"]:
    if not (mpq_path / mpq_file).is_file():
      raise RuntimeError(f"""Unable to find `{mpq_file}` (supposed to be in `{mpq_path}`).
If you just installed tc2, you need to agree to Blizzard's EULA and download Starcraft MPQ files.
Please run `tc2-setup` in a terminal to do so.
""")


class _Paths:
  def __init__(self):
    self._bwenv: Optional[str] = None
    self._bwapilauncher: Optional[str] = None
    self._mpq: Optional[str] = None

  @property
  def bwenv(self) -> Union[str, Path]:
    assert self._bwenv is not None
    return self._bwenv

  @bwenv.setter
  def bwenv(self, value: Union[str, Path]) -> None:
    self._bwenv = str(value)
    tc2lib.set_paths(bwenv=self._bwenv)

  @property
  def bwapilauncher(self) -> Union[str, Path]:
    assert self._bwapilauncher is not None
    return self._bwapilauncher

  @bwapilauncher.setter
  def bwapilauncher(self, value: Union[str, Path]) -> None:
    self._bwapilauncher = str(value)
    tc2lib.set_paths(bwapilauncher=self._bwapilauncher)

  @property
  def mpq(self) -> Union[str, Path]:
    assert self._mpq is not None
    return self._mpq

  @mpq.setter
  def mpq(self, value: Union[str, Path]) -> None:
    check_mpq_path(Path(value))
    self._mpq = str(value)
    tc2lib.set_paths(mpq=self._mpq)

paths = _Paths()
paths.bwenv = bwenv_path
paths.bwapilauncher = bwapilauncher_path
paths.mpq = Path(__file__).parent.resolve().absolute() / "starcraft"

register(id='tc2-demo-v0', entry_point='tc2.envs:TC2EnvDemo')
register(id='tc2-movetobeacon-v0', entry_point='tc2.envs:TC2EnvMoveToBeacon')
register(id='tc2-5marine-v0', entry_point='tc2.envs:TC2Env5Marine')
register(id='tc2-5zealot-v0', entry_point='tc2.envs:TC2Env5Zealot')
register(id='tc2-5mutalisk-v0', entry_point='tc2.envs:TC2Env5Mutalisk')
register(id='tc2-3to7marine-v0', entry_point='tc2.envs:TC2Env3to7Marine')
register(id='tc2-3to7zealot-v0', entry_point='tc2.envs:TC2Env3to7Zealot')
register(id='tc2-3to7mutalisk-v0', entry_point='tc2.envs:TC2Env3to7Mutalisk')
register(id='tc2-vulturezealot-v0', entry_point='tc2.envs:TC2EnvVultureZealot')
register(id='tc2-wraith2hydralisk-v0', entry_point='tc2.envs:TC2EnvWraith2Hydralisks')
register(id='tc2-mutalisk3scourge-v0', entry_point='tc2.envs:TC2EnvMutalisk3Scourge')
register(id='tc2-marinezealot-v0', entry_point='tc2.envs:TC2EnvMarineZealot')
register(id='tc2-fullgame-v0', entry_point='tc2.envs:TC2EnvFullGame')
register(id='tc2-gather-v0', entry_point='tc2.envs:TC2EnvGather')
register(id='tc2-trainworkers-v0', entry_point='tc2.envs:TC2EnvTrainWorkers')
register(id='tc2-trainmarines-v0', entry_point='tc2.envs:TC2EnvTrainMarines')


CommandType = List[int]
FrameNum = int
UnitId = int

__version__ = "0.0.1593699057"
