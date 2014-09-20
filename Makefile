INC=-Isrc
EXEC=rtklib.dylib
SRC = $(wildcard src/*.c)
SRC += $(wildcard src/rcv/*.c)
#SRC += $(wildcard app/rtkpost/*.cpp)
SRC += $(wildcard app/rnx2rtkp/*.c)

OBJ = $(SRC:.c=.o)

$(EXEC): $(OBJ)
	@$(CC) --shared $(LDFLAGS) -o $@ $(OBJ) $(LIBPATH) $(LIBS)

%.o: %.c
	@$(CC) $(CC_FLAGS) $(INC) -c  $< -o $@ 
clean:
	$(RM) src/*.o