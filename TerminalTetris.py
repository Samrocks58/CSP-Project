# I wrote all of this code myself
import msvcrt, os, time, random
from termcolor import colored

ROWS = 16+1
width = 8 * 2
startX = (width // 2) - 2
startY = 0
MoveX = startX
MoveY = startY
passive_blocks = []
# coinPos = [random.randint(0,width//2-1)*2, random.randint(0, ROWS-2)]
direction=1
blocks = [[MoveX, MoveY]]
old_pos = [MoveX, MoveY]
length = 1
keyPressed = False
dropped = False
colors = ["red", "blue"]
IPiece = [[[0,0], [1*2,0], [2*2,0], [3*2,0]], [[0,0], [0,1], [0,2], [0,3]]]
OPiece = [[[0,0], [1*2,0], [0,1], [1*2,1]]]
TPiece = [[[0,0], [1*2,0], [2*2,0], [1*2,1]], [[1*2,0], [0,1], [1*2,1], [1*2,2]], [[1*2,0], [0,1], [1*2,1], [2*2,1]], [[0,0], [0,1], [0,2], [1*2,1]]]
LPiece = [[[0,0], [1*2,0], [2*2,0], [0,1]], [[0,0], [1*2,0], [1*2,1], [1*2,2]], [[0,1], [1*2,1], [2*2,1], [2*2,0]], [[0,0], [0,1], [0,2], [1*2,2]]]
JPiece = [[[0,0], [1*2,0], [2*2,0], [2*2,1]], [[0,2], [1*2,0], [1*2,1], [1*2,2]], [[0,1], [1*2,1], [2*2,1], [0,0]], [[0,0], [0,1], [0,2], [1*2,0]]]
ZPiece = [[[0,0], [1*2,0], [1*2,1], [2*2,1]], [[1*2,0], [0,1], [1*2,1], [0,2]]]
SPiece = [[[1*2,0], [0,1], [1*2,1], [2*2,0]], [[0,0], [0,1], [1*2,1], [1*2,2]]]
pieces = [IPiece, OPiece, TPiece, LPiece, JPiece, ZPiece, SPiece]
pieceIndex = random.randint(0, 6)
rotationIndex = 0

def make_blocks(p, r):
    global blocks, pieces
    offsets = pieces[p][r % len(pieces[p])]
    blocks = []
    for x in offsets:
        blocks.append([MoveX+x[0], MoveY+x[1]])

# This function does most of the GUI for the whole program by calculating the offset of each block
def print_board():
    global blocks, passive_blocks
    os.system('cls')
    rowString = ""
    for i in range(ROWS):
        if i < ROWS-2:
            rowString += "||"
            spacesMoved = 0
            copyList = blocks.copy()
            copyList.extend(passive_blocks)
            for b in sort_blocks(copyList):
                if i == b[1]:
                    if b in passive_blocks:
                        square = colored("[]", "blue")
                    else:
                        square = colored("[]", "red")
                    rowString += " " * (b[0]-spacesMoved) + square
                    spacesMoved = b[0]+2
            rowString += " " * (width-spacesMoved) + "\n"
        else:
            rowString += "  " + "-" * width + "\n"

    print(rowString)

def check_input():
    global MoveX, MoveY, blocks, passive_blocks, rotationIndex, dropped
    if msvcrt.kbhit():
        c = msvcrt.getwch()
        if c == 'q':
            quit()
        if not keyPressed:
            if c == "d" or c == "c":
                if not ([MoveX+2, MoveY] in passive_blocks):
                    MoveX += 2
                    MoveX = min(width-2, MoveX)    
            elif c == "a" or c == "z":
                if not ([MoveX-2, MoveY] in passive_blocks):
                    MoveX -= 2
                    MoveX = max(0, MoveX)
            elif c == "s" or c == "x":
                rotationIndex += 1
                if rotationIndex >= 4:
                    rotationIndex = 0
            elif c == " ":
                print("DROP")
                MoveY = ROWS-3
                reachedBottom = False
                while not reachedBottom:
                    for p in passive_blocks:
                        for x in blocks:
                            if x == p:
                                reachedBottom = True
                                for b in blocks:
                                    b[1] -= 1
                    for b in blocks:
                        b[1] += 1
                        if b[1] >= ROWS-3:
                            reachedBottom = True
                dropped = True
                # bigOffset = 1
                # for b in blocks:
                #     bigOffset = max(bigOffset, b[1])
                # for p in passive_blocks:
                #     if p[0] == MoveX and p[1] <= MoveY:
                #         MoveY = p[1]-bigOffset
                #     make_blocks(pieceIndex, rotationIndex)
                # Instant DROP key

elapsed_time = 0
fall_timer = 0
coinCollected = False
game_over = False
def gameloop():
    global blocks, passive_blocks, MoveX, MoveY, elapsed_time, fall_timer, game_over, pieceIndex, rotationIndex, dropped
    while True:
        start_time = time.perf_counter()
        check_input()

        if elapsed_time >= 1/20:
            elapsed_time = 0

            if game_over:
                print_board()
                print("You Died!")
                print(f"Final Score: {len(blocks)-1}\n")
                quit()
                
            print_board()

            for b in blocks:
                if (b[1] == ROWS-3) or ([b[0], b[1]+1] in passive_blocks) or dropped:
                    # if (MoveY == ROWS-3) or ([MoveX, MoveY+1] in passive_blocks):
                    # passive_blocks.append([MoveX, MoveY])
                    passive_blocks.extend(blocks)
                    MoveX = startX
                    MoveY = startY
                    dropped = False
                    break

            # blocks = []
            # blocks.append([MoveX, MoveY])
            make_blocks(pieceIndex, rotationIndex)
        
        # if fall_timer >= 3/4:
        if fall_timer >= 3/8:
            fall_timer = 0
            MoveY += 1
            # if (MoveY == ROWS-3) or ([MoveX, MoveY+1] in passive_blocks):
            #     passive_blocks.append([MoveX, MoveY])
            #     MoveX = startX
            #     MoveY = startY

        end_time = time.perf_counter()
        elapsed_time += (end_time-start_time)
        fall_timer += (end_time-start_time)

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