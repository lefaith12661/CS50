# importing library
from cs50 import get_int


def main():
    # prompt user for height
    Height = get_height()

    # Height = 4
    # 0 1 2 3
    # row - 0, (   |#), i = 3
    # row - 1, (  |##), i = 2
    # row - 2, ( |###), i = 1
    # row - 3, (|####), i = 0
    for row in range(Height):
        i = Height - row - 1
        for column in range(Height):
            if column >= i:
                print("#", end="")
            else:
                print(" ", end="")
        print()


def get_height():
    while True:
        h = get_int("Height: ")
        if 1 <= h <= 8:
            break
    return h


main()
