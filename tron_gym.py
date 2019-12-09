from trontypes import CellType

# a function which parses the state of the game into a vector
    # this is one place
        # where the bots will differ, in their implementation of this function
    # questions are what is necessary and sufficient information for the bot to play well

    # examples:
def transform_board(state):
    return_vector = []
    num_rows = len(state.board)
    num_colums = len(state.board[0])
    for row in range(num_rows):
        for column in range(num_colums):
            on_this_place = state.board[row][column]
            this_vector = []
            if on_this_place == CellType.WALL:
                this_vector.append(1)
            else:
                this_vector.append(0)
            if on_this_place == CellType.BARRIER:
                this_vector.append(1)
            else:
                this_vector.append(0)
            if on_this_place == CellType.SPACE:
                this_vector.append(1)
            else:
                this_vector.append(0)
            if on_this_place == CellType.TRAP:
                this_vector.append(1)
            else:
                this_vector.append(0)
            if on_this_place == CellType.SPEED:
                this_vector.append(1)
            else:
                this_vector.append(0)
            if on_this_place == CellType.BOMB:
                this_vector.append(1)
            else:
                this_vector.append(0)
            if on_this_place == CellType.ARMOR:
                this_vector.append(1)
            else:
                this_vector.append(0)
            if on_this_place == '1':
                this_vector.append(1)
            else:
                this_vector.append(0)
            if on_this_place == '2':
                this_vector.append(1)
            else:
                this_vector.append(0)
            # testing purposes
            # if (row < 10):
            #     if (column < 10 ):
            #         return_vector.append((40+row, 40+column))
            #     else:
            #         return_vector.append((40 + row, column))
            # else:
            #     if (column < 10):
            #         return_vector.append((row, 40+ column))
            #     else:
            #         return_vector.append((row, column))
            return_vector.append(this_vector)
    # now return_vector[i][1] specifies if there is a barrier in location corresponding to the i-th number
    # this is one of the things that can be fed into the neural network (in which case there would be 17 * 17 * 9 = 2601 input nodes,
    # though we'd also need to add whether or not the two players have armors or not if this were to be a useful representation

    #print(return_vector)

    return return_vector







# a function which chooses one of our many bots to train on

# a function which chooses our bot's adversery
    # at the beginning this is just ta1, ta2, wallbot, and voroni bot
    # later this changes between them and our bot

# a function which makes the bots play one game on
