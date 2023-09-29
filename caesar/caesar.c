#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

bool only_digits(string check);
string rotate(string plaintext, int key);

int main(int argc, string argv[])
{
    //Check 2 arguments
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    //Check if use only digits in key
    string check = argv[1];
    int length = strlen(check);
    for (int i = 0; i < length; i++)
    {
        if (!isdigit(check[i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    int key = atoi(check);
    //Input plaintext
    string plaintext = get_string("plaintext:  ");
    //Coding
    string ciphertext = rotate(plaintext, key);
    printf("ciphertext: %s\n", ciphertext);
}

//Rotate text
string rotate(string plaintext, int key)
{
    //Check key
    key = key % 26;
    //Rotate letters
    for (int k = 0, l = strlen(plaintext); k < l; k++)
    {
        if (isupper(plaintext[k]))
        {
            plaintext[k] = plaintext[k] - 65 + key;
            if (plaintext[k] > 25)
            {
                plaintext[k] = plaintext[k] - 26;
            }
            plaintext[k] = plaintext[k] + 65;
        }
        if (islower(plaintext[k]))
        {
            plaintext[k] = plaintext[k] - 97 + key;
            if (plaintext[k] > 25)
            {
                plaintext[k] = plaintext[k] - 26;
            }
            plaintext[k] = plaintext[k] + 97;
        }
    }
    return plaintext;
}