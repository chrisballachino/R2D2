#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <time.h>

int main(void){
  wiringPiSetupGpio();
  pinMode(14,OUTPUT);
  pinMode(15,OUTPUT);
  pinMode(18,OUTPUT);
  digitalWrite(14,1);
  digitalWrite(15,1);
  digitalWrite(18,1);
  return 0;
}
