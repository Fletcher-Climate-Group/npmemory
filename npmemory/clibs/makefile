UTIL_CFLAGS = -shared -Wl,-soname,box_average

CC = gcc

ifeq ($(UNAME_S),Linux)
	CFLAGS = -shared -I . -Wl,-soname,box_average -o box_average.so -FPIC
endif
ifeq ($(UNAME_S),Darwin)
	CFLAGS = -o box_average.so
endif

default: clean box_average

box_average:
	$(CC) $(CFLAGS) box_average.c

clean:
	-rm -f box_average.so
