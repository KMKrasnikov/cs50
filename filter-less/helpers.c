#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //Change pixel by pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtBlue = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtGreen = image[i][j].rgbtBlue;
            image[i][j].rgbtRed = image[i][j].rgbtBlue;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int red[height][width];
    int green[height][width];
    int blue[height][width];
    //Change pixel by pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Change red pixel
            red[i][j] = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            if (red[i][j] > 255)
            {
                red[i][j] = 255;
            }
            //Change green pixel
            green[i][j] = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            if (green[i][j] > 255)
            {
                green[i][j] = 255;
            }
            //Change blue pixel
            blue[i][j] = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            if (blue[i][j] > 255)
            {
                blue[i][j] = 255;
            }
            //Make sephia pixels
            image[i][j].rgbtRed = red[i][j];
            image[i][j].rgbtGreen = green[i][j];
            image[i][j].rgbtBlue = blue[i][j];
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //Variables and arrive swap
    RGBTRIPLE swap[height][width];
    int half_width = round(width / 2 - 1);
    //Swap pixels
    for (int i = 0; i < height; i++)
    {
        int j = 0;
        int k = width - 1;
        do
        {
            swap[i][k] = image[i][k];
            image[i][k] = image[i][j];
            image[i][j] = swap[i][k];
            j++;
            k--;
        }
        while (k > half_width);
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    int last_pixel_h = height - 1;
    int last_pixel_w = width - 1;
    //Copy RGBTRIPLE
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Variables
            int red = 0;
            int green = 0;
            int blue = 0;
            float k = 0.0;
            //3x3 arrive
            for (int m = i - 1; m <= i + 1; m++)
            {
                for (int n = j - 1; n <= j + 1; n++)
                {
                    //If overage arrive
                    if (m < 0 || n < 0 || m > last_pixel_h || n > last_pixel_w)
                    {
                        continue;
                    }
                    blue += copy[m][n].rgbtBlue;
                    green += copy[m][n].rgbtGreen;
                    red += copy[m][n].rgbtRed;
                    k++;
                }
            }
            //Make blur pixels
            image[i][j].rgbtBlue = round(blue / k);
            image[i][j].rgbtGreen = round(green / k);
            image[i][j].rgbtRed = round(red / k);
        }
    }
    return;
}
