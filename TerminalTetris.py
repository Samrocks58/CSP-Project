# I wrote all of this code myself
import msvcrt, os, time, random, readkeys
from termcolor import colored

ROWS = 20+2
width = 10 * 2
startX = (width // 2) - 2
startY = 0
MoveX = startX
MoveY = startY
passive_blocks = []
blocks = []
dropped = False
inColor = True
swapped = False
swapIndex = -1
colors = ["cyan", "light_grey", "magenta", "light_yellow", "blue", "red", "green"]
IPiece = [[[0,0], [1*2,0], [2*2,0], [3*2,0]], [[0,0], [0,1], [0,2], [0,3]]]
OPiece = [[[0,0], [1*2,0], [0,1], [1*2,1]]]
TPiece = [[[0,0], [1*2,0], [2*2,0], [1*2,1]], [[1*2,0], [0,1], [1*2,1], [1*2,2]], [[1*2,0], [0,1], [1*2,1], [2*2,1]], [[0,0], [0,1], [0,2], [1*2,1]]]
LPiece = [[[0,0], [1*2,0], [2*2,0], [0,1]], [[0,0], [1*2,0], [1*2,1], [1*2,2]], [[0,1], [1*2,1], [2*2,1], [2*2,0]], [[0,0], [0,1], [0,2], [1*2,2]]]
JPiece = [[[0,0], [1*2,0], [2*2,0], [2*2,1]], [[0,2], [1*2,0], [1*2,1], [1*2,2]], [[0,1], [1*2,1], [2*2,1], [0,0]], [[0,0], [0,1], [0,2], [1*2,0]]]
ZPiece = [[[0,0], [1*2,0], [1*2,1], [2*2,1]], [[1*2,0], [0,1], [1*2,1], [0,2]]]
SPiece = [[[1*2,0], [0,1], [1*2,1], [2*2,0]], [[0,0], [0,1], [1*2,1], [1*2,2]]]
pieces = [IPiece, OPiece, TPiece, LPiece, JPiece, ZPiece, SPiece]
display_indexes = [1, 0, 1, 3, 3, 1, 1]
colors_stored = {}
pieceIndex = random.randint(0, 6)
nextIndex = random.randint(0, 6)
# pieceIndex = 6
rotationIndex = 0
n = 12.0
# ^^^ start here then decrease with lines cleared till you get to 1
# n = 8

def make_blocks(p, r, X = MoveX, Y = MoveY):
    global pieces
    offsets = pieces[p][r % len(pieces[p])]
    new_blocks = []
    for x in offsets:
        new_blocks.append([X+x[0], Y+x[1]])
    return new_blocks

# This function does most of the GUI for the whole program by calculating the offset of each block
def print_board():
    global blocks, passive_blocks, pieceIndex, nextIndex, colors_stored, inColor
    os.system('cls')
    rowString = ""
    for i in range(ROWS):
        if i < ROWS-2:
            rowString += "||"
            spacesMoved = 0
            if nextIndex == 0:
                displayBlocks = make_blocks(nextIndex, display_indexes[nextIndex], X = 23, Y = 2)
            else:
                displayBlocks = make_blocks(nextIndex, display_indexes[nextIndex], X = 23, Y = 3)
            copyList = blocks.copy()
            copyList.extend(passive_blocks)
            copyList.extend(displayBlocks)
            storeBlocks = []
            if swapIndex != -1:
                storeBlocks = make_blocks(swapIndex, display_indexes[swapIndex], X = 23, Y= 8)
                copyList.extend(storeBlocks)
            
            end = find_bottom_blocks()
            end_blocks = end[0]
            # endY = end[1]
            end_blocks = list(filter(lambda x: not(x in blocks), end_blocks))
            copyList.extend(end_blocks)
            # if endY != MoveY and len(list(filter(lambda x: x in blocks, end_blocks))) == 0:
            #     copyList.extend(end_blocks)
            # else:
            #     # end_blocks = []
            #     end_blocks = list(filter(lambda x: not(x in blocks), end_blocks))
            #     copyList.extend(end_blocks)


            for b in sort_blocks(copyList):
                if i == b[1]:
                    if b in passive_blocks:
                        # square = colored("[]", colors[colors_stored[hash_lst(b)]])
                        if inColor:
                            try:
                                # square = colored("[]", colors[colors_stored[hash_lst(b)]])
                                square = colored("[]", colors[colors_stored[(b[0], b[1])]])
                            except Exception as e:
                                square = colored("[]", "red")
                        else:
                            square = colored("[]", "dark_grey")
                            
                            # print(str(e))
                            # quit()
                            # print(str(e).split("KeyError: ")[1])
                            # print(e.with_traceback())
                        # square = colored("[]", "dark_grey")
                    else:
                        if not ([startX, startY] in passive_blocks):
                            if inColor:
                                if b in displayBlocks:
                                    square = colored("[]", colors[nextIndex])
                                elif b in storeBlocks:
                                    square = colored("[]", colors[swapIndex])
                                elif b in end_blocks:
                                    square = colored("[]", "dark_grey")
                                else:
                                    square = colored("[]", colors[pieceIndex])
                            else:
                                square = colored("[]", "dark_grey")
                    rowString += " " * (b[0]-spacesMoved) + square
                    spacesMoved = b[0]+2
            rowString += " " * (width-spacesMoved)
            # if i == 0 or i >= 4:
            #     rowString += "\n"
            if i == 1:
                rowString += " N E X T" + "\n"
            elif i == 7:
                rowString += "S T O R E" + "\n"
            else:
                rowString += "\n"
        else:
            rowString += "  " + "-" * width + "\n"

    print(rowString)

def find_bottom_blocks():
    global MoveY, blocks
    clear = True
    end_blocks = blocks
    returnY = MoveY
    while clear:
        oldY = returnY
        oldBlocks = end_blocks
        returnY += 1
        end_blocks = make_blocks(pieceIndex, rotationIndex, X = MoveX, Y = returnY)
        for i in end_blocks:
            if (i in passive_blocks) or (i[1] >= ROWS-2):
                clear = False
                end_blocks = oldBlocks
                returnY = oldY

    return [end_blocks, returnY]

def check_input():
    global MoveX, MoveY, blocks, passive_blocks, rotationIndex, dropped, n, inColor, pieceIndex, swapIndex, swapped, nextIndex
    # print(readkeys.getch())
    if msvcrt.kbhit():
        c = msvcrt.getwch()
        if c == 'q':
            print(f"Lines Cleared: {linesCleared}\n")
            quit()
    #   DEBUGGING STUFF:
        # if c == "k":
        #     n -= 1
        # if c == "m":
        #     n += 1
        # if c == "c":
        #     inColor = not inColor
        if c == "r":
            passive_blocks = []
        # if c in "1234567":
        #     nextIndex = eval(c) - 1
        if c == "d":
            if not ([MoveX+2, MoveY] in passive_blocks):
                clear = True
                future_blocks = make_blocks(pieceIndex, rotationIndex, X = MoveX+2, Y = MoveY)
                for b in future_blocks:
                    if ([b[0], b[1]] in passive_blocks) or (b[0] > width-2):
                        clear = False
                if clear:
                    MoveX += 2
                    MoveX = min(width-2, MoveX)    
        elif c == "a":
            if not ([MoveX-2, MoveY] in passive_blocks):
                clear = True
                for b in blocks:
                    if ([b[0]-2, b[1]] in passive_blocks):
                        clear = False
                if clear:
                    MoveX -= 2
                    MoveX = max(0, MoveX)
        elif c == "s":
            future_blocks = make_blocks(pieceIndex, rotationIndex+1, X = MoveX, Y = MoveY)
            clear = True
            for i in future_blocks:
                if (i in passive_blocks) or (i[0] > width-2):
                    clear = False
            if clear:
                rotationIndex += 1
                if rotationIndex >= 4:
                    rotationIndex = 0
        elif c == " ":
            # Instant DROP key
            test = find_bottom_blocks()
            blocks = test[0]
            MoveY = test[1]
        elif c == "e":
            # Block SWAP key
            if not swapped:
                swapped = True
                MoveX = startX
                MoveY = startY
                if swapIndex == -1:
                    swapIndex = pieceIndex
                    pieceIndex = nextIndex
                    nextIndex = random.randint(0, 6)
                else:
                    temp = swapIndex
                    swapIndex = pieceIndex
                    pieceIndex = temp


elapsed_time = 0
FFC = 0 # Fall Frame Counter (Obviously)
coinCollected = False
linesCleared = 0
def gameloop():
    global blocks, passive_blocks, MoveX, MoveY, elapsed_time, FFC, linesCleared, pieceIndex, rotationIndex, dropped, n, nextIndex, colors_stored, swapped
    while True:
        start_time = time.perf_counter()
        check_input()

        if elapsed_time >= 1/20:
            elapsed_time = 0
            blocks = make_blocks(pieceIndex, rotationIndex, X = MoveX, Y = MoveY)
            print_board()
                
            if [startX, startY] in passive_blocks:
                print_board()
                print("Game Over!")
                print(f"Lines Cleared: {linesCleared}")
                quit()

            for b in blocks:
                if (b[1] == ROWS-3) or ([b[0], b[1]+1] in passive_blocks) or dropped:
                    passive_blocks.extend(blocks)
                    MoveX = startX
                    MoveY = startY

                    if [startX, startY] in passive_blocks:
                        # print_board()
                        print("Game Over!")
                        print(f"Lines Cleared: {linesCleared}")
                        quit()

                    dropped = False
                    swapped = False
                    for b in blocks:
                        colors_stored[(b[0], b[1])] = pieceIndex
                        # colors_stored[hash_lst(b)] = pieceIndex

                    pieceIndex = nextIndex
                    nextIndex = random.randint(0, 6)

                    # pieceIndex = 0
                    break

            # if [startX, startY] in passive_blocks:
            #     print_board()
            #     print("Game Over!")
            #     print(f"Lines Cleared: {linesCleared}")
            #     quit()

            if FFC >= n:
                FFC = 0
                MoveY += 1
            
            for y in range(ROWS-2):
                counter = 0
                rm_list = []
                for p in passive_blocks:
                    if p[1] == y:
                        counter += 1
                        rm_list.append(p)
                    if counter >= width/2:
                        # if not ([startX, startY] in passive_blocks): # just in case
                        linesCleared += 1
                        # n -= 0.5
                        # n -= 0.1
                        n -= 0.2

                        for r in rm_list:
                            passive_blocks.remove(r)
                            # del colors_stored[hash_lst(r)]
                            del colors_stored[(r[0], r[1])]

                        for p3 in passive_blocks:
                            if p3[1] < y:
                                p3[1] += 1

                        old_colors = colors_stored.copy()
                        colors_stored.clear()

                        # if abs(len(colors_stored)-len(old_colors)) != 10:
                        #     raise Exception("NOT REMOVING ALL TEN")

                        for key, value in old_colors.items():
                            if key[1] < y+1:
                                colors_stored[(key[0], key[1] + 1)] = value
                            else:
                                colors_stored[key] = value

            FFC += 1

        end_time = time.perf_counter()
        elapsed_time += (end_time-start_time)

def sort_blocks(blist):
    sorted = False
    for i in range(len(blist)-1):
        if blist[i][0] > blist[i+1][0]:
            temp = blist[i]
            blist[i] = blist[i+1]
            blist[i+1] = temp
            sorted = True
    if sorted:
        return sort_blocks(blist)
    else:
        return blist

gameloop()