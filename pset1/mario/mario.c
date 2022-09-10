#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height = 0;

    do
    {
        height = get_int("Height: ");
    }
    while (height <= 0 || height >= 9);

    for (int i = 1; i <= height; i++)
    {
        int spaces = height;

        while (spaces > i)
        {
            spaces--;
            printf(" ");
        }

        for (int left = 0; left < i; left++)
        {
            printf("#");
        }
        printf(" ");
        printf(" ");

        for (int right = 0; right < i; right++)
        {
            printf("#");
        }

        printf("\n");
    }

}