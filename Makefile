.PHONY: all
all:
	g++ motor.c -lwiringPi -o motor
	g++ dome.c -lwiringPi -lpthread -o dome
	g++ led_grid.c -lwiringPi -o led_grid
	g++ led_grid_on.c -lwiringPi -o led_grid_on

.PHONY: clean
clean:
	rm -f motor

.PHONY: run
run:
	sudo ./motor 19 27 7777 &
	sudo ./dome 16 22 7778 &
	sudo ./dome 2 3 7779 &
