#!/usr/bin/python

import numpy as np
from tronproblem import *
from trontypes import CellType, PowerupType
import random, math
from algorithms import getalphabetaWithN, alpha_beta_cutoff
from queue import Queue
from collections import deque
# Throughout this file, ASP means adversarial search problem.


class StudentBot:
    def __init__(self):
        self.BOT_NAME = "GIBS"
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


        frontier_looked_at = []
        p1Frontier = deque()
        p2Frontier = deque()
        if (ptm == 0):
            visitedOrDominated[p2Pos] = 1
            p1Frontier.append((p1Pos, 0))
            p2Frontier.append((p2Pos, 1))
            frontier_looked_at = p1Frontier
            currentDominatorCount = numberP1Dominates
        else:
            visitedOrDominated[p1Pos] = 1
            p1Frontier.append((p1Pos, 1))
            p2Frontier.append((p2Pos, 0))
            frontier_looked_at = p2Frontier
            currentDominatorCount = numberP2Dominates

        #print("start of something new")
        curDepth = 0
        curNode = 0
        while (p1Frontier or p2Frontier):
            #print("in whil")
            try:
                # what to do when one player stops having things in its frontier
                # pop the current Node and its Depth
                #print("try")
                #print("lala ", frontier_looked_at[0])

                curNode, curDepth = frontier_looked_at.popleft()
                #print("heer")
                # as long as the current depth is the one we're interested in
                while curDepth == depth:
                    r0, c0 = curNode
                    # for each of the node's neighbors
                    #print(r0, c0, "| Depth", curDepth)
                    for action in {U, D, L, R}:

                        r1, c1 = TronProblem.move(curNode, action)
                        #
                        #print("child", r1, c1)
                        # which don't have barriers, walls, or other players
                        # and are not visitedOrDominated
                        if not (
                            board[r1][c1] == CellType.BARRIER
                            or board[r1][c1] == CellType.WALL
                            or TronProblem.is_cell_player(board, (r1, c1))
                        ) and not (r1, c1) in visitedOrDominated:

                            #print("this one is getting it", currentDominatorCount)
                            # make sure to visit that node in the future
                            frontier_looked_at.append(((r1, c1), curDepth+2))
                            # increment the number of nodes P1 dominates
                            currentDominatorCount += 1
                            # say that it is dominated with depth curDepth+1
                            visitedOrDominated[(r1, c1)] = curDepth+2
                    # we check if the next node has the depth we're looking for
                    #potential error
                    #print("here")
                    if not (frontier_looked_at and frontier_looked_at[0][1] == depth):
                        #print("now ")
                        if (frontier_looked_at is p1Frontier):
                            frontier_looked_at = p2Frontier
                            numberP1Dominates = currentDominatorCount
                            currentDominatorCount = numberP2Dominates
                        else:
                            #print("lala ")
                            frontier_looked_at = p1Frontier
                            numberP2Dominates = currentDominatorCount
                            currentDominatorCount = numberP1Dominates
                        depth += 1

                        break
                    else:
                        curNode, curDepth = frontier_looked_at.popleft()


            except:
                #print(frontier_looked_at)
                depth += 1
                if (frontier_looked_at is p1Frontier):
                    frontier_looked_at = p2Frontier
                    numberP1Dominates = currentDominatorCount
                    currentDominatorCount = numberP2Dominates
                else:
                    frontier_looked_at = p1Frontier
                    numberP2Dominates = currentDominatorCount
                    currentDominatorCount = numberP1Dominates
                #print("we're here")
                break
        #print("out")
        while frontier_looked_at:

             #print("curDept", curDepth, curNode)
             curNode, curDepth = frontier_looked_at.popleft()
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
                    frontier_looked_at.append(((r1, c1), curDepth+2))
                    # increment the number of nodes P1 dominates
                    currentDominatorCount += 1
                    # say that it is dominated with depth curDepth+1
                    visitedOrDominated[(r1, c1)] = depth
        #print(curNode, " | ", currentDominatorCount)
        #print(numberP1Dominates, "voronoia before ", numberP2Dominates)
        if frontier_looked_at is p1Frontier:
            numberP1Dominates = currentDominatorCount
        else:
            numberP2Dominates = currentDominatorCount
        #print("numberP1Dominates", numberP1Dominates, "|", numberP2Dominates)
        #print(numberP1Dominates, "voronoia ", numberP2Dominates)
        score = (numberP1Dominates - numberP2Dominates)
        #print(numberP1Dominates ,"|", numberP2Dominates)
        return score

        # Start with the loop with player_to_play's position
    playerNum = 0
    def boardEvaluation(self, state):
        #print("evaluate", self.playerNum)
        if self.playerNum:
            return 1/2 - self.voronoi(state)/512
        else:
            return 1/2 + self.voronoi(state)/512

    movesMade = 0
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
        #print("player to move", ptm)
        if ptm:
            self.playerNum = ptm
        self.movesMade += 1
        print(self.movesMade)
        # initialize the depth of alpha beta

        if self.movesMade < 20:
            alpha_beta_depth = 5
        elif self.movesMade < 35:
            alpha_beta_depth = 6
        elif self.movesMade < 45:
            alpha_beta_depth = 7
        elif self.movesMade < 60:
            alpha_beta_depth = 8
        elif self.movesMade < 90:
            alpha_beta_depth = 9
        elif self.movesMade < 120:
            alpha_beta_depth = 11
        else:
            alpha_beta_depth = 13
        #alpha_beta_depth = 7
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
