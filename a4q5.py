# CMPT 317 A  Python script for playing games

# Copyright (c) 2016-2019 Michael C Horsch,
# Department of Computer Science, University of Saskatchewan

# This file is provided solely for the use of CMPT 317 students.  Students are permitted
# to use this file for their own studies, and to make copies for their own personal use.

# This file should not be posted on any public server, or made available to any party not
# enrolled in CMPT 317.

# This implementation is provided on an as-is basis, suitable for educational purposes only.


import Players
import AlphaBetaDL as DL
from Game import Game
import MinimaxData as Data
# create the game, and the initial state
# game = TicTacToe(depthlimit=2)

for i in range(1,3):

    game = Game(depthlimit=i)


    state = game.initial_state()
    # game.rebel_direction_constraint(state)
    # game.sith_direction_constraint(state)
    # game.jedi_direction_constraints(state)
    # print(game.actions(state))
    # game.result(state,['REBEL', [2, 5], 'UP', 1, [1, 5]])
    # state.display()

    # game1 = TicTacToe(depthlimit=4)


    # set up the players
    # current_player = Players.VerboseComputer(game, Searcher.MinimaxData(game))
    # current_player = Players.HumanMenu(game)

    current_player = Players.VerboseComputer(game, DL.AlphaBetaDL(game))



    other_player = Players.VerboseComputer(game, DL.AlphaBetaDL(game))
    # other_player = Players.HumanMenu(game)


    # play the game
    while not game.is_terminal(state):
        #show the board out of courtesy
        state.display()

        # ask the current player for a move
        choice = current_player.ask_move(state)

        print(game.actions(state))

        # check the move
        assert choice in game.actions(state), "The action <{}> is not legal in this state".format(choice)

        # apply the move
        state = game.result(state, choice)

        # swap the players
        current_player, other_player = other_player, current_player

    # game's over
    state.display()
    game.congratulate(state)
    print(" ")
    print("##########################################################################################################################################")
    print("##########################################################################################################################################")
    print("##########################################################################################################################################")
    print("Finished the depth limit")
    print("##########################################################################################################################################")
    print("##########################################################################################################################################")
    print("##########################################################################################################################################")
    print(" ")

    # eof




