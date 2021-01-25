#!/usr/bin/env python
# coding: utf-8
# USDJPY with DQN
# [Original](https://gist.github.com/tsu-nera/d801fab3100c8c2f29b0ed6927c4355a/)

# dukascopyからヒストリカルデータをダウンロードする。
# - https://www.dukascopy.com/swiss/english/marketwatch/historical

# How to execute: $ python main.py

from lib import *
import const

const.SCALING = 10000 
const.T = 1200      # final time step T of one episode
const.MA_WIN1 = 120 # Moving Average Window
const.MA_WIN2 = 80
const.MA_WIN3 = 50
const.MA_WIN4 = 30
const.MA_WIN5 = 20
const.LOG_DIR = './result_MA3/'
const.LOG_PER_STEP = const.LOG_DIR + 'log_per_step_'
const.LOG_PER_EP   = const.LOG_DIR + 'log_per_episode_'

class HistData():
    def __init__(self, csv_path, date_range=None):
        self.csv_path = csv_path
        f = '%d.%m.%Y %H:%M:%S.%f'
        my_parser = lambda date: pd.datetime.strptime(date, f)
        self.csv_data = pd.read_csv(self.csv_path, index_col=0, parse_dates=True, header=0,
                                   date_parser=my_parser)
        self.csv_name = os.path.basename(self.csv_path)
        self.date_range = date_range
        self.TARGET = 'Close'

    def set_date_range(self, date_range):
        self.date_range = date_range

    def data(self):
        if self.date_range is None:
            return self.csv_data
        else:
            return self.csv_data[self.date_range]

    def max_value(self):
        return self.data()[[self.TARGET]].max()[self.TARGET]

    def min_value(self):
        return self.data()[[self.TARGET]].min()[self.TARGET]

    def dates(self):
        return self.data().index.values

    def plot(self):
        fig, ax = plt.subplots()
        ax.plot(self.data()[[self.TARGET]])
        fig.tight_layout()
        fig.savefig(const.LOG_DIR + self.csv_name + ".png")

    def list(self):
        l = []
        for close in self.data()[[self.TARGET]].iterrows():
            l.append(close[1][0])
        return l



class Trading():
    def __init__(self):
        self.reset()

    def reset(self):
        self._ac_pl = 0    # Accumulated Profit and Loss
        self.reset_liq()

    def reset_liq(self): # reset when liquidating
        self._position = Position.SQUARE.value
        self._pos_rate = 0 # the exchange rate when taking the position (Normalize)

    def is_square(self):
        return self._position == Position.SQUARE.value

    def change(self, action, pos_rate: float):
        if self._position != Position.SQUARE.value:
            raise ValueError("The position is not SQUARE when taking a position")
        if type(pos_rate) is not float and type(pos_rate) is not int:
            raise TypeError("The pos_rate type is neither float nor int. type={}, pos_rate={}".format(type(pos_rate), pos_rate))
        
        self._pos_rate = pos_rate
        if action == Action.SHORT.value:
            self._position = Position.SHORT.value
        elif action == Action.LONG.value:
            self._position = Position.LONG.value
        else:
            raise ValueError("action is neither SHORT nor LONG. action={}".format(action))
        
    def liquidate(self, cu):
        pl = self.calc_pl(cu) # profit and loss
        if pl == None:
            raise ValueError("The position is neither LONG nor SHORT when liquidating")
        self._ac_pl += pl
        debug_print2("pl={} self._ac_pl={}".format(pl, self._ac_pl))
        self.reset_liq()
        return pl
    
    def calc_pl(self, cu): # calculate profit and loss
        fpl = None
        if self._position == Position.LONG.value:
            fpl = (cu - self._pos_rate) * const.SCALING
        elif self._position == Position.SHORT.value:
            fpl = (self._pos_rate - cu) * const.SCALING
        return fpl


# memo: https://moriokalab.com/news/57
class FXTrade(gym.core.Env):
    def __init__(self, hist_list, kind):
        self.action_space = gym.spaces.Discrete(len(Action))
        high = np.array([ 2.0, max([e.value for e in Position]),  2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0])
        low  = np.array([-2.0, min([e.value for e in Position]), -2.0,-2.0,-2.0,-2.0,-2.0,-2.0,-2.0])
        # The elements of high and low (max and min) in self.observation_space:
        # 1st: Current exchange rate: Cu 
        # 2nd: Position: pos
        # 3rd: Moving Average: ma1
        # 4rd: Moving Average: ma2
        # 5rd: Moving Average: ma3
        # 6rd: Moving Average: ma4
        # 7rd: Moving Average: ma5
        # 8th: Floating Profid and Loss: fpl
        # 9th: the exchange rate when taking the position: pos_rate
        # commeting out 6th: metrics 1: met1
        # commeting out 7th: metrics 2: met2
        # commeting out 8th: metrics 3: met3
        # *All elements are normalized except the position
        self.observation_space = gym.spaces.Box(low=low, high=high)
        self.reset_FXTrade()
        self._trading = Trading()
        self._hist_list = hist_list
        self._hist_list_len = len(self._hist_list)
        # for result log
        self._1st_header_step = True
        self._1st_header_ep = True
        self._log_per_step = []
        self._kind = kind
        self._ep_inc = False # episode increment flag
        self._episode = 1

    def step(self, action):
        reward = None
        cu = self._hist_list[self.cur_id] # current rate
        ma1 = stat.mean(self._hist_list[self.cur_id-const.MA_WIN1:self.cur_id])
        ma2 = stat.mean(self._hist_list[self.cur_id-const.MA_WIN2:self.cur_id])
        ma3 = stat.mean(self._hist_list[self.cur_id-const.MA_WIN3:self.cur_id])
        ma4 = 0
        ma5 = 0
        fpl = 0 if self._trading.calc_pl(cu) == None else self._trading.calc_pl(cu)/const.SCALING

        self.cur_id +=1
        done = True if self.cur_id == self._hist_list_len else False

        if done == True: # Force the agent to liquidate when an episode finishes
            action = Action.LIQUIDATE.value

        if not self.is_valid_action(action):
            reward = 0 # No Penalty for taking invalid action
        else:
            reward = 0  # No Reward for taking valid action
            if action == Action.WAIT.value:
                pass
            elif self._trading.is_square():
                if action != Action.LIQUIDATE.value:
                    self._trading.change(action, cu)
                else:
                    raise ValueError("The action must be SHORT or LONG in SQUARE. _position={}, action={}, _pos_rate={}".format(
                            self._trading._position, action, self._trading._pos_rate))
            else: # When position is SHORT or LONG
                if action == Action.LIQUIDATE.value:
                    reward += self._trading.liquidate(cu)
                else:
                    raise ValueError("_position={}, action={}, _pos_rate={}".format(
                        self._trading._position, action, self._trading._pos_rate))

        # observation element
        oe = [cu, self._trading._position, ma1, ma2, ma3, ma4, ma5, fpl, self._trading._pos_rate]
        if reward == None:
            raise ValueError("reward is not set: oe={}".format(oe))
        elif None in oe:
            raise ValueError("observation element includes invalid value: oe={}".format(oe))
        observation = np.array(oe)
        self.ac_rw += reward
        # result log
        self._log_per_step = [self.cur_id,  self._trading._ac_pl, self.ac_rw, reward, self._trading._position, action, fpl, cu, ma1, ma2, ma3, ma4, ma5]
        if done == True:
            df = pd.DataFrame([[self._episode, self._trading._ac_pl, self.ac_rw]],
                columns=['episode', 'accumulated P/L','accumulated reward'])
            df.to_csv(const.LOG_PER_EP + self._kind + '.csv', mode='a', index=False, header=self._1st_header_ep)
            if self._1st_header_ep == True:
                self._1st_header_ep = False
            self._ep_inc = True
            
        return observation, reward, done ,{}  # {} means "info" which is not used

    def render(self, mode='human'): # Set visualize=True on fit() and test()
        df = pd.DataFrame([self._log_per_step],
            columns=['current ID', 'accumulated P/L','accumulated reward', 'reward', 'position', 'action', 'fpl', 'cu', 'ma1', 'ma2', 'ma3', 'ma4', 'ma5'])
        df.to_csv(const.LOG_PER_STEP + self._kind + '_ep' + str(self._episode) + '.csv', mode='a', index=False, header=self._1st_header_step)
        if self._1st_header_step == True:
            self._1st_header_step = False
        if self._ep_inc == True:
            self._ep_inc = False
            self._episode += 1
            self._1st_header_step = True
  
    def reset(self):
        self.reset_FXTrade()
        self._trading.reset()
        ma1 = stat.mean(self._hist_list[self.cur_id-const.MA_WIN1:self.cur_id])
        ma2 = stat.mean(self._hist_list[self.cur_id-const.MA_WIN2:self.cur_id])
        ma3 = stat.mean(self._hist_list[self.cur_id-const.MA_WIN3:self.cur_id])
        ma4 = 0
        ma5 = 0
        # TODO: # Think about validity of setting　0.0 on 5th element (pos_rate) as initial value
        return np.array([self._hist_list[self.cur_id], self._trading._position, ma1, ma2, ma3, ma4, ma5, 0.0, 0.0])
    
    def reset_FXTrade(self):
        self.cur_id = const.MA_WIN1
        self.ac_rw  = 0 # accumulated reward

    def is_valid_action(self, action):
        if self._trading.is_square():
            if (action == Action.WAIT.value or 
                action == Action.LONG.value or 
                action == Action.SHORT.value):
                return True
        else:
            if (action == Action.WAIT.value or 
                action == Action.LIQUIDATE.value):
                return True
        return False


def normalize(hist):
    # Normalize the history data because normalizing narrows the range between max and min
    # in the observation (state) space to reduce computational complexity.
    mean = np.mean(hist.list())
    hist_list = hist.list() - mean 
    hist_list = hist_list[0:const.T]
    fig, ax = plt.subplots()
    fig.tight_layout()
    ax.plot(np.linspace(0,const.T, const.T), hist_list)
    fig.savefig(const.LOG_DIR + hist.csv_name + "_dev.png")  # _dev: _deviation
    hist_list = hist_list.tolist()
    return hist_list

def gen_env(csv_path, kind='train'): # generate environment
    hist = HistData(csv_path=csv_path)
    hist.plot()
    hist_list = normalize(hist)

    env = FXTrade(hist_list, kind)
    return env

def gen_multi_env(dir, kind='test'): # generate multiple environments
    env_list = []
    id = 0
    for csv in natsorted(glob.glob(dir)):
        id += 1
        env = gen_env(csv, kind + str(id))
        env.reset()
        env_list.append(env)
    return env_list

def rm_glob(wild):
    for filename in glob.glob(wild):
        os.remove(filename)

def main():
    try:
        rm_glob(const.LOG_DIR + "*.csv")
        rm_glob(const.LOG_DIR + "*.png")      
    except FileNotFoundError:
        pass

    train_csv = '../data/train/USDJPY_Candlestick_5_M_BID_01.01.2004-10.01.2004.csv'
    train_env = gen_env(train_csv)
    train_env.reset()

    test_envs = gen_multi_env('../data/test/*csv')

    nb_actions = train_env.action_space.n
    model = Sequential()
    model.add(Flatten(input_shape=(1,) + train_env.observation_space.shape))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('linear'))
    model.summary()

    memory = SequentialMemory(limit=50000, window_length=1)
    policy = BoltzmannQPolicy()
    dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory,
                target_model_update=1e-2, policy=policy)
    # metrics(評価関数) https://note.com/randr_inc/n/n643873336995
    # 分類の時には'acuracy'、回帰の時には'mae': Mean Absolute Error(平均絶対誤差)
    dqn.compile(Adam(lr=1e-3), metrics=['mae']) 
    dqn.fit(train_env, nb_steps=50000, visualize=True, verbose=1)
    for test_env in test_envs:
        # nb_episodes=1 because the environment acts the exact same way as other episodes
        # in my research setting.
        dqn.test(test_env, nb_episodes=1, visualize=True, verbose=1) 

if __name__ == '__main__':
    main()