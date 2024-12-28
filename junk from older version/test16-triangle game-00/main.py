import random



# def tryNextMove(pegs, definedMoves, recordOfMoves, depth) :
#     # definition of "depth":  at start of game, when one slot is empty, depth is 0 (arbitarily)
#     # when we eventually insert recordOfMoves[0], that will be the first move
#     for move in definedMoves :
#         if pegs[move[1]] and ( pegs[move[0]] != pegs[move[2]] )  :
#             makeAMove(pegs, move)
#             newDepth = depth + 1
#             recordOfMoves[newDepth] = move
#             if newDepth == 13 :
#                 return True
#             if tryNextMove(pegs, definedMoves, recordOfMoves, newDepth) :
#                 return True
#     # unwind the most recent move (from one level deeper in the recursion
#     makeAMove(pegs, recordOfMoves[depth])
#     return False

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

definedMoves = [
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
    depth = playUntilWeCannotPlayFurther(definedMoves)
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
    tryNextMove(pegs, definedMoves, recordOfMoves, 0, counter, allPossibleSolutions, histogramOfDepthOfEachEndingPoint, file)


    # for depth in range(0, 15) :
    #     print(str(depth) + ", " + str(histogramOfDepthOfEachEndingPoint[depth]))


    # print(recordOfMoves)
    # for n in range(0, 15) :
    #     #vif pegs[n] :
    #     print("peg at " + str(n) + " is " + str(pegs[n]))