from cs50 import get_int


def main():
    """Asks the user for the height"""
    while True:
        height = get_int("Height: ")
        if (height > 0 and height < 9):
            break

    """Prints the pyramide"""
    for i in range(height):
        hashes = i + 1
        printSpace(height-1-i)
        printHash(hashes)
        printSpace(2)
        printHash(hashes)
        print()


def printSpace(num):
    """Print num spaces"""
    for i in range(num):
        print(" ", end="")
        
        
def printHash(num):
    """Print num hashes"""
    for i in range(num):
        print("#", end="")
        
        
if __name__ == "__main__":
    main()