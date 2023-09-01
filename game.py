from game_env import GameEnv
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import VecFrameStack, DummyVecEnv
import sys
import os


mode = sys.argv[1]
if mode == "model":
    env = GameEnv()
    env = DummyVecEnv([lambda: env])
    env = VecFrameStack(env, 4, channels_order='last')

    model = DQN.load(os.path.join('models', 'best_model'))
    terminated = False
    score_info = None
    obs = env.reset()
    while not terminated:
        action, _ = model.predict(obs)
        obs, reward, terminated, info = env.step(action)

        score_info = info[0]["score"]
    print('score: ', score_info)

elif mode == "human":
    env = GameEnv()
    env.run_game()
    print('score: ', env.get_score())
