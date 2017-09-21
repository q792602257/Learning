#include <stdio.h>
#include <unistd.h>

int hw(int num){
    printf("%5d:\tHello,World!\n",num);
    return 0;
}
int main(void){
    for(int i=0;i<20;i++){
//	i = rand() % 1000;
        hw(i);
//	sleep(2);
    }
    return 0;
}
