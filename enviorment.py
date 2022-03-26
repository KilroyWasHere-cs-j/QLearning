import numpy as np
import os
import time
from LoadConfig import loader


class Env:

    def __init__(self):
        self.parser = loader()
        e = self.parser.get_enviorment()
        self.height = e[0]  # 8
        self.width = e[1]  # 52
        self.startX = e[2]  # 20
        self.startY = e[3]  # 7
        self.posX = self.startX
        self.posY = self.startY
        self.endX = e[4]  # 10
        self.endY = e[5]  # 2
        self.actions = [0, 1, 2, 3]
        self.stateCount = self.height * self.width
        self.actionCount = len(self.actions)
        self.wallX = [0, 3, 0, 3, 23, 23, 22, 22, 21, 21, 24, 24, 51, 51, 48, 48, 24, 21]  # Side to side
        self.wallY = [0, 0, 2, 2, 4, 3, 4, 3, 4, 3, 4, 3, 5, 7, 5, 7, 8, 5]  # Up and down
        self.pastSteps = []
        self.count = 0
        self.resets = 0
        self.render_walls = True
        self.wallHits = 0


    def reset(self):
        self.posX = self.startX
        self.posY = self.startY
        self.done = False
        self.resets = self.resets + 1
        return 0, 0, False

    # take action
    def step(self, action):
        self.pastSteps.append(action)
        if action == 0:  # left
            self.posX = self.posX - 1 if self.posX > 0 else self.posX
        if action == 1:  # right
            self.posX = self.posX + 1 if self.posX < self.width - 1 else self.posX
        if action == 2:  # up
            self.posY = self.posY - 1 if self.posY > 0 else self.posY
        if action == 3:  # down
            self.posY = self.posY + 1 if self.posY < self.height - 1 else self.posY

        done = self.posX == self.endX and self.posY == self.endY
        # mapping (x,y) position to number between 0 and 5x5-1=24
        nextState = self.width * self.posY + self.posX
        reward = 1 if done else 0
        # 1 if done else 0
        if self.posX == self.wallX[0] and self.posY == self.wallY[0]:
            reward = 0
            done = False
            self.wallHits = self.wallHits + 1
            self.reset()
        elif self.posX == self.wallX[1] and self.posY == self.wallY[1]:
            reward = 0
            done = False
            self.wallHits = self.wallHits + 1
            self.reset()
        elif self.posX == self.wallX[2] and self.posY == self.wallY[2]:
            reward = 0
            done = False
            self.wallHits = self.wallHits + 1
            self.reset()
        elif self.posX == self.wallX[3] and self.posY == self.wallY[3]:
            reward = 0
            done = False
            self.wallHits = self.wallHits + 1
            self.reset()
        elif self.posX == self.wallX[4] and self.posY == self.wallY[4]:
            reward = 0
            self.reset()
            self.wallHits = self.wallHits + 1
            done = False
        elif self.posX == self.wallX[5] and self.posY == self.wallY[5]:
            reward = 0
            done = False
            self.wallHits = self.wallHits + 1
            self.reset()
        elif self.posX == self.wallX[6] and self.posY == self.wallY[6]:
            reward = 0
            done = False
            self.wallHits = self.wallHits + 1
            self.reset()
        elif self.posX == self.wallX[7] and self.posY == self.wallY[7]:
            reward = 0
            done = False
            self.wallHits = self.wallHits + 1
            self.reset()
        elif self.posX == self.wallX[8] and self.posY == self.wallY[9]:
            reward = 0
            done = False
            self.wallHits = self.wallHits + 1
            self.reset()
        elif self.posX == self.wallX[9] and self.posY == self.wallY[9]:
            reward = 0
            done = False
            self.wallHits = self.wallHits + 1
            self.reset()
        elif self.posX == self.wallX[10] and self.posY == self.wallY[10]:
            reward = 0
            done = False
            self.reset()
        elif self.posX == self.wallX[11] and self.posY == self.wallY[11]:
            reward = 0
            done = False
            self.wallHits = self.wallHits + 1
            self.reset()
        elif self.posX == self.wallX[12] and self.posY == self.wallY[12]:
            reward = 0
            done = False
            self.wallHits = self.wallHits + 1
            self.reset()
        elif self.posX == self.wallX[13] and self.posY == self.wallY[13]:
            reward = 0
            done = False
            self.wallHits = self.wallHits + 1
            self.reset()
        elif self.posX == self.wallX[14] and self.posY == self.wallY[14]:
            reward = 0
            done = False
            self.wallHits = self.wallHits + 1
            self.reset()
        elif self.posX == self.wallX[15] and self.posY == self.wallY[15]:
            reward = 0
            done = False
            self.wallHits = self.wallHits + 1
            self.reset()
        elif self.posX == self.wallX[16] and self.posY == self.wallY[16]:
            reward = 0
            done = False
            self.wallHits = self.wallHits + 1
            self.reset()
        elif self.posX == self.wallX[17] and self.posY == self.wallY[17]:
            reward = 0
            done = False
            self.wallHits = self.wallHits + 1
            self.reset()


        return nextState, reward, done

    # return a random action
    def randomAction(self):
        return np.random.choice(self.actions)

    def get_pose(self):
        return self.posX, self.posY

    def is_done(self):
        return self.done

    def get_past_actions(self):
        return self.pastSteps

    # display environment
    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.posY == i and self.posX == j:
                    print("O", end='')
                elif j == self.startX and i == self.startY:
                    print("S", end='')
                elif self.endY == i and self.endX == j:
                    print("T", end='')
                elif self.wallX[0] == j and self.wallY[0] == i:
                    print("X", end='')
                elif self.wallX[1] == j and self.wallY[1] == i:
                    print("X", end='')
                elif self.wallX[2] == j and self.wallY[2] == i:
                    print(  "X", end='')
                elif self.wallX[3] == j and self.wallY[3] == i:
                    print(  "X", end='')
                elif self.wallX[4] == j and self.wallY[4] == i:
                    print(  "X", end='')
                elif self.wallX[4] == j and self.wallY[4] == i:
                    print(  "X", end='')
                elif self.wallX[5] == j and self.wallY[5] == i:
                    print(  "X", end='')
                elif self.wallX[6] == j and self.wallY[6] == i:
                    print(  "X", end='')
                elif self.wallX[7] == j and self.wallY[7] == i:
                    print(  "X", end='')
                elif self.wallX[8] == j and self.wallY[8] == i:
                    print(  "X", end='')
                elif self.wallX[9] == j and self.wallY[9] == i:
                    print(  "X", end='')
                elif self.wallX[10] == j and self.wallY[10] == i:
                    print(  "X", end='')
                elif self.wallX[11] == j and self.wallY[11] == i:
                    print(  "X", end='')
                elif self.wallX[12] == j and self.wallY[12] == i:
                    print(  "X", end='')
                elif self.wallX[13] == j and self.wallY[13] == i:
                    print(  "X", end='')
                elif self.wallX[14] == j and self.wallY[14] == i:
                    print(  "X", end='')
                elif self.wallX[15] == j and self.wallY[15] == i:
                    print(  "X", end='')
                elif self.wallX[16] == j and self.wallY[16] == i:
                    print(  "X", end='')
                elif self.wallX[17] == j and self.wallY[17] == i:
                    print(  "X", end='')
                else:
                    print(".", end='')
            print("")

    def replay(self):
        print("Starting replay")
        for h in self.pastSteps:
            os.system('clear')
            self.render()
            self.step(h)
            time.sleep(0.05)
        print("Replay done")
