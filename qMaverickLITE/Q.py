from enviorment import Env
import numpy as np
import time
import os
import csv
from Server import sender
from LoadConfig import loader


def get_local_path():
    return os.getcwd()

def write_actions(step, pastActions, pathName):
    try:
        # /media/gabriel/DD2D-1A4E/q-learning/
        file = open(get_local_path() + "/actions" + str(pathName) + ".csv", "w")
        file.write(str(pastActions))
        file.close()
    except:
        exit("Couldn't find actions.csv")


def write_xys(step, pastXY, pathName):
    try:
        file = open(get_local_path() + "/xys" + str(pathName) + ".csv", "w")
        file.write(str(pastXY))
        file.close()
    except:
        exit("Couldn't find xys.csv")


def write_qtables(qtable, pathName):
    try:
        np.savetxt(get_local_path() + "/qtables" + str(pathName) + ".csv", qtable,
                   delimiter=",")
    except:
        exit("Couldn't find qtables.csv")


# noinspection PySimplifyBooleanCheck
class QLib:

    def __init__(self):
        self.env = Env()
        self.serv = sender()
        self.parser = loader()
        self.serv.handShake()

    def load_qtable(self, pathName):
        results = []
        with open(get_local_path() + "/qtables" + pathName + ".csv") as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
            for row in reader:  # each row is a list
                results.append(row)
            return results

    # Get the optimal path
    def get_optimal(self):
        return min(self.pastStepCounts)

    # Run the Q learning model
    def run(self):
        self.t0 = time.time()
        self.t1 = 0
        # print(self.load_qtable())
        # QTable : contains the Q-Values for every (state,action) pair
        # qtable = np.random.rand(self.env.stateCount, self.env.actionCount).tolist()

        # hyperparameters
        q = self.parser.get_Q()
        m = self.parser.get_meta_data()
        self.epochs = int(q[0])
        self.gamma = q[1]
        self.epsilon = q[2]
        self.decay = q[3]
        self.epochCount = 0
        self.pastStepCounts = []
        self.optimal = 0
        self.lastOptimal = 0
        self.optimalRepeats = 0
        self.pastActions = []
        self.pastPoses = []
        self.name = m[0]
        self.version = m[1]
        self.modelNumber = m[2]
        self.modelName = m[3]
        self.lastModelName = m[4]
        self.usePreTrained = m[5]
        self.render = m[6]
        self.render_times = m[7]

        if "true" in self.usePreTrained:
            qtable = self.load_qtable(pathName=self.lastModelName)
        else:
            qtable = np.random.rand(self.env.stateCount, self.env.actionCount).tolist()
        print(self.name)
        print(self.version)
        print("Use pretrained Q Table", self.usePreTrained)

        # training loop
        render_count = 0
        for i in range(self.epochs):
            state, reward, done = self.env.reset()
            steps = 0
            while not done:
                render_count += 1

                if "false" in self.render:
                        os.system('clear')
                        print("Epsilon: ", self.epsilon)
                        print("Epochs: ", self.epochCount, "/", self.epochs)
                        print("Past epoch step counts: ", self.pastStepCounts)
                        print("Step: ", steps)
                        print("Current optimal output: ", self.optimal)
                        print("Resets: ", self.env.resets)
                        print("Attempts to phase through a wall: ", self.env.wallHits)
                        print("Last optimal: ", self.lastOptimal)
                        self.env.render()
                        time.sleep(0.05)
                # elif "false" in self.render:
                #     pass
                # count steps to finish game
                steps += 1

                # act randomly sometimes to allow exploration
                if np.random.uniform() < self.epsilon:
                    action = self.env.randomAction()
                # if not select max action in Qtable (act greedy)
                else:
                    action = qtable[state].index(max(qtable[state]))

                self.pastActions.append(action)
                self.pastPoses.append(self.env.get_pose())
                # take action
                next_state, reward, done = self.env.step(action)
                # update qtable value with Bellman equation
                qtable[state][action] = reward + self.gamma * max(qtable[next_state])
                # update state
                state = next_state
                # print("Past actions ", self.pastActions)
                if done:
                    self.env.reset()
                    self.pastStepCounts.append(steps)
                    self.epochCount += 1
                    self.epsilon -= self.decay * self.epsilon
                    self.optimal = self.get_optimal()
                    write_actions(step=steps, pastActions=self.pastActions, pathName=self.modelName)
                    write_qtables(qtable=qtable, pathName=self.modelName)
                    write_xys(step=steps, pastXY=self.pastPoses, pathName=self.modelName)
                    if steps == self.optimal:
                        self.optimalRepeats = self.optimalRepeats + 1
                        if self.optimalRepeats > 4:
                            self.t1 = time.time()
                            print(self.t1 - self.t0)
                            print("Start Pose", self.env.get_start())
                            print("End Pose", self.env.get_end())
                            print("Current Pose", self.pastPoses[-1])
                            self.serv.send(self.pastPoses)
                            exit("SOLVED WITH " + str(self.optimal) + " AS THE OPTIMAL PATH")
                        else:
                            self.pastActions.clear()
                            self.pastPoses.clear()
                    else:
                        self.optimalRepeats = 0
                    steps = 0
                    done = False
            # env.replay()
            time.sleep(0.8)
        exit("EXITED")
