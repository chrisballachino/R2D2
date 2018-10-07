.PHONY: all
all:
	g++ motor.c -lwiringPi -o motor

.PHONY: clean
clean:
	rm -f motor

.PHONY: run
run:
	sudo ./motor 19 27 7777
