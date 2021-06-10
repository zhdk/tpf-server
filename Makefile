# the compiler: gcc for C program, define as g++ for C++
CC = gcc

# compiler flags:
#  -g    adds debugging information to the executable file
#  -Wall turns on most, but not all, compiler warnings
CFLAGS  =

# the build target executable:
TARGET = tpf-udp-proxy

all: $(TARGET)

$(TARGET): src/$(TARGET).c
	$(CC) $(CFLAGS) -o $(TARGET) src/$(TARGET).c

clean:
	$(RM) $(TARGET)
