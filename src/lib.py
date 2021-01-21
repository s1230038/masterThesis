import numpy as np
from matplotlib import pyplot as plt
from debug_tools import *
import os
import glob
import pandas as pd
import gym
import gym.spaces
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam
from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
import statistics as stat
from natsort import natsorted

from enum import Enum, unique
@unique
class Position(Enum):
	SQUARE = 0
	SHORT  = 1
	LONG   = 2

@unique
class Action(Enum):
	WAIT      = 0
	SHORT     = 1
	LONG      = 2
	LIQUIDATE = 3