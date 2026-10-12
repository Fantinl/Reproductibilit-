#include <stdio.h>


int main(){ 
    double e =2.71828-1;
    for (int i=1;i<50;i++){
        e=(e-1)*i;
    }

    printf("%E\n",(e-1));

    return 0;
}