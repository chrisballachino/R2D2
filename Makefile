.PHONY: all
all:
	g++ motor.c -lwiringPi -o motor
	g++ dome.c -lwiringPi -lpthread -o dome

.PHONY: clean
clean:
	rm -f motor

.PHONY: run
run:
	sudo ./motor 19 27 7777 &
	sudo ./motor 83 84 7778 &
	sudo ./dome 66 67 7779 &
