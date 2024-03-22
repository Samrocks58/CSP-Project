import msvcrt, os, time, random

ROWS = 10+1
MoveX = 12
MoveY = 4
passive_blocks = []
snake_head = [MoveX, MoveY]
coinPos = [random.randint(0,9)*2, random.randint(0, ROWS-2)]
direction=1 #1: right 2: up 3: left 4: down
blocks = [[MoveX-4, MoveY], [MoveX-3, MoveY], [MoveX-2, MoveY], [MoveX-1, MoveY], [MoveX, MoveY]]
old_pos = [MoveX, MoveY]
length = 10
keyPressed = False

def print_board():
    global blocks
    os.system('cls')
    rowString = ""
    for i in range(ROWS):
        if i == 0:
            rowString += " " + "_" * 20 + "\n"
        if i < ROWS-1:
            rowString += "|"
            spacesMoved = 0
            copyList = blocks.copy()
            for b in sort_blocks(copyList):
                if i == b[1]:
                    square = "[]"
                    if (b == snake_head):
                        square = "00"
                    rowString += " " * (b[0]-spacesMoved) + square
                    spacesMoved = b[0]+2
            rowString += " " * (20-spacesMoved) + "|" + "\n"
        else:
            rowString += " " + "-" * 20 + "\n"
    print(rowString)

def check_input():
    global MoveX, MoveY, blocks, direction, keyPressed
    if msvcrt.kbhit():
        c = msvcrt.getwch()
        if c == 'q':
            print(f"MoveX: {MoveX}")
            print(f"MoveY: {MoveY}")
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
    global blocks, MoveX, MoveY, direction, elapsed_time, snake_head, old_pos, length, keyPressed
    while True:
        start_time = time.perf_counter()
        check_input()

        if elapsed_time >= 1/8:
            keyPressed = False
            print_board()
            elapsed_time = 0

            # copy = blocks.copy()
            # copy.remove([MoveX, MoveY])

            if direction == 1:
                MoveX += 2
            elif direction == 2:
                MoveY -= 1
            elif direction == 3:
                MoveX -= 2
            elif direction == 4:
                MoveY += 1

            if MoveX > 18:
                MoveX = 0
            if MoveX < 0:
                MoveX = 18
            if MoveY > ROWS-2:
                MoveY = 0
            if MoveY < 0:
                MoveY = ROWS-2

            # if copy.count([MoveX, MoveY]) >= 1:
            print(blocks)
            if blocks.count([MoveX, MoveY]) >= 1:
                print_board()
                print("You Died!\n")
                quit()

            snake_head = [MoveX, MoveY]
            blocks.append(old_pos)
            old_pos=[MoveX, MoveY]

            print(f"len: {len(blocks)}")
            if len(blocks) > length:
                # if blocks[0] == snake_head:
                #     del blocks[1]
                # else:
                del blocks[0]
            

            snake_head = blocks[-1]
            # if not (snake_head in blocks):
            #     # blocks.remove(snake_head)
            #     blocks.append(snake_head)
            #     print("yay")

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