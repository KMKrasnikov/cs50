from cs50 import get_int

# Get height
height = get_int("Height: ")

# Create condition
while height > 8 or height < 1:
    height = get_int("Height: ")

# Prinring blocks
for i in range(height):
    for j in range(height):
        if height > j + i + 1:
            print(" ", end="")
        else:
            print("#", end="")
    print("")