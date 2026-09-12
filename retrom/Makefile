CORE_DIR := nxengine
EXTRACTDIR := $(CORE_DIR)/extract-auto
STATIC_LINKING := 0
include Makefile.common
SOURCES_C += retrom/bridge.c
OBJECTS := $(addprefix .retrom-build/,$(SOURCES_C:.c=.o) $(SOURCES_CXX:.cpp=.o))
FLAGS := -O2 $(INCFLAGS) -DHAVE_INTTYPES_H -D__LIBRETRO__ -DINLINE=inline -DRELEASE_BUILD -DFRONTEND_SUPPORTS_RGB565 -DSINGLE_PRECISION_FLOATS -DMIN_AUDIO_PROCESSING_PER_FRAME
EXPORTS := _malloc,_free,_retrom_abi,_retrom_load,_retrom_step,_retrom_key,_retrom_ready,_retrom_width,_retrom_height,_retrom_fps,_retrom_pixels,_retrom_audio,_retrom_audio_count,_retrom_stop
all: $(OBJECTS)
	em++ $(OBJECTS) -O2 -o /output/nxengine-retrom.mjs -sMODULARIZE=1 -sEXPORT_ES6=1 -sALLOW_MEMORY_GROWTH=1 -sENVIRONMENT=web,node -sFILESYSTEM=1 -sSTACK_SIZE=1048576 -sEXPORTED_FUNCTIONS=$(EXPORTS) -sEXPORTED_RUNTIME_METHODS=FS,HEAPU8,HEAP16
.retrom-build/%.o: %.c
	@mkdir -p $(dir $@)
	emcc $(FLAGS) -MMD -MP -c $< -o $@
.retrom-build/%.o: %.cpp
	@mkdir -p $(dir $@)
	em++ $(FLAGS) -MMD -MP -c $< -o $@
-include $(OBJECTS:.o=.d)
