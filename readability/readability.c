#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    //Input text
    string text = get_string("Text: ");

    //Calculate the number of letters
    float count1 = count_letters(text);

    //Words
    float count2 = count_words(text);

    //Sentences
    float count3 = count_sentences(text);

    //Calcute the average number of letters per 100 words in the text
    float L = count1 / count2 * 100;

    //Calcute the average number of sentences per 100 words in the text
    float S = count3 / count2 * 100;

    //Output result
    float index = 0.0588 * L - 0.296 * S - 15.8;
    if (index > 15)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %.0f\n", roundf(index));
    }
}

//Calculate the number of letters
int count_letters(string text)
{
    int letters = 0;
    int length = strlen(text);
    for (int i = 0; i < length; i++)
    {
        if (isupper(text[i]) || islower(text[i]))
        {
            letters++;
        }
    }
    return letters;
}

//Calculate the number of words
int count_words(string text)
{
    int words = 0;
    int length = strlen(text);
    int k = 0;
    while (k < length)
    {
        if (isupper(text[k]) || islower(text[k]) || text[k] == 39 || text[k] == 45)
        {
            k++;
        }
        else
        {
            words++;
            do
            {
                k++;
            }
            while ((text[k] > 31 && text[k] < 65) || (text[k] > 90 && text[k] < 97) || (text[k] > 122));
        }
    }
    return words;
}

//Calculate the number of sentences
int count_sentences(string text)
{
    int sentences = 0;
    int length = strlen(text);
    for (int l = 0; l < length; l++)
    {
        if (text[l] == '.' || text[l] == '!' || text[l] == '?')
        {
            sentences++;
        }
    }
    return sentences;
}