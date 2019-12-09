INC=-Isrc
EXEC=librtk
SRC = $(wildcard src/*.c)
SRC += $(wildcard src/rcv/*.c)
#SRC += $(wildcard app/rtkpost/*.cpp)
SRC += $(wildcard app/rnx2rtkp/*.c)

OBJ = $(SRC:.c=.o)
CC_FLAGS += -fPIC 
CC_FLAGS += -DTRACE 
#CC_FLAGS += --save-temps
LDFLAGS += -fPIC
$(EXEC).so: $(OBJ)
	@$(CC) --shared $(LDFLAGS) -g3 -o $@ $(OBJ) $(LIBPATH) $(LIBS)

$(EXEC).a: $(OBJ)
	ar rcs $@ $(OBJ)  $(LIBPATH) $(LIBS)

#	@ar  $(OBJ)  $@ $(OBJ) $(LIBPATH) $(LIBS)

%.o: %.c
	@$(CC) $(CC_FLAGS) $(INC) -c -g3  $< -o $@ 
clean:
	$(RM) $(OBJ)
	$(RM) $(EXEC)	
