#include <stdio.h>
#include <stdlib.h>
#include <time.h>



int main(){
    double compt=0;
    int max =100;
    srand(time(NULL));

    for (int i=0;i<10000;i++){
        
        float x = (float)rand() / ((float)RAND_MAX/max);
        float y = (float)rand() / ((float)RAND_MAX/max);
        float z = (float)rand() / ((float)RAND_MAX/max);
    
        //printf("%f %f %f\n",x,y,z);

        if ((x+y)+z != x+(y+z)){
            compt++;
        }

    }

    FILE *fichier = fopen("answer_associativity.txt", "w");

    if (fichier == NULL) {
        printf("Erreur lors de l'ouverture du fichier.\n");
        return 1;
    }

    fprintf(fichier, "%f pourcents\n",(100-compt/100));

    fclose(fichier);
    return 0;
}