INC=-Isrc
EXEC=librtk
SRC = $(wildcard src/*.c)
SRC += $(wildcard src/rcv/*.c)
#SRC += $(wildcard app/rtkpost/*.cpp)
SRC += $(wildcard app/rnx2rtkp/*.c)

OBJ = $(SRC:.c=.o)
CC_FLAGS += -DTRACE -DIS_DLL 
CC_FLAGS += -fPIC -O0 -g3 -arch arm64 
#CFLAGS = -arch arm64
#LDFLAGS = -arch arm64

#CC_FLAGS += --save-temps
LDFLAGS += -fPIC -arch arm64
#LDFLAGS += -fsanitize=address
#CC_FLAGS += -fsanitize=address 
$(EXEC).dylib: $(OBJ)
	@$(CC) --shared $(LDFLAGS) -g3 -o $@ $(OBJ) $(LIBPATH) $(LIBS)

$(EXEC).a: $(OBJ)
	ar rcs $@ $(OBJ)  $(LIBPATH) $(LIBS)

#	@ar  $(OBJ)  $@ $(OBJ) $(LIBPATH) $(LIBS)

%.o: %.c
	@$(CC) $(CC_FLAGS) $(INC) -c -g3  $< -o $@ 
clean:
	$(RM) $(OBJ)
	$(RM) $(EXEC)	
