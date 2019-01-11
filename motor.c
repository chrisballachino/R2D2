#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

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

void print_usage(){
    printf("sudo ./motor pwm_pin direction_pin udp_port\n");
    printf("Notes:\n");
    printf("  -Running this without sudo will fuck everything up\n");
    printf("  -Pins are BCM notation - run gpio readall to get mappings\n");
    printf("  -Check the pins you're using - wrong pins will also fuck everything up\n");
    printf("  -For multiple motors, use multiple instances\n");
}

int setup_socket(int port, int& sock){
    struct sockaddr_in servaddr;

    memset(&servaddr,0,sizeof(servaddr));

    //filling server information
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(port);

    //create socket
    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0){
        printf("Creating socket failed\n");
        printf("Errno %i\n",errno);
        return -1;
    }

    //bind socket
    if(bind(sock,
           (const struct sockaddr*)&servaddr,
           sizeof(servaddr)) < 0 ){
        printf("Socket bind to port %i failed\n",port);
        printf("Errno %i\n",errno);
        return -1;
    }

    return 0;
}

void test_functionality(int pwm_pin, int direction_pin){
    digitalWrite(direction_pin,1);
    int list[] = {10, 25, 50, 75, 95};
    int i = 0;
    for(i = 0; i < 5; i++){
        pwmWrite(pwm_pin,list[i]);
	printf("Running pwm at %i\n",list[i]);
        delay(3000);
    }
    pwmWrite(pwm_pin,0);
    delay(1000);
    digitalWrite(direction_pin,0);
    for(i = 0; i < 5; i++){
        pwmWrite(pwm_pin,list[i]);
        printf("Running pwm at %i\n",list[i]);
        delay(3000);
    }

    pwmWrite(pwm_pin,0);
}

int main(int argc, char* argv[]){
    if(argc != 4){
        print_usage();
        return -1;
    }

    FILE* fp = fopen("motor.log","a");

    int pwm_pin = atoi(argv[1]);
    int direction_pin = atoi(argv[2]);
    int port = atoi(argv[3]);

    int sock = 0;
    struct sockaddr_in cliaddr;
    memset(&cliaddr,0,sizeof(cliaddr));

    int last_speed = -1;
    time_t startTime;
    time_t currentTime;

    time(&startTime);

    if(setup_socket(port,sock) < 0){
        return -1;
    }

    wiringPiSetupGpio(); //use BCM
    setup_motor(pwm_pin,direction_pin);

    pwmWrite(pwm_pin,0);

    //test_functionality(pwm_pin,direction_pin);
    while(1){
        socklen_t len = 0;
        int n = 0;
        char data[64];
        n = recvfrom(sock,
                     (char*)data,
                     64,
                     MSG_WAITALL,
                     (struct sockaddr*)&cliaddr,
                     &len);

        if(n != 2){
            printf("Received improper packet size %i\n",n);
            fprintf(fp,"Received improper packet size %i\n",n);
            fflush(fp);
        }
        else{
            int speed = (int)data[0];
            int direction = (int)data[1];
            bool validPacket = true;
            bool allowChange = true;

            if(speed < 0 || speed > 100){
                validPacket = false;
            }

            if(direction != 0 && direction != 1){
                validPacket = false;
            }

            if(speed == last_speed){
                //allowChange = false;
            }
            last_speed = speed;

            if(validPacket == true && allowChange == true){
                time(&currentTime);
//                if(difftime(currentTime,startTime)>1){
                    digitalWrite(direction_pin,direction);
                    pwmWrite(pwm_pin,speed);
                    printf("Recv: speed %x, direction %i\n",(int)speed,direction);
                    fprintf(fp,"Recv: speed %x, direction %i\n",(int)speed,direction);
                    fflush(fp);
                    startTime = currentTime;
//                }
            }
            else if(allowChange == false){
                printf("Recv: speed %x, direction %i, allowChange == false\n",(int)speed,direction);
                fprintf(fp,"Recv: speed %x, direction %i, allowChange == false\n",(int)speed,direction);
                fflush(fp);
            }
        }
    }

    return 0;
}
