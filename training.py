from game_env import GameEnv
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import VecFrameStack, DummyVecEnv
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.evaluation import evaluate_policy
import optuna
import os 

CHECK_DIR = './models/'
LOG_DIR = './training_logs/'
OPT_DIR = './models/'

class TrainAndLoggingCallback(BaseCallback):

    def __init__(self, check_freq, save_path, verbose=1):
        super(TrainAndLoggingCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.save_path = save_path

    def _init_callback(self):
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self):
        if self.n_calls % self.check_freq == 0:
            model_path = os.path.join(self.save_path, 'best_model_{}'.format(self.n_calls))
            self.model.save(model_path)

        return True

def objective(trial):
    return {
        'learning_rate': trial.suggest_float('learning_rate', 0.00001, 0.001),
        'gamma': trial.suggest_float('gamma', 0.85, 0.99)
    }

def hyperaparameters_tune(trial):
    try:
        model_params = objective(trial)

        env = GameEnv()
        env = Monitor(env, LOG_DIR)
        env = DummyVecEnv([lambda: env])
        env = VecFrameStack(env, 4, channels_order='last')

        model = DQN('CnnPolicy', env, tensorboard_log=LOG_DIR, verbose=1,  buffer_size=50000, **model_params) 
        model.learn(total_timesteps=3000001) 

        mean_reward, _ = evaluate_policy(model, env, n_eval_episodes=100)
        env.close()
        SAVE_PATH = os.path.join(OPT_DIR,'trial_{}_best_model'.format(trial.number))
        model.save(SAVE_PATH)

        return mean_reward

    except Exception as e:
        return -1000

def train_tune():
    study = optuna.create_study(direction='maximize')
    study.optimize(hyperaparameters_tune, n_trials=5, n_jobs=1)
    
    print("\n")
    print(study.best_params)

def train():
    callback_dqn = TrainAndLoggingCallback(check_freq=300000, save_path=CHECK_DIR)

    env = GameEnv()
    env = Monitor(env, LOG_DIR)
    env = DummyVecEnv([lambda: env])
    env = VecFrameStack(env, 4, channels_order='last')

    model = DQN('CnnPolicy', env, buffer_size=50000, tensorboard_log=LOG_DIR, verbose=1) 
    model.learn(total_timesteps=3000001, callback=callback_dqn)


train()
#train_tune()


'''
DQN(
policy, 
env, 
learning_rate=0.0001,
buffer_size=1000000, 
learning_starts=50000, 
batch_size=32,  
tau=1.0,  
gamma=0.99,
train_freq=4, 
gradient_steps=1, 
replay_buffer_class=None, 
replay_buffer_kwargs=None, 
optimize_memory_usage=False, 
target_update_interval=10000, 
exploration_fraction=0.1, 
exploration_initial_eps=1.0, 
exploration_final_eps=0.05, 
max_grad_norm=10, 

tensorboard_log=None, 
policy_kwargs=None, 
verbose=0, 
seed=None, 
device='auto', 
_init_setup_model=True)
'''

'''
:param policy: The policy model to use (MlpPolicy, CnnPolicy, ...)
:param env: The environment to learn from (if registered in Gym, can be str)
:param learning_rate: The learning rate, it can be a function of the current progress remaining (from 1 to 0)
:param buffer_size: size of the replay buffer
:param learning_starts: how many steps of the model to collect transitions for before learning starts
:param batch_size: Minibatch size for each gradient update
:param tau: the soft update coefficient ("Polyak update", between 0 and 1) default 1 for hard update
:param gamma: the discount factor
:param train_freq: Update the model every ``train_freq`` steps. Alternatively pass a tuple of frequency and unit like ``(5, "step")`` or ``(2, "episode")``.
:param gradient_steps: How many gradient steps to do after each rollout (see ``train_freq``) Set to ``-1`` means to do as many gradient steps as steps done in the environment during the rollout.
:param replay_buffer_class: Replay buffer class to use (for instance ``HerReplayBuffer``). If ``None``, it will be automatically selected.
:param replay_buffer_kwargs: Keyword arguments to pass to the replay buffer on creation.
:param optimize_memory_usage: Enable a memory efficient variant of the replay buffer at a cost of more complexity.
        See https://github.com/DLR-RM/stable-baselines3/issues/37#issuecomment-637501195
:param target_update_interval: update the target network every ``target_update_interval`` environment steps.
:param exploration_fraction: fraction of entire training period over which the exploration rate is reduced
:param exploration_initial_eps: initial value of random action probability
:param exploration_final_eps: final value of random action probability
:param max_grad_norm: The maximum value for the gradient clipping
'''
