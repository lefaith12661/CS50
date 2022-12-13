#include <cs50.h>
#include <stdio.h>

int get_cents(void);
int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);
int calculate_pennies(int cents);


// driver, driver function
int main(void)
{
    // Ask how many cents the customer is owed
    int cents = get_cents();

    // Calculate the number of quarters to give the customer
    int quarters = calculate_quarters(cents);
    cents = cents - quarters * 25;

    // Calculate the number of dimes to give the customer
    int dimes = calculate_dimes(cents);
    cents = cents - dimes * 10;

    // Calculate the number of nickels to give the customer
    int nickels = calculate_nickels(cents);
    cents = cents - nickels * 5;

    // Calculate the number of pennies to give the customer
    int pennies = calculate_pennies(cents);
    cents = cents - pennies * 1;

    // Sum coins
    int coins = quarters + dimes + nickels + pennies;

    // Print total number of coins to give the customer
    printf("%i\n", coins);
}

// Prompt user
// Input: nothing/void
// Output: cents
int get_cents(void)
{
    // Declaring cents
    int cents;
    do
    {
        //Defining cents
        cents = get_int("Change owed: ");
    }
    while (cents < 0);

    return cents;
}

// Given cents, returns num of quarters
// Input: cents
// Output: quarter
int calculate_quarters(int cents)
{
    return cents / 25;
}

// Given cents, returns num of dimes
int calculate_dimes(int cents)
{
    return cents / 10;
}

// Given cents, returns num of nickels
int calculate_nickels(int cents)
{
    // Initializing nickels
    int nickels = cents / 5;

    if (cents >= 5)
    {
        return nickels;
    }
    else
    {
        return 0;
    }
}

// Given cents, returns num of pennies
int calculate_pennies(int cents)
{
    //Num of cents = num of pennies
    return cents;
}
