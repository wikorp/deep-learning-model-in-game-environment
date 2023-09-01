from utils import screen_height, screen_width
from level import Level
from map import Map
from gym import Env
from gym.spaces import Box, Discrete
from matplotlib import pyplot as plt
import numpy as np
import cv2
import pygame
import sys


class GameEnv(Env):
    def __init__(self):
        super().__init__()    
        self.observation_space = Box(low=0, high=255, shape=(145,105,1), dtype=np.uint8) 
        self.action_space = Discrete(4)
        # 0 jump  # 1 left  # 2 right  # 3 none

        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.level = Level(Map().layout, self.screen)
        self.reset()

    def step(self, action):
        reward = self.level.step(action)
        observation = self.get_obs()

        terminated = False
        if self.level.check_end():
            terminated = True

        info = {"score": self.get_score()}
        return observation, reward, terminated, info
            
    def get_obs(self):
        self.render_obs()

        cap = pygame.surfarray.array2d(pygame.display.get_surface())  # x, y
        cap = cap.T  # y, x changing to cv2 and box format
        cap = cap.astype(np.uint8)  # y, x resize needs unint8 and box needs also uint8
        cap = cv2.resize(cap, (105, 145))  # y, x (x, y) function needs arguments in that order
        cap = np.reshape(cap, (145, 105, 1))  # changing to cv2 and box format
        self.cap = cap
        return cap
    
    def render_obs(self): 
        self.screen.fill('Black')
        self.level.render()
        pygame.display.update()
        self.clock.tick(60)

    def render(self):
        plt.imshow(self.cap, cmap='gray')
        plt.show(block=False)
        plt.pause(1)
        plt.close() 

    def reset(self):
        self.level.reset(Map().layout)
        observation = self.get_obs()
        info = {}
        return observation

    def close(self):
        pygame.display.quit()
        pygame.quit()

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('Black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(60)

            if self.level.check_end():
                break
    
    def get_score(self):
        return self.level.get_score()
