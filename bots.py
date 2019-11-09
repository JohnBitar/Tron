#!/usr/bin/python

import numpy as np
from tronproblem import *
from trontypes import CellType, PowerupType
import random, math
from algorithms import getalphabetaWithN, alpha_beta_cutoff
# Throughout this file, ASP means adversarial search problem.


class StudentBot:
    """ Write your student bot here"""
    
    
    
    

    """
        player location is row, column tuple
        we can call TronProblem
    """
    def voronoi(self, state):
        
         # gets the locations of the players
        locs = state.player_locs
        # gets the board that we're in
        board = state.board
        # gets the player to move (here we don't know if that's us or the opponent)
        ptm = state.ptm
        
        
        #   find where p1 and p2 are
        p1Pos = locs[0]
        p2Pos = locs[1]
        
        # keep track of nodes you're going to visit for both players and those you've visited

        
        
        # keep track of the number of nodes P1 and P2 dominated
        numberP1Dominates = 0
        numberP2Dominates = 0
        
        # keep track of the nodes that have been visited or dominated
        visitedOrDominated = {p1Pos: 0, 
                              p2Pos: 0}
        depth = 0
        
       
        
        
        if (ptm == 0):
            visitedOrDominated[p2Pos] = 1
            p1Frontier = [(p1Pos, 0)]
            p2Frontier = [(p2Pos, 1)]
            frontier_looked_at = p1Frontier
            currentDominatorCount = numberP1Dominates
        else:
            visitedOrDominated[p1Pos] = 1
            p1Frontier = [(p1Pos, 1)]
            p2Frontier = [(p2Pos, 0)]
            frontier_looked_at = p2Frontier
            currentDominatorCount = numberP2Dominates
        
        
        while not (p1Frontier == [] and p2Frontier == []):
            try:
                # what to do when one player stops having things in its frontier
                # pop the current Node and its Depth 
                curNode, curDepth = frontier_looked_at.pop()
                # as long as the current depth is the one we're interested in
                while curDepth == depth:
                    r0, c0 = curNode
                    # for each of the node's neighbors
                    for action in {U, D, L, R}:
                        r1, c1 = TronProblem.move(curNode, action)
                        # which don't have barriers, walls, or other players
                        # and are not visitedOrDominated
                        if not (
                            board[r1][c1] == CellType.BARRIER
                            or board[r1][c1] == CellType.WALL
                            or TronProblem.is_cell_player(board, (r1, c1))
                        ) and not (r1, c1) in visitedOrDominated:
                            # make sure to visit that node in the future
                            frontier_looked_at.append((r1, c1), curDepth+2)
                            # increment the number of nodes P1 dominates
                            currentDominatorCount += 1
                            # say that it is dominated with depth curDepth+1
                            visitedOrDominated[(r1, c1)] = curDepth+2
                    # we check if the next node has the depth we're looking for 
                    #potential error
                    if frontier_looked_at == [] or not frontier_looked_at[0][1] == depth:
                        if (frontier_looked_at is p1Frontier):
                            frontier_looked_at = p2Frontier
                            currentDominatorCount = numberP2Dominates
                        else:
                            frontier_looked_at = p1Frontier
                            currentDominatorCount = numberP1Dominates
                        depth += 1
                        
                        break
                    else:
                        curNode, curDepth = frontier_looked_at.pop()

                       
            except:
                depth += 1
                if (frontier_looked_at is p1Frontier):
                    frontier_looked_at = p2Frontier
                    currentDominatorCount = numberP2Dominates
                else:
                    frontier_looked_at = p1Frontier
                    currentDominatorCount = numberP1Dominates
                break
        while frontier_looked_at:
             curNode, curDepth = frontier_looked_at.pop()
             r0, c0 = curNode
             # for each of the node's neighbors
             for action in {U, D, L, R}:
                r1, c1 = TronProblem.move(curNode, action)
                # which don't have barriers, walls, or other players
                # and are not visitedOrDominated
                if not (
                    board[r1][c1] == CellType.BARRIER
                    or board[r1][c1] == CellType.WALL
                    or TronProblem.is_cell_player(board, (r1, c1))
                ) and not (r1, c1) in visitedOrDominated:
                    # make sure to visit that node in the future
                    # depth doesn't mattter at this stage, just getting there asap!
                    frontier_looked_at.append((r1, c1), depth)
                    # increment the number of nodes P1 dominates
                    currentDominatorCount += 1
                    # say that it is dominated with depth curDepth+1
                    visitedOrDominated[(r1, c1)] = depth

        return numberP1Dominates - numberP2Dominates
    
        # Start with the loop with player_to_play's position
        
    def boardEvaluation(self, state):
        return self.voronoi(self, state)
        return 0
    
    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        # gets the state of the game
        state = asp.get_start_state()
        # gets the locations of the players
        locs = state.player_locs
        # gets the board that we're in
        board = state.board
        # gets the player to move (and knows that's us)
        ptm = state.ptm
        # get our location
        loc = locs[ptm]
        
        
        # initialize the depth of alpha beta
        alpha_beta_depth = 10
        
        return alpha_beta_cutoff(asp, alpha_beta_depth, self.boardEvaluation)

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
        # gets the state of the problem
        state = asp.get_start_state()
        # from the state gets the locations of the players
        locs = state.player_locs
        board = state.board
        # gets the player to move information
        ptm = state.ptm
        # gets the location of the player to move
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
