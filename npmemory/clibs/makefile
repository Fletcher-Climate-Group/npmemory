
CC = gcc

CFLAGS=

UNAME_S = $(shell uname -s)
ifeq ($(UNAME_S),Linux)
	CFLAGS += -shared -I . -Wl,-soname,box_average -o box_average.so -FPIC
endif
ifeq ($(UNAME_S),Darwin)
	CFLAGS += -dynamiclib -o box_average.dylib
endif

default: clean box_average

box_average:
	$(CC) $(CFLAGS) box_average.c

clean:
	-rm -f box_average.so
