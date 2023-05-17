#include<stdio.h>

int main()

{
    //Variable Declaration
    int i, number;

    //Take User Input
    printf("Enter a number: ");
    scanf("%d", &number);

    //Loop to check if number is perfect square
    for(i = 0; i <= number; i++)
    {
        if(number == i*i)
        {
            printf("\n\n\n\t\t\t%d is a perfect square\n\n\n", number);
            printf("\n\n\t\t\tCoding is Fun !\n\n\n");
            return 0;
        }
    }

    printf("\n\n\n\t\t\t%d is not a perfect square\n", number);
    printf("\n\n\t\t\tCoding is Fun !\n\n\n");
    return 0;
}
