import msvcrt, os, time, random

ROWS = 10+1
width = 10 * 2
MoveX = (width // 2) - 2
MoveY = (ROWS-1) // 2 - 1

passive_blocks = []
snake_head = [MoveX, MoveY]
coinPos = [random.randint(0,width//2-1)*2, random.randint(0, ROWS-2)]
direction=1 #1: right 2: up 3: left 4: down
blocks = [[MoveX, MoveY]]
old_pos = [MoveX, MoveY]
length = 1
keyPressed = False
game_over = False
coinCollected = False

def print_board():
    global blocks
    os.system('cls')
    rowString = ""
    for i in range(ROWS):
        if i == 0:
            rowString += " " + "_" * width + "\n"
        if i < ROWS-1:
            rowString += "|"
            spacesMoved = 0
            copyList = blocks.copy()
            copyList.append(coinPos)
            for b in sort_blocks(copyList):
                if i == b[1]:
                    square = "[]"
                    if (b == snake_head):
                        square = "00"
                    if (b == coinPos):
                        square = "()"
                    rowString += " " * (b[0]-spacesMoved) + square
                    spacesMoved = b[0]+2
            rowString += " " * (width-spacesMoved) + "|" + "\n"
        else:
            rowString += " " + "-" * width + "\n"

    print(rowString)

def check_input():
    global MoveX, MoveY, blocks, direction, keyPressed
    if msvcrt.kbhit():
        c = msvcrt.getwch()
        if c == 'q':
            quit()
        if not keyPressed:
            if c == 'M' or c == "d":
                if direction % 2 == 0:
                    direction = 1
                keyPressed = True
            elif c == 'H' or c == "w":
                if direction % 2 == 1:
                    direction = 2
                keyPressed = True
            elif c == 'K' or c == "a":
                if direction % 2 == 0:
                    direction = 3
                keyPressed = True
            elif c == 'P' or c == "s":
                if direction % 2 == 1:
                    direction = 4
                keyPressed = True

elapsed_time = 0
def gameloop():
    global blocks, MoveX, MoveY, direction, elapsed_time, snake_head, old_pos, length, keyPressed, game_over, coinPos, coinCollected
    while True:
        start_time = time.perf_counter()
        check_input()

        if elapsed_time >= 1/10 * (0.98**(len(blocks)-1)):
        # if elapsed_time >= 1/8:
            keyPressed = False
            elapsed_time = 0

            if game_over:
                print_board()
                print("You Died!")
                print(f"Final Score: {len(blocks)-1}\n")
                quit()
                
            print_board()
            print(f"Score: {len(blocks)-1}")

            if coinCollected:
                length += 1
                coinPos = [random.randint(0,width//2-1)*2, random.randint(0, ROWS-2)]
                closeX = abs(MoveX-coinPos[0]) <= 3
                closeY = abs(MoveY-coinPos[1]) <= 3
                while (coinPos in blocks) or (direction % 2 == 1 and closeX) or (direction % 2 == 0 and closeY):
                    coinPos = [random.randint(0, width//2-1)*2, random.randint(0, ROWS-2)]
                    closeX = abs(MoveX-coinPos[0]) <= 3
                    closeY = abs(MoveY-coinPos[1]) <= 3
                coinCollected = False

            if direction == 1:
                MoveX += 2
            elif direction == 2:
                MoveY -= 1
            elif direction == 3:
                MoveX -= 2
            elif direction == 4:
                MoveY += 1

            if MoveX > width-2:
                MoveX = 0
            if MoveX < 0:
                MoveX = width-2
            if MoveY > ROWS-2:
                MoveY = 0
            if MoveY < 0:
                MoveY = ROWS-2
                
            blocks.append(old_pos)
            old_pos=[MoveX, MoveY]

            if [MoveX, MoveY] == coinPos:
                coinCollected = True

            if len(blocks) > length:
                del blocks[0]

            snake_head = blocks[-1]

            if blocks.count([MoveX, MoveY]) >= 1:
                game_over = True

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