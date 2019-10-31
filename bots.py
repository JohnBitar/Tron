#!/usr/bin/python

import numpy as np
from tronproblem import *
from trontypes import CellType, PowerupType
import random, math

# Throughout this file, ASP means adversarial search problem.


class StudentBot:
    """ Write your student bot here"""
    
    
    
    
    def getalphabetaWithN(self, asp, state, youPlayer, getMax,alpha, beta, n, funct):
        if asp.is_terminal_state(state):
            return asp.evaluate_state(state)[youPlayer]
        if n==0:
            return funct(state)
    
        returnVal = 0
        alp= alpha
        bet= beta
        if getMax:
            returnVal = float("-inf")
            for action in asp.get_available_actions(state):
                successor = asp.transition(state, action)
                successorScore = self.getalphabetaWithN(self, asp, successor, youPlayer, False, alp, bet, n-1, funct)
                if successorScore > returnVal:
                    returnVal = successorScore
                if alp < successorScore:
                    alp= successorScore
                if bet <= alp:
                    break
        else:
            returnVal = float("inf")
            for action in asp.get_available_actions(state):
                successor = asp.transition(state, action)
                successorScore = self.getalphabetaWithN(self, asp, successor, youPlayer, True, alp, bet, n-1, funct)
                if successorScore < returnVal:
                    returnVal = successorScore
                if bet > successorScore:
                    bet = successorScore
                if bet <= alp:
                    break
        return returnVal
    
    def alpha_beta_cutoff(self, asp, cutoff_ply, eval_func):
        """
    	This function should:
    	- search through the asp using alpha-beta pruning
    	- cut off the search after cutoff_ply moves have been made.
    
    	Inputs:
    		asp - an AdversarialSearchProblem
    		cutoff_ply- an Integer that determines when to cutoff the search
    			and use eval_func.
    			For example, when cutoff_ply = 1, use eval_func to evaluate
    			states that result from your first move. When cutoff_ply = 2, use
    			eval_func to evaluate states that result from your opponent's
    			first move. When cutoff_ply = 3 use eval_func to evaluate the
    			states that result from your second move.
    			You may assume that cutoff_ply > 0.
    		eval_func - a function that takes in a GameState and outputs
    			a real number indicating how good that state is for the
    			player who is using alpha_beta_cutoff to choose their action.
    			You do not need to implement this function, as it should be provided by
    			whomever is calling alpha_beta_cutoff, however you are welcome to write
    			evaluation functions to test your implemention. The eval_func we provide
                does not handle terminal states, so evaluate terminal states the
                same way you evaluated them in the previous algorithms.
    
    	Output: an action(an element of asp.get_available_actions(asp.get_start_state()))
    	"""
    
    
        # get the starting state from which you are calculating what move to take
        STARTSTATE = asp.get_start_state()
    
        # get which player you are
        IAMPLAYER = STARTSTATE.player_to_move()
        # initialiye alpha
        alp = float("-inf")
    
        # initialize beta
        bet = float("inf")
    
        # keep track of the action to take
        actionToTake = 0
        score = float("-inf")
        for action in asp.get_available_actions(STARTSTATE):
            successor = asp.transition(STARTSTATE, action)
            successorScore = self.getalphabetaWithN(self, asp, successor, IAMPLAYER, False, alp, bet, cutoff_ply-1, eval_func)
    
            if successorScore > score:
                score = successorScore
                actionToTake= action
            if alp < successorScore:
                alp= successorScore
            if bet <= alp:
                break
    
        return actionToTake
        pass

    def boardEvaluation(self, board):
        return 0
    
    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if possibilities:
            return random.choice(possibilities)
        return "U"

    def cleanup(self):
        """
        Input: None
        Output: None

        This function will be called in between
        games during grading. You can use it
        to reset any variables your bot uses during the game
        (for example, you could use this function to reset a
        turns_elapsed counter to zero). If you don't need it,
        feel free to leave it as "pass"
        """
        pass


class RandBot:
    """Moves in a random (safe) direction"""

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if possibilities:
            return random.choice(possibilities)
        return "U"

    def cleanup(self):
        pass


class WallBot:
    """Hugs the wall"""

    def __init__(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def cleanup(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if not possibilities:
            return "U"
        decision = possibilities[0]
        for move in self.order:
            if move not in possibilities:
                continue
            next_loc = TronProblem.move(loc, move)
            if len(TronProblem.get_safe_actions(board, next_loc)) < 3:
                decision = move
                break
        return decision
