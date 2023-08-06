# TorchCraft 2 [![CircleCI](https://circleci.com/gh/fairinternal/TorchCraft2.svg?style=svg&circle-token=6181f15b3ed51c760ace7cfdefda6f8a18dc5c1b)](https://circleci.com/gh/fairinternal/TorchCraft2)
### *(aka StarCraft Gym)*

The fastest, easiest way to use *StarCraft* as a reinforcement learning environment.

And all you have to do to get started is `pip install` it.

## Motivation

Researchers are eager to use *StarCraft*-based environments for RL experiments. But the process of getting *StarCraft* up and running can be time-consuming, and most environments aren't easy to use out of the box.

TorchCraft 2 offers simple (one-touch!) installation, an easy-to-use Gym interface, and multiple challenges/baselines out of the box.

In addition, we've worked with Blizzard to allow to TorchCraft 2 to include *first* legal distribution of *StarCraft: Brood War* binaries. This will enable the public to use TorchCraft 2 without having to acquire their own copies of *StarCraft*, or having to install it.

See the [project proposal](https://fb.quip.com/kzrHA90kEEMY) for details.

## Roadmap

With those ready, we're aiming to launch TorchCraft 2 internally for experiments and beta testing. From there, the plan is:
* Integration with TorchCraft (deprecating the original Lua/Python APIs)
* Pre-compiled binary distribution on PyPy
* Public release, PR, and tutorial content

The full roadmap lives [on GitHub](https://github.com/fairinternal/FAIR_rush/projects/21)

## Usage
### Building TorchCraft 2 for development

This is how I recommend using TorchCraft 2 at the moment:

```
git clone --recursive https://github.com/fairinternal/TorchCraft2/ tc2
cd tc2

conda create --name tc2 python=3 pip
source activate tc2
conda install pip cmake pybind11 numpy
conda install -y -c conda-forge sdl2 zstd
conda install -y -c anaconda zeromq
pip install -e .
```

### Downloading required Starcraft files
Once you have installed `tc2`, you have to download StarCraft data files (*MPQ files*). We provide you with
a tool to do that just for you - we can't provide them right away because we need you to read and accept Blizzard's EULA first.

```
tc2-setup
```


### Demo

This demo (`run_demo.py`) creates a StarCraft gym environment and controls an agent using a simple "attack the middle" policy.

```
import gym
import tc2
from tc2.agents import attack_middle

env = gym.make('tc2-demo-v0')
while True:
  env.reset()
  actions = []
  done = False
  while not done:
    observation, reward, done, info = env.step(actions)
    actions = attack_middle(observation)
```

### Running the TorchCraft 2 demo:

* `python3 run_demo.py`
