from game_env import GameEnv
from stable_baselines3 import DQN
from stable_baselines3.common import env_checker
from stable_baselines3.common.vec_env import VecFrameStack, DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
from matplotlib import pyplot as plt
import random
import os


def env_test():
    env = GameEnv()
    env_checker.check_env(env)

    for i in range(3):
        reward_total = 0
        terminated = False
        env.reset()
        while not terminated:
            action = random.randint(0, 3)
            obs, reward, terminated, info = env.step(action) 
            reward_total += reward
            env.render()
    
            print('obs shape ', obs.shape)
            print('obs type', obs.dtype)
            print('reward ', reward)
            print('terminated', terminated)

        print('Episode:{} Score:{} Reward:{}'.format(i, env.get_score(), reward_total))

def env_frame_test():
    env = GameEnv()
    s = env.reset()
    print(s.shape)

    env = DummyVecEnv([lambda: env])
    s = env.reset()
    print(s.shape)

    obs, reward, terminated, info = env.step([0]) 
    plt.imshow(obs[0], cmap='gray')
    plt.show(block=False)
    plt.pause(1)
    plt.close()

    env = VecFrameStack(env, 4, channels_order='last') 
    s = env.reset()
    print(s.shape)
    obs, reward, terminated, info = env.step([0])
    obs, reward, terminated, info = env.step([1])
    obs, reward, terminated, info = env.step([1])
    obs, reward, terminated, info = env.step([1])

    plt.figure(figsize=(10,8))
    for idx in range(4):
        plt.subplot(1,4,idx+1)
        plt.imshow(obs[0][:,:,idx], cmap='gray')
    plt.show() 
    plt.show(block=False)
    plt.pause(15)
    plt.close()

def eval():
    x = 0
    s = ""
    env = GameEnv()
    env = DummyVecEnv([lambda: env])
    env = VecFrameStack(env, 4, channels_order='last')
    for i in range(10):
        x += 300000
        s = "best_model_" + str(x)
        

        env = GameEnv()
        env = DummyVecEnv([lambda: env])
        env = VecFrameStack(env, 4, channels_order='last')
        
        model = DQN.load(os.path.join('models', s))
        mean_reward, _ = evaluate_policy(model, env, n_eval_episodes=100)
        print(s + "   " + str(mean_reward) + "\n")
        
        del env


eval()
#env_test()
#env_frame_test()
