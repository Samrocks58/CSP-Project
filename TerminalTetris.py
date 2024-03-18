import msvcrt, threading, os, time

ROWS = 15+1
MoveX = 8
MoveY = 0
blocks = [(MoveX, MoveY), (18, 10)]          
def print_board():
    global MoveX, MoveY, blocks
    # while True:
    os.system('cls')
    # print("\033[H\033[J", end="")
    rowString = ""
    for i in range(ROWS):
        if i < ROWS-1:
            # for b in blocks:
            if i == MoveY:
                rowString += "||" + " " * MoveX + "[]" + "\n"
            else:
                rowString += "|| \n"
        else:
            rowString += "  " + "-" * 20 + "\n"
    print(rowString)
    # print(f"MoveY: {MoveY}")
    time.sleep(1/120)


# t2 = threading.Thread(target = print_board)
# t2.start()

def check_input():
    global MoveX, MoveY, blocks
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
            blocks = [(MoveX, MoveY), (18, 10)]
        elif c == 'M' or c == "d":
            # print("RIGHT")
            MoveX += 2
            MoveX = min(MoveX, 18)
            blocks = [(MoveX, MoveY), (18, 10)]
        elif c == 'H' or c == "w":
            # print("UP")
            MoveY -= 1
            MoveY = max(MoveY, 0)
            blocks = [(MoveX, MoveY), (18, 10)]
        elif c == 'P' or c == "s":
            # print("DOWN")
            MoveY += 1
            MoveY = min(MoveY, ROWS-2)
            blocks = [(MoveX, MoveY), (18, 10)]
        # elif c != "à":
        #     print(f"\"{c}\"")


# t1 = threading.Thread(target=check_input)
# t1.start()
def gameloop():
    while True:
        print_board()
        check_input()

gameloop()