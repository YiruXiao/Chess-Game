import random as rand

class GameState(object):
    """ The GameState class stores the information about the state of the game.
    """
    _ablank = ' '
    _anS = 'S'
    _anR = 'R'
    _anJ = 'J'

    def __init__(self):
        # the gameState dictionary stores the position of each piece

        self.gameState = dict()
        # print(self.gameState)
        for r in range(1, 6):
            for c in range(1, 6):
                self.gameState[r, c] = self._ablank

                # self.gameState[3,4] = self._anS
                # self.gameState[1,4] = self._anS
                # self.gameState[4,2] = self._anR
                # self.gameState[2,2] = self._anJ
                # self.gameState[3,5] = self._anS
                # self.gameState[4,4] = self._anS
                # self.gameState[2,5] = self._anS

                # self.gameState[3,3] = self._anJ
                # self.gameState[4,3] = self._anR
                # self.gameState[2,1] = self._anR
                # self.gameState[2,5] = self._anR
                # self.gameState[2,4] = self._anS

                self.gameState[5,c] = self._anR
                self.gameState[1,3] = self._anS

        # print(self.gameState)


        # the blanks show what's left to choose from
        self.blanks = {v for v in self.gameState}

        # a boolean to store if it's Max's turn; True by default
        self.maxs_turn = True

        # if this state is a winning state, store that information
        # because it is cheaper to check once, than a bunch of times
        self.cachedWin = False

        # if cachedWin is True, then cachedWinner is a boolean
        # True means Max won; False means Min won
        self.cachedWinner = None

        # now cache the string that represents this state
        self.stringified = str(self)

        self.move = 40

    def myclone(self):
        """ Make and return an exact copy of the state.
        """

        new_state = GameState()
        for rc in self.gameState:
            new_state.gameState[rc] = self.gameState[rc]
        new_state.blanks = {v for v in self.blanks}  # copy the data not the reference
        new_state.maxs_turn = self.maxs_turn
        new_state.cachedWin = self.cachedWin
        new_state.cachedWinner = self.cachedWinner
        new_state.stringified = self.stringified  # copy the reference not the string
        new_state.move = self.move

        return new_state

    def display(self):
        """
        Present the game state to the console.
        """
        for r in range(1, 6):
            print("+-+-+-+-+-+")
            print("|", end = "")
            for c in range(1, 5):
                print(self.gameState[r, c], end="")
                print("|", end="")
            print(self.gameState[r, 5], end="")
            print("|")
        print("+-+-+-+-+-+")

    def __str__(self):
        """ Translate the board description into a string.
            Could be used as a key for a hash table.
            :return: A string that describes the board in the current state.
        """
        s = ""
        for r in range(1, 6):
            for c in range(1, 6):
                s += self.gameState[r, c]
        return s


class Game(object):
    """ The Game object defines the interface that is used by Game Tree Search
        implementation.
    """
    
    def __init__(self,depthlimit = 0):
        """ Initialization.
        """
        self.depth_limit = depthlimit

    def initial_state(self):
        """ Return an initial state for the game.
        """
        state = GameState()
        return state

    def is_mins_turn(self, state):
        """ Indicate if it's Min's turn
            :return: True if it's Min's turn to play
        """
        return not state.maxs_turn

    def is_maxs_turn(self, state):
        """ Indicate if it's Min's turn
            :return: True if it's Max's turn to play
        """
        return state.maxs_turn

    def is_terminal(self, state):
        """ Indicate if the game is over.
            :param node: a game state with stored game state
            :return: a boolean indicating if node is terminal
        """
        return state.cachedWin or state.move == 0 or len(self.actions(state)) == 0

    def rebel_direction_constraint(self,state):

        rebel_list = []
        rebel_list_not_move = []

        for r in range(1,6):

            for c in range(1,6):

                if state.gameState[r,c] == 'R':

                    if r!= 1:

                        if state.gameState[r-1,c] == ' ':

                            a = []
                            a.append("REBEL")
                            a.append([r, c])
                            a.append("UP")
                            a.append(1)
                            a.append([r - 1, c])
                            rebel_list.append(a)



                    if r!= 1 and c!= 5:

                        if state.gameState[r-1,c+1] == 'S':

                            a = []
                            a.append("REBEL")
                            a.append([r, c])
                            a.append("UPRIGHT")
                            a.append(1)
                            a.append([r - 1, c+1])
                            rebel_list.append(a)

                    if c!= 1 and r!= 1:

                        if state.gameState[r-1,c-1] == 'S':

                            a = []
                            a.append("REBEL")
                            a.append([r, c])
                            a.append("UPLEFT")
                            a.append(1)
                            a.append([r - 1, c-1])
                            rebel_list.append(a)

                    if r!= 1:

                        if state.gameState[r-1,c] == 'R':

                            rebel_list_not_move.append("Rebel "+ str(r)+ ","+ str(c) + " cannot move to this position.")

        return rebel_list



    def sith_direction_constraint(self,state):

        sith_list = []
        sith_list_not_move = []

        for r in range(1,6):

            for c in range(1,6):

                if state.gameState[r,c] == 'S':

                    if r!=1 and state.gameState[r-1,c] == ' ':
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("UP")
                        a.append(1)
                        a.append([r - 1, c])
                        sith_list.append(a)

                    if r!=5 and state.gameState[r+1,c] == ' ':
                        a = []
                        a.append("SITH")
                        a.append([r,c])
                        a.append("DOWN")
                        a.append(1)
                        a.append([r+1,c])
                        sith_list.append(a)


                    if c!=1 and state.gameState[r,c-1] == ' ':
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("LEFT")
                        a.append(1)
                        a.append([r, c-1])
                        sith_list.append(a)

                    if c!= 5 and state.gameState[r,c+1] == ' ':
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("RIGHT")
                        a.append(1)
                        a.append([r, c+1])
                        sith_list.append(a)

                    if r!=1 and c!= 1 and state.gameState[r-1,c-1] == ' ':
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("UPLEFT")
                        a.append(1)
                        a.append([r - 1, c-1])
                        sith_list.append(a)


                    if r!= 1 and c!= 5 and state.gameState[r-1,c+1] == ' ':
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("UPRIGHT")
                        a.append(1)
                        a.append([r -1, c+1])
                        sith_list.append(a)


                    if r!=5 and c!=1 and state.gameState[r+1, c-1] == ' ':
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("DOWNLEFT")
                        a.append(1)
                        a.append([r + 1, c-1])
                        sith_list.append(a)


                    if c!= 5 and r!=5 and state.gameState[r+1,c+1] == ' ':
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("DOWNRIGHT")
                        a.append(1)
                        a.append([r + 1, c+1])
                        sith_list.append(a)



                    # when it meet the
                    if r != 1 and state.gameState[r - 1, c] == 'R' :
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("UP")
                        a.append(1)
                        a.append([r - 1, c])
                        sith_list.append(a)

                    if r != 5 and state.gameState[r + 1, c] == 'R'  :
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("DOWN")
                        a.append(1)
                        a.append([r + 1, c])
                        sith_list.append(a)

                    if c != 1 and state.gameState[r, c - 1] == 'R'  :
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("LEFT")
                        a.append(1)
                        a.append([r , c-1])
                        sith_list.append(a)

                    if c!=5 and state.gameState[r, c + 1] == 'R':
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("RIGHT")
                        a.append(1)
                        a.append([r , c+1])
                        sith_list.append(a)

                    if r != 1 and c != 1 and state.gameState[r - 1, c - 1] == 'R':
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("UPLEFT")
                        a.append(1)
                        a.append([r - 1, c-1])
                        sith_list.append(a)

                    if r != 5 and c != 1 and state.gameState[r + 1, c - 1] == 'R'  :
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("DOWNLEFT")
                        a.append(1)
                        a.append([r + 1, c-1])
                        sith_list.append(a)


                    if c != 5 and r != 1 and state.gameState[r - 1, c + 1] == 'R'  :
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("UPRIGHT")
                        a.append(1)
                        a.append([r - 1, c+1])

                        sith_list.append(a)

                    if r != 5 and c!= 5:
                        if state.gameState[r + 1, c + 1] == 'R'  :
                            a = []
                            a.append("SITH")
                            a.append([r, c])
                            a.append("DOWNRIGHT")
                            a.append(1)
                            a.append([r + 1, c+1])
                            sith_list.append(a)





                    if r != 1 and state.gameState[r - 1, c] == 'J' :
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("UP")
                        a.append(1)
                        a.append([r - 1, c])
                        sith_list.append(a)

                    if r != 5 and state.gameState[r + 1, c] == 'J'  :
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("DOWN")
                        a.append(1)
                        a.append([r + 1, c])
                        sith_list.append(a)

                    if c != 1 and state.gameState[r, c - 1] == 'J'  :
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("LEFT")
                        a.append(1)
                        a.append([r , c-1])
                        sith_list.append(a)

                    if c!=5 and state.gameState[r, c + 1] == 'J':
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("RIGHT")
                        a.append(1)
                        a.append([r , c+1])
                        sith_list.append(a)

                    if r != 1 and c != 1 and state.gameState[r - 1, c - 1] == 'J':
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("UPLEFT")
                        a.append(1)
                        a.append([r - 1, c-1])
                        sith_list.append(a)

                    if r != 5 and c != 1 and state.gameState[r + 1, c - 1] == 'J'  :
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("DOWNLEFT")
                        a.append(1)
                        a.append([r + 1, c-1])
                        sith_list.append(a)


                    if c != 5 and r != 1 and state.gameState[r - 1, c + 1] == 'J'  :
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("UPRIGHT")
                        a.append(1)
                        a.append([r - 1, c+1])
                        sith_list.append(a)

                    if r != 5 and c!=5 and state.gameState[r + 1, c + 1] == 'J'  :
                        a = []
                        a.append("SITH")
                        a.append([r, c])
                        a.append("DOWNRIGHT")
                        a.append(1)
                        a.append([r + 1, c+1])
                        sith_list.append(a)


        return sith_list


    def jedi_direction_constraints(self,state):

                jedi_list= []
                jedi_list_not_move = []

                for c in range(1,6):
                    for r in range(1,6):
                        for i in range(1,5):
                            if state.gameState[r, c] == 'J':
                                if  r > i:
                                    if state.gameState[r - i, c] == ' ':

                                        a = []
                                        a.append("JEDI")
                                        a.append([r, c])
                                        a.append("UP")
                                        a.append(i)
                                        a.append([r - i, c])
                                        jedi_list.append(a)

                                    if state.gameState[r-i,c] == 'R' or state.gameState[r-i,c] == 'J':

                                        break

                                    if state.gameState[r - i, c] == 'S':

                                        a = []
                                        a.append("JEDI")
                                        a.append([r, c])
                                        a.append("UP")
                                        a.append(i)
                                        a.append([r - i, c])
                                        jedi_list.append(a)

                                    if state.gameState[r - i, c] == 'S':

                                        break


                for c in range(1, 6):
                    for r in range(1, 6):
                        for i in range(1, 5):
                            if state.gameState[r, c] == 'J':
                                if r < 6-i:
                                    if state.gameState[r + i, c] == ' ':
                                        a = []
                                        a.append("JEDI")
                                        a.append([r, c])
                                        a.append("DOWN")
                                        a.append(i)
                                        a.append([r + i, c])
                                        jedi_list.append(a)

                                    if state.gameState[r + i, c] == 'R' or state.gameState[r+i,c] == 'J':

                                        break


                                    if state.gameState[r + i, c] == 'S':

                                        a = []
                                        a.append("JEDI")
                                        a.append([r, c])
                                        a.append("DOWN")
                                        a.append(i)
                                        a.append([r + i, c])
                                        jedi_list.append(a)


                                    if state.gameState[r + i, c] == 'S':

                                        break



                for c in range(1, 6):
                    for r in range(1, 6):
                        for i in range(1, 5):
                            if state.gameState[r, c] == 'J':
                                if c > i:
                                    if state.gameState[r, c - i] == ' ':
                                        a = []
                                        a.append("JEDI")
                                        a.append([r, c])
                                        a.append("LEFT")
                                        a.append(i)
                                        a.append([r, c - i])
                                        jedi_list.append(a)
                                    if state.gameState[r, c - i] == 'R' or state.gameState[r,c-i] == 'J':
                                        break


                                    if state.gameState[r, c - i] == 'S':
                                        a = []
                                        a.append("JEDI")
                                        a.append([r, c])
                                        a.append("LEFT")
                                        a.append(i)
                                        a.append([r, c - i])
                                        jedi_list.append(a)

                                    if state.gameState[r, c - i] == 'S':
                                        break



                for c in range(1, 6):
                    for r in range(1, 6):
                        for i in range(1, 5):
                            if state.gameState[r, c] == 'J':
                                if c < 6-i:
                                    if state.gameState[r, c + i] == ' ' :

                                        a = []
                                        a.append("JEDI")
                                        a.append([r, c])
                                        a.append("RIGHT")
                                        a.append(i)
                                        a.append([r, c + i])
                                        jedi_list.append(a)

                                    if state.gameState[r, c + i] == 'R' or state.gameState[r, c + i] == 'J':
                                        break


                                    if state.gameState[r, c + i] == 'S':
                                        a = []
                                        a.append("JEDI")
                                        a.append([r, c])
                                        a.append("RIGHT")
                                        a.append(i)
                                        a.append([r, c + i])
                                        jedi_list.append(a)

                                    if state.gameState[r, c + i] == 'S':
                                        break



                for c in range(1, 6):
                    for r in range(1, 6):
                        for i in range(1, 5):
                            if state.gameState[r, c] == 'J':
                                if r>i and c>i:
                                    if state.gameState[r - i, c - i] == ' ':
                                        a = []
                                        a.append("JEDI")
                                        a.append([r, c])

                                        a.append("UPLEFT")
                                        a.append(i)
                                        a.append([r - i, c - i])
                                        jedi_list.append(a)

                                    if state.gameState[r - i, c - i] == 'R' or state.gameState[r - i, c - i] == 'J':
                                        break


                                    if state.gameState[r - i, c - i] == 'S':
                                        a = []
                                        a.append("JEDI")
                                        a.append([r, c])
                                        a.append("UPLEFT")
                                        a.append(i)
                                        a.append([r - i, c - i])
                                        jedi_list.append(a)

                                    if state.gameState[r - i, c - i] == 'S':
                                        break


                for c in range(1, 6):
                    for r in range(1, 6):
                        for i in range(1, 5):
                            if state.gameState[r, c] == 'J':
                                if r > i and c < 6-i:
                                    if state.gameState[r - i, c + i] == ' ' or state.gameState[r - i, c + i] == 'R' or state.gameState[r - i, c + i] == 'J':
                                        a = []
                                        a.append("JEDI")
                                        a.append([r, c])

                                        a.append("UPRIGHT")
                                        a.append(i)
                                        a.append([r - i, c + i])
                                        jedi_list.append(a)
                                        if state.gameState[r - i, c + i] == 'R' or state.gameState[r - i, c + i] == 'J':
                                            break


                                        if state.gameState[r - i, c + i] == 'S':
                                            a = []
                                            a.append("JEDI")
                                            a.append([r, c])
                                            a.append("UPRIGHT")
                                            a.append(i)
                                            a.append([r - i, c + i])
                                            jedi_list.append(a)

                                        if state.gameState[r - i, c + i] == 'S':
                                            break




                for c in range(1, 6):
                    for r in range(1, 6):
                        for i in range(1, 5):
                            if state.gameState[r, c] == 'J':
                                if r < 6 - i and c > i:
                                    if state.gameState[r + i, c - i] == ' ':
                                        a = []
                                        a.append("JEDI")
                                        a.append([r, c])

                                        a.append("DOWNLEFT")
                                        a.append(i)
                                        a.append([r + i, c - i])
                                        jedi_list.append(a)

                                    if state.gameState[r + i, c - i] == 'R' or state.gameState[r + i, c - i] == 'J':
                                        break



                                    if state.gameState[r + i, c - i] == 'S':
                                        a = []
                                        a.append("JEDI")
                                        a.append([r, c])
                                        a.append("DOWNLEFT")
                                        a.append(i)
                                        a.append([r + i, c - i])
                                        jedi_list.append(a)


                                    if state.gameState[r + i, c - i] == 'S':
                                        break


                for c in range(1, 6):
                    for r in range(1, 6):
                        for i in range(1, 5):
                            if state.gameState[r, c] == 'J':
                                if r < 6 - i :
                                    if c < 6 - i:
                                        if state.gameState[r + i, c + i] == ' ':

                                            a = []
                                            a.append("JEDI")
                                            a.append([r, c])
                                            a.append("DOWNRIGHT")
                                            a.append(i)
                                            a.append([r + i, c + i])
                                            jedi_list.append(a)

                                        if state.gameState[r + i, c + i] == 'R' or state.gameState[r + i, c + i] == 'J':
                                            break


                                        if state.gameState[r + i, c + i] == 'S':
                                            a = []
                                            a.append("JEDI")
                                            a.append([r, c])
                                            a.append("DOWNRIGHT")
                                            a.append(i)
                                            a.append([r + i, c + i])
                                            jedi_list.append(a)

                                        if state.gameState[r + i, c + i] == 'S':
                                            break



                return jedi_list



    def actions(self, state):
        """ Returns all the legal actions in the given state.
            :param state: a state object
            :return: a list of actions legal in the given state
        """


        player1_action_list = []

        player2_action_list = []

        rebel_action = self.rebel_direction_constraint(state)

        sith_action = self.sith_direction_constraint(state)

        jedi_action = self.jedi_direction_constraints(state)



        for j in range(len(jedi_action)):

            player1_action_list.append(jedi_action[j])

        for i in range(len(rebel_action)):

            player1_action_list.append(rebel_action[i])

        for k in range(len(sith_action)):


            player2_action_list.append(sith_action[k])

        if self.is_maxs_turn(state):

            # print(player1_action_list)
            # state.move -= 1
            # print(state.move)
            return player1_action_list

        if self.is_mins_turn(state):

            # print(player2_action_list)
            # state.move -= 1
            # print(state.move)
            return player2_action_list


    def result(self, state, action):
        """ Return the state that results from the application of the
            given action in the given state.
            :param state: a legal game state
            :param action: a legal action in the game state
            :return: a new game state
        """
        # print(state.move)
        new_state = state.myclone()

        # new_state.move -= 1
        #
        # print(new_state.move)
        # if state.maxs_turn == True:
        #     print(new_state.move)
        #     new_state.move -= 1
        # if state.maxs_turn == False:
        #     print(new_state.move)
        #     new_state.move -= 1
        # print(action[0])
        # print(action[1][0])
        # print(action[1][1])
        # print(action[3][0])
        # print(action[3][1])



        who = action[0]



        who1 = state.maxs_turn
        # print("max_turn",state.maxs_turn)

        current_position = action[1]
        # print(current_position[0])
        # direction = action[2]
        # final_position = action[3]

        final_position = action[4]
        # print(who)
        # print(new_state.gameState[final_position2[0],final_position2[1]])
        # print(new_state.gameState[current_position[0],current_position[1]])
        # print(new_state.gameState[current_position[0]])
        if who == 'SITH':

            if new_state.gameState[final_position[0],final_position[1]] == ' ':

                new_state.gameState[final_position[0],final_position[1]] = 'S'
                # print(new_state.gameState[current_position[0], current_position[1]])
                new_state.gameState[current_position[0],current_position[1]] = ' '
                # print(new_state.gameState[current_position[0], current_position[1]])

                # print(new_state.gameState[final_position[0],final_position[1]])

            if new_state.gameState[final_position[0],final_position[1]] == 'R':
                new_state.gameState[final_position[0],final_position[1]] = ' '
                new_state.gameState[final_position[0],final_position[1]] = 'S'
                new_state.gameState[current_position[0],current_position[1]] = ' '

            if new_state.gameState[final_position[0],final_position[1]] == 'J':
                new_state.gameState[final_position[0],final_position[1]] = 'S'
                new_state.gameState[current_position[0],current_position[1]] = 'S'

        if who == 'JEDI':
            # print(new_state.gameState[final_position2[0],final_position2[1]])
            if new_state.gameState[final_position[0],final_position[1]] == ' ':
                new_state.gameState[final_position[0],final_position[1]] = 'J'
                new_state.gameState[current_position[0],current_position[1]] = ' '

            if new_state.gameState[final_position[0],final_position[1]] == 'S':
                new_state.gameState[final_position[0],final_position[1]] = ' '
                new_state.gameState[final_position[0],final_position[1]] = 'J'
                new_state.gameState[current_position[0],current_position[1]] = ' '

        if who == 'REBEL':

            if new_state.gameState[final_position[0],final_position[1]] == ' ':
                new_state.gameState[final_position[0],final_position[1]] = 'R'
                new_state.gameState[current_position[0],current_position[1]] = ' '

            if new_state.gameState[final_position[0],final_position[1]] == 'S':
                new_state.gameState[final_position[0],final_position[1]] = ' '
                new_state.gameState[final_position[0],final_position[1]] = 'R'
                new_state.gameState[current_position[0],current_position[1]] = ' '

            #print(current_position[0])

            if final_position[0] == 1:
                #print(final_position)
                new_state.gameState[final_position[0],final_position[1]] = ' '
                new_state.gameState[final_position[0],final_position[1]] = 'J'

        new_state.maxs_turn = not state.maxs_turn

        # if state.maxs_turn == True:
        #     print(new_state.move)
        #     new_state.move -= 1
        # if state.maxs_turn == False:
        #     print(new_state.move)
        #     new_state.move -= 1

        self._cache_winner(new_state,final_position,who1)


        # new_state.display()

        new_state.move -=1




        return new_state




    def utility(self, state):
        """ Calculate the utility of the given state.
            :param state: a legal game state
            :return: utility of the terminal state
        """

        if state.cachedWin and state.cachedWinner:
            return 1
        elif state.cachedWin and not state.cachedWinner:
            return -1
        else:
            return 0


    def cutoff_test(self, state, depth):
        """
            Check if the search should be cut-off early.
            In a more interesting game, you might look at the state
            and allow a deeper search in important branches, and a shallower
            search in boring branches.

            :param state: a game state
            :param depth: the depth of the state,
                          in terms of levels below the start of search.
            :return: True if search should be cut off here.
        """


        return self.depth_limit > 0 and depth>self.depth_limit

    def eval(self, state):
        """
            When a depth limit is applied, we need to evaluate the
            given state to estimate who might win.
            state: a legal game state
            :return: a numeric value in the range of the utility function
        """

        number_sith = []
        number_jedi = []
        number_rebel = []

        for r in range(1,6):
            for c in range(1,6):
                if state.gameState[r,c] == 'S':
                    number_sith.append([r,c])
                if state.gameState[r,c] == 'J':
                    number_jedi.append([r,c])
                if state.gameState[r,c] == 'R':
                    number_rebel.append([r,c])

        f1 = 5*(-len(number_sith))
        f2 = 2*(len(number_rebel))
        f3 = 20*(len(number_jedi))



        return f1+f2+f3

    def congratulate(self, state):
        """ Called at the end of a game, display some appropriate 
            sentiments to the console. Could be used to display 
            game statistics as well.
            :param state: a legal game state
        """

        winstring = 'Congratulations, {} wins (utility: {})'
        if state.cachedWin and state.cachedWinner:
            print(winstring.format("Player 1", self.utility(state)))
        elif state.cachedWin and not state.cachedWinner:
            print(winstring.format("Player 2", self.utility(state)))
        else:
            print('No winner')

        return  # not really needed, but indicates the end of the method


    def transposition_string(self, state):
        """ Returns a unique string for the given state.  For use in 
            any Game Tree Search that employs a transposition table.
            :param state: a legal game state
            :return: a unique string representing the state
        """
        return state.stringified

    def _cache_winner(self,state,where,who):

        won = False

        recent_r, recent_c = where



        if state.gameState[recent_r,recent_c] == 'R' or state.gameState[recent_r,recent_c] =='J':


            if 'S' not in state.gameState.values():
                won = True



        else:

           if 'R' not in state.gameState.values() and 'J' not in state.gameState.values():

               won = True





        if won:

            state.cachedWin = True

            state.cachedWinner = who

        return












        
# eof