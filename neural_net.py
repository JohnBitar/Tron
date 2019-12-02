# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 08:25:27 2019

@author: PC
"""

import numpy as np
import random
from collections import deque
from keras.models import Sequential
from keras.layer import Dense
from keras.optimiyers import Adam


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95 # discount rate
        self.epsilon = 1.0 # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self.build_model()
    
    # could generalize to number of layers and nodes in them 
    def build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])
    
    def replay(self, batch_size):
        minibatch = random.sample(self.memort, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward = self.gamma * np.amax(self.mode.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def load(self, name):
        self.model.load_weights(name)
    
    def save(self, name):
        self.model.save_weigths(name)
    
EPISODES = 1000
def train_with_RL():
    #game = TronProblem()
    environment = 0 #our game 
    state_size = 2400 # dependent on our function that converts states
    action_space = 4
    agent = DQNAgent(state_size, action_space)
    done = False
    batch_size = 32
    for e in range(EPISODES):
        state = environment.reset()
        state = np.reshape(state, [1, state_size])
        for time in range(400):
            action = agent.act(state)
            next_state, reward, done = environment.step(action)
            if done:
                reward = 0 # change it later
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                print("episode: {}/{}, score: {}, e: {:.2}"
                      .format(e, EPISODES, time, agent.epsilon))
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
        if e%10 == 0:
            agent.save("./save/neural-net-dqn.h5")

def train_with_SL():
    return 0
    