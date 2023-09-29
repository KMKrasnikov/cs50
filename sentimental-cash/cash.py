from cs50 import get_float


def main():
    while True:
        try:
            total = get_float("Change owed: ")
            if total > 0:
                break
        except ValueError:
            print("That's not a float.")

    # Number of coins
    coins = get_coins(total)
    print(f"{coins}")


def get_coins(total):
    # Number of quarters
    quarters = total // 0.25
    total = round(total - quarters * 0.25, 2)
    # Number of dimes
    dimes = total // 0.10
    total = round(total - dimes * 0.10, 2)
    # Number of nickels
    nickels = total // 0.05
    total = round(total - nickels * 0.05, 2)
    # Number of pennies
    pennies = total // 0.01
    coins = int(quarters + dimes + nickels + pennies)
    return coins


if __name__ == "__main__":
    main()
