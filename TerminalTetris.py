# I wrote all of this code myself
import msvcrt, os, time, random
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
    global blocks, passive_blocks, pieceIndex, nextIndex
    os.system('cls')
    rowString = ""
    for i in range(ROWS):
        if i < ROWS-2:
            rowString += "||"
            spacesMoved = 0
            displayBlocks = make_blocks(nextIndex, display_indexes[nextIndex], X = 22, Y = 2)
            copyList = blocks.copy()
            copyList.extend(passive_blocks)
            copyList.extend(displayBlocks)
            for b in sort_blocks(copyList):
                if i == b[1]:
                    if b in passive_blocks:
                        square = colored("[]", "dark_grey")
                    else:
                        if not ([startX, startY] in passive_blocks):
                            if b in displayBlocks:
                                square = colored("[]", colors[nextIndex])
                            else:
                                square = colored("[]", colors[pieceIndex])
                    rowString += " " * (b[0]-spacesMoved) + square
                    spacesMoved = b[0]+2
            rowString += " " * (width-spacesMoved)
            # if i == 0 or i >= 4:
            #     rowString += "\n"
            if i == 1:
                rowString += " N E X T" + "\n"
            else:
                rowString += "\n"
        else:
            rowString += "  " + "-" * width + "\n"

    print(rowString)

def check_input():
    global MoveX, MoveY, blocks, passive_blocks, rotationIndex, dropped, n
    if msvcrt.kbhit():
        c = msvcrt.getwch()
        if c == 'q':
            print(f"Lines Cleared: {linesCleared}\n")
            quit()
        if c == "k":
            n -= 1
        if c == "m":
            n += 1
        if c == "r":
            passive_blocks = []
        if c == "d" or c == "c":
            if not ([MoveX+2, MoveY] in passive_blocks):
                clear = True
                for b in blocks:
                    if ([b[0]+2, b[1]] in passive_blocks) or (b[0]+2 > width-2):
                        clear = False
                if clear:
                    MoveX += 2
                    MoveX = min(width-2, MoveX)    
        elif c == "a" or c == "z":
            if not ([MoveX-2, MoveY] in passive_blocks):
                clear = True
                for b in blocks:
                    if ([b[0]-2, b[1]] in passive_blocks):
                        clear = False
                if clear:
                    MoveX -= 2
                    MoveX = max(0, MoveX)
        elif c == "s" or c == "x":
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
            clear = True
            while clear:
                oldY = MoveY
                oldBlocks = blocks
                MoveY += 1
                blocks = make_blocks(pieceIndex, rotationIndex, X = MoveX, Y = MoveY)
                for i in blocks:
                    if (i in passive_blocks) or (i[1] >= ROWS-2):
                        clear = False
                        blocks = oldBlocks
                        MoveY = oldY

elapsed_time = 0
FFC = 0 # Fall Frame Counter (Obviously)
coinCollected = False
linesCleared = 0
def gameloop():
    global blocks, passive_blocks, MoveX, MoveY, elapsed_time, FFC, linesCleared, pieceIndex, rotationIndex, dropped, n, nextIndex
    cter = 0
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
                    dropped = False
                    # pieceIndex = random.randint(0, 6)
                    pieceIndex = nextIndex
                    nextIndex = random.randint(0, 6)
                    # pieceIndex = 1
                    break

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
                        n -= 0.1
    
                        for r in rm_list:
                            passive_blocks.remove(r)
                        for p3 in passive_blocks:
                            if p3[1] < y:
                                p3[1] += 1

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