#include "helpers.h"
#include <math.h>
#include <cs50.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int avg = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);

            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtRed = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // create variables
            int orginalBlue = image[i][j].rgbtBlue;
            int orginalGreen = image[i][j].rgbtGreen;
            int orginalRed = image[i][j].rgbtRed;

            // find the pixel values and storing them in new variables
            int sepiaBlue = round(.272 * orginalRed + .534 * orginalGreen + .131 * orginalBlue);
            int sepiaGreen = round(.349 * orginalRed + .686 * orginalGreen + .168 * orginalBlue);
            int sepiaRed = round(.393 * orginalRed + .769 * orginalGreen + .189 * orginalBlue);

            // if pixel = 255, then set to 255 pixels
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            // assign the updated pixel values to image
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtRed = sepiaRed;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        // width/2 bc if it loops thru the whole thing, the image will go back to normal
        for (int j = 0; j < width / 2; j++)
        {
            // create a temporary variable
            RGBTRIPLE tmp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = tmp;
        }
    }
    return;
}


// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // create a copy of image
    RGBTRIPLE copy[height][width];

    // nested for loop to copy 'image' into 'copy'
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // loop thru 'image'
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int ttl_red = 0;
            int ttl_blue = 0;
            int ttl_green = 0;

            // use counter to keep track of how many time a piece of code is executed
            float counter = 0.00;

            // find the surrounding pixels
            for (int k = 0; k < 3; k++)
            {
                for (int l = 0; l < 3; l++)
                {
                    int curr_k = i + k - 1;
                    int curr_l = j + l - 1;

                    // exclude the corner pixels and add up all the diff colored pixels
                    if (curr_k >= 0 && curr_l >= 0 && curr_k < height && curr_l < width)
                    {
                        ttl_red += image[curr_k][curr_l].rgbtRed;
                        ttl_blue += image[curr_k][curr_l].rgbtBlue;
                        ttl_green += image[curr_k][curr_l].rgbtGreen;

                        counter++;
                    }
                }

                // calc average of surrounding pixels
                copy[i][j].rgbtRed = round(ttl_red / counter);
                copy[i][j].rgbtBlue = round(ttl_blue / counter);
                copy[i][j].rgbtGreen = round(ttl_green / counter);
            }
        }
    }

    // write new pixels into 'image'
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }
    return;

}
