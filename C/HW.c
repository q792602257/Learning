#include <stdio.h>
#include <unistd.h>

void hw(int num){
    printf("%5d:\tHello,World!\n",num);
}
void main(void){
    for(int i=0;i<20;i++){
        hw(i);
    }
}
