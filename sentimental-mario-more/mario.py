# Import get_int
from cs50 import get_int

# Get height
height = get_int("Height: ")

# Check condition
while height < 1 or height > 8:
    height = get_int("Height: ")

# Create blocks
for i in range(height):
    for j in range(height):
        if height > i + j + 1:
            print(" ", end="")
        else:
            print("#", end="")

        if j == height - 1:
            print("  ", end="")
            for k in range(height):
                if height > height - k + i:
                    print(" ", end="")
                else:
                    print("#", end="")
    print("")