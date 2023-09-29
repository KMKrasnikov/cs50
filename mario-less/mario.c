#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //Input height and range condition
    int height;
    do
    {
        height = get_int("Enter height value(1 to 8): ");
    }
    while (height > 8 || height < 1);
    //Make bricks
    //Column
    for (int y = 0; y < height; y++)
    {
        //Line
        for (int x = 0; x < height; x++)
        {
            if (x >= height - y - 1)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }

        }
        printf("\n");
    }
}