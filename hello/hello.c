#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Input name
    string name = get_string("What is your name? ");
    //Output
    printf("Hello, %s\n", name);
}