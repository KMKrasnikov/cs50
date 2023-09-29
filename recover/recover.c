#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

//New variable
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE");
        return 1;
    }

    // Remember filenames
    char *infile = argv[1];

    // Open input file
    FILE *inptr = fopen(infile, "r");


    // Memory of buffer
    int block_size = 512;
    BYTE *buffer = malloc(block_size * sizeof(BYTE));
    if (buffer == NULL)
    {
        printf("Not enough memory\n");
        fclose(inptr);
        return 3;
    }

    // Open output file
    int i = 0;
    char name[8];
    sprintf(name, "%03i.jpg", i);
    FILE *outptr = fopen(name, "w");
    if (outptr == NULL)
    {
        printf("Could not create.\n");
        free(buffer);
        fclose(inptr);
        return 4;
    }

    // Create new JPEG files
    while (fread(buffer, sizeof(BYTE), block_size, inptr))
    {
        //Create new file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff)
        {
            if (i > 0)
            {
                fclose(outptr);
                sprintf(name, "%03i.jpg", i);
                outptr = fopen(name, "w");
                if (outptr == NULL)
                {
                    printf("Could not create.\n");
                    free(buffer);
                    fclose(inptr);
                    return 4;
                }
            }
            fwrite(buffer, sizeof(BYTE), block_size, outptr);
            i++;
        }
        else
        {
            //Check if file doesn't starts at JPEG bytes
            if (i == 0)
            {
                for (int n = 0; n < block_size; n++)
                {
                    if (buffer[n] == 0xff && buffer[n + 1] == 0xd8 && buffer[n + 2] == 0xff)
                    {
                        fwrite(buffer, sizeof(BYTE), block_size, outptr);
                    }
                }
            }
            //Writing into file
            else
            {
                fwrite(buffer, sizeof(BYTE), block_size, outptr);
            }
        }
    }

    // Close files
    free(buffer);
    fclose(inptr);
    fclose(outptr);
}