import msvcrt, os, time, random

ROWS = 10+1
MoveX = 12
MoveY = 4
passive_blocks = []
snake_head = [MoveX, MoveY]
snake_tail = [[MoveX-1, MoveY], [MoveX-2, MoveY], [MoveX-3, MoveY], [MoveX-4, MoveY]]
coinPos = [random.randint(0,9)*2, random.randint(0, ROWS-2)]
direction=1 #1: right 2: up 3: left 4: down
blocks=[]
blocks.append(snake_head)
old_pos = [MoveX, MoveY]
length = 5
blocks.extend(snake_tail)

def print_board():
    global MoveX, MoveY, blocks
    # while True:
    os.system('cls')
    # print("\033[H\033[J", end="")
    rowString = ""
    for i in range(ROWS):
        if i == 0:
            rowString += " " + "_" * 20 + "\n"
        if i < ROWS-1:
            rowString += "|"
            spacesMoved = 0
            for b in sort_blocks(blocks):
                if i == b[1]:
                    square = "[]"
                    if (b == snake_head):
                        square = "00"
                    rowString += " " * (b[0]-spacesMoved) + square
                    spacesMoved += b[0]+2
            rowString += " " * (20-spacesMoved) + "|" + "\n"
        else:
            rowString += " " + "-" * 20 + "\n"
    print(rowString)
    # print(f"MoveY: {MoveY}")

def check_input():
    global MoveX, MoveY, blocks, direction
    if msvcrt.kbhit():
        c = msvcrt.getwch()
        if c == 'q':
            print(f"MoveX: {MoveX}")
            print(f"MoveY: {MoveY}")
            quit()
        elif c == 'M' or c == "d":
            if direction % 2 == 0:
                direction = 1
        elif c == 'H' or c == "w":
            if direction % 2 == 1:
                direction = 2
        elif c == 'K' or c == "a":
            if direction % 2 == 0:
                direction = 3
        elif c == 'P' or c == "s":
            if direction % 2 == 1:
                direction = 4
        # elif c != "à":
        #     print(f"\"{c}\"")

elapsed_time = 0
def gameloop():
    global blocks, MoveX, MoveY, direction, elapsed_time, snake_head, old_pos, length
    while True:
        start_time = time.perf_counter()
        check_input()

        if elapsed_time >= 1/8:
            print_board()
            elapsed_time = 0

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

            blocks = []
            snake_head = [MoveX, MoveY]
            blocks.append(snake_head)

            blocks.append(old_pos)
            old_pos=(MoveX, MoveY)
            print(len(blocks))
            if len(blocks) > length:
                del blocks[0]

        # time.sleep(1/16)
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