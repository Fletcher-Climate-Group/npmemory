UTIL_CFLAGS = -shared -Wl,-soname,box_average

CC = gcc
CFLAGS = -I . -fPIC

default: clean box_average

box_average:
	$(CC) -shared -I . -Wl,-soname,box_average -o box_average.so -FPIC box_average.c

clean:
	-rm -f box_average.so
