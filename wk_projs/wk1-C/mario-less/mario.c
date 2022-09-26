#include <cs50.h>
#include <stdio.h>

int main(void) {
    int h;
    do {
        h = get_int("Height: ");
    } while ((h < 1) || (h > 8));

    // number of rows, i = row
    for (int row = 0; row < h; row++) {
        // // convert to right aligned staircase
        // for (int j = 0 ; j < h - i - 1; j++)
        // {
        //     printf(" ");
        // }
        // // number of # columns
        // // b/c column loop is nested in the row loop,
        // // everytime row increased, column is initialized to 0
        // for (int k = 0; k <= i; k++)
        // {
        //     printf("#"); //print #
        // }

        int i = h - row - 1;
        // h = 4
        //           0 1 2 3
        // row - 0, (   |#), i = 3
        // row - 1, (  |##), i = 2
        // row - 2, ( |###), i = 1
        // row - 3, (|####), i = 0
        for (int column = 0; column < h; column++) {

            // if before line -> #
            if (column < i) {
                printf(" ");
            }
            // else (after line) -> ' '
            else {
                printf("#");
            }
        }

        printf("\n");  // new line
    }
}





// int x


// // double x n times
// // if n = 3, double x three times
// // if n = 7, double x seven times

// for (int i = 0; i < n; i++) {
//     x = x * 2;
// }
