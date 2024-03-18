import msvcrt, os, time, random

ROWS = 15+1
MoveX = 8
MoveY = 0
passive_blocks = []
snake_head = [MoveX, MoveY]
snake_tail = [[MoveX-1, MoveY], [MoveX-2, MoveY], [MoveX-3, MoveY], [MoveX-4, MoveY]]
coinPos = [random.randint(0,9)*2, random.randint(0, ROWS-2)]
direction=1 #1: right 2: up 3: left 4: down
blocks = snake_tail.extend(snake_head)
def print_board():
    global MoveX, MoveY, active_blocks
    # while True:
    os.system('cls')
    # print("\033[H\033[J", end="")
    rowString = ""
    for i in range(ROWS):
        if i < ROWS-1:
            rowString += "||"
            spacesMoved = 0
            for b in blocks:
                if i == b[1]:
                    rowString += " " * (b[0]-spacesMoved) + "[]"
                    spacesMoved += b[0]+2
            rowString += "\n"
        else:
            rowString += "  " + "-" * 20 + "\n"
    print(rowString)
    # print(f"MoveY: {MoveY}")
    time.sleep(1/16)


# t2 = threading.Thread(target = print_board)
# t2.start()

def check_input():
    global MoveX, MoveY, active_blocks
    # while True:
    if msvcrt.kbhit():
        c = msvcrt.getwch()
        # d = msvcrt.getch()
        if c == 'q':
            print(f"MoveX: {MoveX}")
            print(f"MoveY: {MoveY}")
            # t2.join()
            quit()
        elif c == 'K' or c == "a":
            # print("LEFT")
            MoveX -= 2
            MoveX = max(0, MoveX)
            for i in blocks:
                i[0] -= 2
                i[0] = max(0, i[0])
        elif c == 'M' or c == "d":
            # print("RIGHT")
            for i in blocks:
                i[0] += 2
                i[0] = min(i[0], 18)
        elif c == 'H' or c == "w":
            # print("UP")
            for i in blocks:
                i[1] -= 1
                i[1] = max(i[1], 0)
        elif c == 'P' or c == "s":
            # print("DOWN")
            for i in blocks:
                i[1] += 1
                i[1] = min(i[1], ROWS-2)
        # elif c != "à":
        #     print(f"\"{c}\"")


# t1 = threading.Thread(target=check_input)
# t1.start()
def gameloop():
    while True:
        print_board()
        check_input()

gameloop()