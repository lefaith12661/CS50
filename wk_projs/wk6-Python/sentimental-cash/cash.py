# importing library
from cs50 import get_float


def main():

    # Ask how many dollars the customer is owed
    dollars = get_dollars()

    # Calculate the number of quarters to give the customer
    quarters = int(dollars / .25)
    dollars = round((((dollars / .25) - quarters) * .25), 2)

    # Calculate the number of dimes to give the customer
    dimes = int(dollars / .10)
    dollars = round((((dollars / .10) - dimes) * .10), 2)

    # Calculate the number of nickels to give the customer
    nickels = int(dollars / .05)
    dollars = round((((dollars / .05) - nickels) * .05), 2)

    # Calculate the number of pennies to give the customer
    pennies = int(dollars / .01)
    dollars = pennies - pennies

    # Sum coins
    coins = quarters + dimes + nickels + pennies

    # Print total number of coins to give the customer
    print(coins)


# Prompt user
def get_dollars():
    while True:
        dollars = get_float("Change owed: ")
        if dollars > 0.0:
            break
    return dollars


main()