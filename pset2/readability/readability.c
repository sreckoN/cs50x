//include files from these libraries
#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

//main body of code

int main(void)
{
    int letters = 0;
    int spaces = 1;
    int chars = 0;

    //get the text
    string input = get_string("Text: ");

    int stringlength = strlen(input);

    for (int i = 0; i < stringlength; i++)
    {
        if ((input[i] >= 'a' && input[i] <= 'z') || (input[i] >= 'A' && input[i] <= 'Z'))
        {
            letters++;
        }
        
        //if character is space
        if (input[i] == ' ')
        {
            spaces++;
        }
            
        //if character is not letter
        if (input[i] == '.' || input[i] == '!' || input[i] == '?')
        {
            chars++;
        }
    }

    float L = (float) letters / (float) spaces * 100;
    float S = (float) chars / (float) spaces * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;

    int grade = round(index);

    printf("Grade %i\n", grade);

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }

    //If index number is 16 or higher, display "Grade 16+"
    if (grade > 16)
    {
        printf("Grade 16+\n");
    }
}