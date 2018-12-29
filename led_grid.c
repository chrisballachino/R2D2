#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <time.h>

#define NUM_LEDS 19

int leds[NUM_LEDS] = {4,17,10,9,11,5,6,13,26,14,15,23,24,25,8,7,12,20,21};

//LED pins are hardcoded for now. Deal with it 
void setup_grid(){
  for(int i = 0; i < NUM_LEDS; i++){
    pinMode(leds[i],OUTPUT);
    digitalWrite(leds[i],0);
  }
}

int set_pin_val(int led_num, uint32_t led_val_raw){
  return (led_val_raw >> led_num)&0x1;
}

//parse 32-bit value into state of individual pins
void generate_led_status(uint32_t led_val_raw){
  for(int i = 0; i < NUM_LEDS; i++){
    //printf("LED %i: %i\n",i,set_pin_val(i,led_val_raw));
    digitalWrite(leds[i],set_pin_val(i,led_val_raw));
  }
}

int main(void){
  setup_grid();
  srand(time(NULL));
  while(1){
    uint32_t led_val_raw = (uint32_t)rand();
    uint32_t time_val = ((uint32_t)rand())%1000000+500000;
    printf("%08x, %f\n",led_val_raw,(double)time_val/1000000);
    generate_led_status(led_val_raw);
    usleep(time_val);
  }
}
