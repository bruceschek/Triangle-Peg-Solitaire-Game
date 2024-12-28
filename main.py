# d24-12-15
# this version is a re-make of the earlier version of triangle game code (from a few years
#   prior to 2024.  the earlier had no UI.  But the newer one has command line oriented UI.
#   And, the layout of numbering of the holes in the board is different here (with
#   position 1 at top of board, vs older version had position 15 at top.)

import random
import re

# board layout, by definition:
#            15
#            🔴
#          13  14
#          🟡  🔴
#        10   11   12
#       🟡   🔴   🔴
#      6    7    8    9
#     🔴   🔴   🟡   🔴
#   1    2    3    4    5
#  🔴   🔴   🔴   🔴   🔴

# ANSI escape sequences, for colorizing text  (more detail in Roam, under 'f-String formatting in python3'
blue_text =             "\u001b[34m"
red_text  =             "\u001b[31m"
reset_color_text =      "\u001b[0m"
# potential emojis to be used in visual UI:  🟡 ⚪️🪖 ⚫️ 🟤 🔴 ♦︎ ♢ ❌ 🛑

defined_moves = [
    ( 1,  2,  3), # horizontal
    ( 2,  3,  4),
    ( 3,  4,  5),
    ( 6,  7,  8),
    ( 7,  8,  9),
    (10, 11, 12),

    ( 1,  6, 10), # upward from left
    ( 6, 10, 13),
    (10, 13, 15),
    ( 2,  7, 11),
    ( 7, 11, 14),
    ( 3,  8, 12),

    ( 5,  9, 12), # upward from right
    ( 9, 12, 14),
    (12, 14, 15),
    ( 4,  8, 11),
    ( 8, 11, 13),
    ( 3,  7, 10) ]

hole_locations = [
        (15, ),
        (13, 14),
        (10, 11, 12),
        ( 6,  7,  8,  9),
        ( 1,  2,  3,  4,  5)
    ]

# zero'th element of "state" is not used, since we number the board with digits 1-15
full_state = [False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]


#******************************************************************************************
# helper functions that must be in place before introducting the main "UI" loop
#******************************************************************************************

def print_board(state):
    for index, row_elements in enumerate(hole_locations):
        indentation = " " * ( 14 - index * 3 )

        # print(indentation, end = "" )
        # print(indentation, end = "" )

        str_labels = indentation
        str_pegs =   indentation
        for row_element in row_elements:
            str_labels += f"{row_element:2d}   "
            str_pegs   += "🛑   " if state[row_element] else "⚫   "
        print( str_labels )
        print( str_pegs )
    print( f"peg count: {sum( state )}" )
    print()

def print_ui_prompts():
    print()
    print("Each time you are prompted:", red_text, "'Your entry?:'", reset_color_text,
          "your choices are any of the following:")
    print('-- ' + red_text + 'n1 n2 (integers)' + reset_color_text + ': 1st integer is a peg position, 2nd is an empty spot to which to jump.')
    print('-- ' + red_text + 'n' + reset_color_text + ' - Get a suggested ' + red_text + 'next' + reset_color_text + ' move')
    print('-- ' + red_text + 'b' + reset_color_text + ' - ' + red_text + 'Back ' + reset_color_text + 'up, by most recent move')
    print('-- ' + red_text + 'r' + reset_color_text + ' - ' + red_text + 'Reset ' + reset_color_text + 'the board to start')
    print('-- ' + red_text + 's n' + reset_color_text + ' - ' + red_text + 'Set ' + reset_color_text +
          'a starting poistion, at integer ' + red_text + 'n' + reset_color_text )
    print('-- ' + red_text + 'q' + reset_color_text + ' - ' + red_text + 'Quit ' + reset_color_text + 'and exit the game')
    print('-- ' + red_text + 'h' + reset_color_text + ' - ' + red_text + 'Help' + reset_color_text + ', Show again all the possible user entries')

    print()

def peg_count( state ) -> int:
    count = 0
    for peg in state: count += 1 if peg else 0
    return count

# get all possible next moves on the current state of the board
def get_all_possible_moves(state) -> []:
    possibleMoves = []
    for move in defined_moves :
        if ( state[move[0]] ^ state[move[2]] ) and state[move[1]]:
            possibleMoves.append(move)
    return possibleMoves

# If a valid move exists, then we retnrn True and instruction to move from position0 to position1
# If no valid move exsits, return False and 0, 0
def which_posititions_to_jump( state ) -> (bool, int, int):
    status, solution = find_solution( state )
    if status:
        move = solution[0]
        if state[move[0]]:  return True, move[0], move[2]
        else:               return True, move[2], move[0]
    return False, 0, 0

def find_solution( state ) -> ( bool, [] ):
    for move in get_all_possible_moves( state ):
        solution = []
        solution.append( move )
        new_state = make_move( state, move )
        ( status, solution ) = seek_valid_next_move(new_state, solution)
        if status: return  status, solution
    return  False, []

def seek_valid_next_move(state, solution) -> (bool, []):
    # print_board( state )
    if sum( state ) <= 1: return ( True, solution )
    for move in get_all_possible_moves(state):
        new_solution = solution.copy()
        new_solution.append( move )
        new_state = make_move( state, move )
        (result, solution) = seek_valid_next_move(new_state, new_solution)
        if result: return ( True, solution )
    solution.pop()
    return False, solution

# Make a move. We do NOT test for validity, as we assumee one of two conditions:
#   1) We've already determined validity of a possible next move. Or,...
#   2) We know the previously-executed move and we are simply reversing back to the state before that move.
def make_move( state, move ) -> []:
    new_state = state.copy()
    for i in range(3): new_state[move[i]] = not new_state[move[i]]
    return new_state

# In this context, a "valid move" is one of the moves within "defined_moves".
# if position0 and position1 are valid start and end of a valid move,
#    then return True and the "move" (3-element tuple)
# if not, then return False
# We assume that all moves in "defined_moves" are in ascending order (not (3,2,1) but rather (1,2,3)
def determine_if_valid_move(state, position0, position1) -> (bool, (int, int, int)):
    if position1 < position0:  position0, position1 = position1, position0
    for move in defined_moves:
        if position0 == move[0] and position1 == move[2]:
            if ( state[move[0]] ^ state[move[2]] ) and state[move[1]]:
                return True, move
    return False, (0, 0, 0)  # signal error - because position0, position1 do not define a valid move


#******************************************************************************************
# The "UI" function is the overall orchestrator of the game, and manages interaction with the player
#******************************************************************************************

def ui():
    state = full_state.copy()
    # define when hold is empty at start
    starting_position = 15
    state[ starting_position ] = False

    print("The game begins now!  Here is your starting board:")
    print_board( state )

    # A collection of each move up to the current state:
    moves_so_far = []

    print_ui_prompts()
    while (True):
        user_input = input("Your entry?: ")
        user_input = re.split(r'[,\s]+', user_input)

        if user_input[0].isdigit() and user_input[1].isdigit():
            position0, position1 = int(user_input[0]), int(user_input[1])
            success, move = determine_if_valid_move(state, position0, position1)
            if success:
                state = make_move(state, move)
                moves_so_far.append( move )
                if peg_count( state ) <= 1:
                    print("Congratulations!! You won!! Well played!!  Your final board:")
                    print_board( state )
                    print()
                    state = full_state.copy()
                    state[starting_position] = False
                    print("Now, you may begin a new round...")

                print_board( state )
            else:
                print("Invalid move! Ignored, try again...")

        elif user_input[0] == 'n':
            status, position0, position1 = which_posititions_to_jump(state)
            if status:
                print(f"Recommendation: move peg at position {position0} to position {position1}.")
            else:
                print("Alas, there is no valid move available.  You'll ned to 'back up' or 'reset'. 😟")

        elif user_input[0] == 'b':
            move_to_be_reversed = moves_so_far.pop()
            # Note this magical fact about our data structures:  "make_move" can reverse the previous move,
            #   so in a sense, it workds in both directions.
            state = make_move( state, move_to_be_reversed )
            print_board( state )

        elif user_input[0] == 'r':
            state = full_state.copy()
            state[ starting_position ] = False
            print_board(state)

        elif user_input[0] == "s":
            starting_position = int( user_input[1] )
            state = full_state.copy()
            state[ starting_position ] = False
            print_board( state )

        elif user_input[0] == 'q':
            print("Thanks for playing!!  Come back soon!!")
            exit()

        elif user_input[0] == 'h':
            print_ui_prompts()

        else:
            print("invalid entry. Try again. ")


if __name__ == "__main__":
    ui()
    exit()


#******************************************************************************************
#******************************************************************************************
# below is older version from a few years prior to 2024.
#******************************************************************************************
#******************************************************************************************

def tryNextMove(pegs, definedMoves, recordOfMoves, depth, counter, allPossibleSolutions, histogramOfDepthOfEachEndingPoint, file) :
    # definition of "depth":  at start of game, when one slot is empty, depth is 0 (arbitarily)
    # when we eventually insert recordOfMoves[0], that will be the first move
    moveFoundAtThisDepth = False
    for move in definedMoves :
        if pegs[move[1]] and ( pegs[move[0]] != pegs[move[2]] )  :
            moveFoundAtThisDepth = True
            makeAMove(pegs, move)
            newDepth = depth + 1
            recordOfMoves[newDepth] = move
            if newDepth == 13 :
                counter[0] += 1
                file.write(str(counter[0]) + ", " + str(recordOfMoves))
                file.write("\n")
                # testSetOfMoves(recordOfMoves)
                histogramOfDepthOfEachEndingPoint[newDepth] += 1
                makeAMove(pegs, move)  # unwind the latest move before dropping out this level of iteration
                #vreturn True
            else :
                tryNextMove(pegs, definedMoves, recordOfMoves, newDepth, counter, allPossibleSolutions, histogramOfDepthOfEachEndingPoint, file)
                # return True
                # if not moveFoundAtThisDepth :
                #     histogramOfDepthOfEachEndingPoint[depth] += 1
                # if depth == 7 :
                #     print(recordOfMoves)
    # unwind the most recent move (from one level deeper in the recursion
    if depth == 0 :
        print("done")
    else :
        # histogramOfDepthOfEachEndingPoint[depth] += 1
        makeAMove(pegs, recordOfMoves[depth]) # unwind the previous move
        # return # False

def makeAMove(pegs, move) :
    pegs[move[0]] = not pegs[move[0]]
    pegs[move[1]] = not pegs[move[1]]
    pegs[move[2]] = not pegs[move[2]]

def testSetOfMoves(recordOfMoves) :
    pegs = [True] * 16  # ignore peg[0], and use peg[1] through peg[15]; start with peg in all holes
    pegs[0] = False  # so that when we count pegs, we can count from zero using "for peg in pegs"
    pegs[1] = False  # this is the initial open slot on the board at start of game
    for move in recordOfMoves :
        if move == None :
            continue
        if pegs[move[1]] and (pegs[move[0]] != pegs[move[2]]):
            makeAMove(pegs, move)
        else :
            print("Oh no, we are screwed up")
            exit()

def findPossibleMovesOnCurrentBoard(pegs, definedMoves) :
    possibleMoves = []
    for move in definedMoves :
        if pegs[move[1]] and (pegs[move[0]] != pegs[move[2]]) :
            possibleMoves.append(move)
    return possibleMoves

def playUntilWeCannotPlayFurther(definedMoves) :
    pegs = [True] * 16  # ignore peg[0], and use peg[1] through peg[15]; start with peg in all holes
    pegs[0] = False  # so that when we count pegs, we can count from zero using "for peg in pegs"
    pegs[15] = False  # this is the initial open slot on the board at start of game
    recordOfMoves = []

    while True :

        possibleMoves = findPossibleMovesOnCurrentBoard(pegs, definedMoves)
        numberOfPossibleMoves = len(possibleMoves)
        if numberOfPossibleMoves == 0 :
            break
        index = random.randint(0, numberOfPossibleMoves-1)
        makeAMove(pegs, possibleMoves[index])
        recordOfMoves.append(possibleMoves[index])

    numberOfRemainingPegs = 0
    for n in range(0, 16) :
        if pegs[n] :
            numberOfRemainingPegs += 1
    if numberOfRemainingPegs == 1 :
        print("depth = " + str(15-numberOfRemainingPegs) + ", moves: " + str(recordOfMoves))
        exit()
    return 15-numberOfRemainingPegs  # "depth"


# Beware, this is not a zero-based numbering scheme.  I'm ignoring peg[0].
#
#              15
#           13   14
#        10   11   12
#      6    7    8    9
#   1    2    3    4    5:
#

defined_moves = [
    ( 1,  2,  3), # horizontal
    ( 2,  3,  4),
    ( 3,  4,  5),
    ( 6,  7,  8),
    ( 7,  8,  9),
    (10, 11, 12),

    ( 1,  6, 10), # upward from left
    ( 6, 10, 13),
    (10, 13, 15),
    ( 2,  7, 11),
    ( 7, 11, 14),
    ( 3,  8, 12),

    ( 5,  9, 12), # upward from right       ***** NOT DONE YET *******
    ( 9, 12, 14),
    (12, 14, 15),
    ( 4,  8, 11),
    ( 8, 11, 13),
    ( 3,  7, 10)   ]



#--------------------------------------------------------------------
# explore random moves
#--------------------------------------------------------------------

histogramOfDepthOfEachEndingPoint = [0]*16 # every time we reach a point where no more moves are possible (whether or not
# we've reached a winning position, we count one in the histogram of depth level

print("starting now....")

for n in range(0, 20 * 1000 * 1000) :
    depth = playUntilWeCannotPlayFurther(defined_moves)
    histogramOfDepthOfEachEndingPoint[depth] += 1
    # print("played to depth: " + str(depth))

for i in range(0, 15) :
    print("depth: " + str(i) + " - " + str(histogramOfDepthOfEachEndingPoint[i]))

exit()

#--------------------------------------------------------------------
# find all possbile solutions
#--------------------------------------------------------------------


startingPositions = [1, 2, 3, 7] # via symmetry, these are effectively all possible starting positions
allPossibleSolutions = []        # gather a list of all possible solutions, across all four possible starting positions
histogramOfDepthOfEachEndingPoint = [0]*16 # every time we reach a point where no more moves are possible (whether or not
# we've reached a winning position, we count one in the histogram of depth level

for startingPosition in startingPositions :

    path = "allPossibleSolutions.txt"
    file = open(path, "w")

    file.write("\n")
    file.write("starting position open: " + str(startingPosition))
    file.write("\n")
    file.write("\n")

    counter = [0]  # this is a crude yet effective means of passing an integer by reference

    pegs = [True]*16  # ignore peg[0], and use peg[1] through peg[15]; start with peg in all holes
    pegs[0] = False # so that when we count pegs, we can count from zero using "for peg in pegs"
    pegs[1] = False # this is the initial open slot on the board at start of game
    recordOfMoves = [None]*15
    # sequence of moves toward a win.  Each element of this list is reference to one of the
    # items in the defindMoves list.
    tryNextMove(pegs, defined_moves, recordOfMoves, 0, counter, allPossibleSolutions, histogramOfDepthOfEachEndingPoint, file)

    # for depth in range(0, 15) :
    #     print(str(depth) + ", " + str(histogramOfDepthOfEachEndingPoint[depth]))

    # print(recordOfMoves)
    # for n in range(0, 15) :
    #     #vif pegs[n] :
    #     print("peg at " + str(n) + " is " + str(pegs[n]))