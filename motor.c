#include <wiringPi.h>
#include <stdio.h>

void setup_motor(int pwm_pin, int direction_pin){
    pinMode(pwm_pin, PWM_OUTPUT);
    pinMode(direction_pin, OUTPUT);
    pwmSetMode(PWM_MODE_MS);
    pwmSetClock(3840);
    pwmSetRange(100);
}

void set_speed(int pwm_pin, int direction_pin, int speed, int direction){
    digitalWrite(direction_pin,direction);
    pwmWrite(pwm_pin,speed);
}

int main(int argc, char* argv[]){
    wiringPiSetupGpio(); //use BCM
    //BCM 19 == wPi 24
    //BCM 27 == wPi 5
    //setup_motor(24,5);
    setup_motor(19,27);

    digitalWrite(27,1);
    int list[] = {10, 25, 50, 75, 95};
    int i = 0;
    for(i = 0; i < 5; i++){
        pwmWrite(19,list[i]);
	printf("Running pwm at %i\n",list[i]);
        delay(3000);
    }
    pwmWrite(19,0);
    delay(1000);
    digitalWrite(27,0);
    for(i = 0; i < 5; i++){
        pwmWrite(19,list[i]);
        printf("Running pwm at %i\n",list[i]);
        delay(3000);
    }

    pwmWrite(19,0);
    return 0;
}
