#include <stdio.h>


int main(){ 
    double e =2.71828-1;
    for (int i=1;i<50;i++){
        e=(e-1)*i;
    }

    FILE *fichier = fopen("answer_banking.txt", "w");

    if (fichier == NULL) {
        printf("Erreur lors de l'ouverture du fichier.\n");
        return 1;
    }

    fprintf(fichier,"%E\n",(e-1));

    fclose(fichier);


    return 0;
}