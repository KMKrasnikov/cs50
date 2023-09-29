from cs50 import get_int


while True:
    try:
        # Number of a credit card
        str_number = input("Number: ")
        # Lunh's algorithm:
        # Convert str to list
        number = [int(i) for i in str(str_number)]
        # Multiply every other digit by 2, starting with the number’s second-to-last digit, and then add those products’ digits together.
        numbers_even = [number[k] * 2 for k in range(len(number) - 2, -1, -2)]
        # Convert list to str
        str_even = ''.join(map(str, numbers_even))
        # Convert str_even to list and sum
        sum_even = sum([int(l) for l in str(str_even)])
        # Convert odds to list and sum
        sum_numbers_odd = sum([number[k] for k in range(len(number) - 1, -1, -2)])
        # Sum odd and even numbers
        sum = sum_even + sum_numbers_odd
        # Convert sum to list
        sum_list = [int(j) for j in str(sum)]

        # Check count of numbers and lunh's algorithm
        if len(number) < 13 or len(number) > 16 or sum_list[len(sum_list) - 1] != 0:
            print("INVALID")
            break

        # Check AMEX
        elif number[0] == 3 and (number[1] == 4 or number[1] == 7) and len(number) == 15:
            print("AMEX")
            break

        # Check MASTERCARD
        elif number[0] == 5 and (number[1] in range(1, 6)) and len(number) == 16:
            print("MASTERCARD")
            break

        # Check VISA
        elif number[0] == 4 and (len(number) == 13 or len(number) == 16):
            print("VISA")
            break

        else:
            print("INVALID")
            break

    except ValueError:
        print("That's not an integer.")

