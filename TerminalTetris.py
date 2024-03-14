import msvcrt, threading, os, time

ROWS = 15           
def print_board():
    while True:
        os.system('cls')
        rowString = ""
        for i in range(ROWS):
            if i < ROWS-2:
                rowString += " || \n"
            else:
                rowString += "-" * 40 + "\n"
        print(rowString)
        time.sleep(1/16)

t2 = threading.Thread(target = print_board)
t2.start()

def check_input():
    while True:
        if msvcrt.kbhit():
            c = msvcrt.getwch()
            if c == 'q':
                t2.stop()
                quit()
            elif c == 'K' or c == "a":
                print("LEFT")
            elif c == 'M' or c == "d":
                print("RIGHT")
            elif c == 'H' or c == "w":
                print("UP")
            elif c == 'P' or c == "s":
                print("DOWN")
            # elif c != "à":
            #     print(c)


t1 = threading.Thread(target=check_input)
t1.start()