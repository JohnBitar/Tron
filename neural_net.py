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


from tron_gym import transform_board


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

def train_with_RL(args):
    #game = TronProblem()

    #environment = 0 #our game
    actual_actions = ["U", "D", "L", "R"]
    state_size = 2400 # dependent on our function that converts states
    action_space = 4
    agent = DQNAgent(state_size, action_space)
    done = False
    batch_size = 32

    show_visual = True

    for e in range(EPISODES):
        # initialize the game
        game = TronProblem(args.map, 0)
        state = game.get_start_state()



        # decide which player the DQN agent is going to be
        dqn_player = e % 2
        moves_made_in_game = 0

        # assume the training bot is the first player
        while not (game.is_terminal_state(state)):


            if show_visual:
                print("Training RL BOT to make a move")
                args.visualizer(state, colored)
                time.sleep(0.2)
            # transform the state into something we can feed the agent
            training_state = transform_board(state)
            training_state = np.reshape(training_state, [1, state_size])




            # get the calculated action of the DQN Agent
            rl_action = agent.act(training_state)

            # convert it into an actual action
            action = actual_actions[rl_action]





            # take the action to get into a new state
            next_state = game.transition(state, action)

            # prepare everything for the bot playing against our bots
            # to make the decision
            game.set_start_state(next_state)

            done = False

            reward = 0

            # if the game has ended that means our bot just made
            # a losing move
            if game.is_terminal_state():
                reward = -1
                done = True
                next_training_state = transform_board(next_state)
                next_training_state = np.reshape(next_training_state, [1, state_size])
                agent.remember(training_state, rl_action, reward, next_training_state, done)
                break



            if show_visual:
                print("training RL BOT made a move")
                args.visualizer(state, colored)
                time.sleep(0.2)
            # this upper part was all our training bot

            # this down is the other bot



            # create a deep copy of the game
            exposed = copy.deepcopy(game)




            # let the programmed bot make the decision
            decision = bots[next_state.ptm].decide(exposed)


            # check if it's a legal action
            available_actions = game.get_available_actions(next_state)
            if not decision in available_actions:
                decision = list(available_actions)[0]


            # see the resultant state after the transition
            result_state = game.transition(next_state, decision)
            game.set_start_state(result_state)

            # if we the opponent lead us to a terminal state that means
            # we won
            if game.is_terminal_state():
                reward = 1
                done = True

            # the new state will be the result state
            state = result_state



            # old code
            # action = agent.act(state)
            #
            # next_state, reward, done = environment.step(action)
            # if done:
            #     reward = 0 # change it later
            next_training_state = transform_board(state)
            next_training_state = np.reshape(next_training_state, [1, state_size])

            # remember the transition
            agent.remember(training_state, rl_action, reward, next_training_state, done)



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
