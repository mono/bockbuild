SOURCES = $(wildcard *.mm)
OBJECTS = $(SOURCES:.mm=.o)
DYLIB =   libmonobjc.2.dylib

CURRENT_VERSION = 2.0.0
COMPATIBILITY_VERSION = 2.0.0

CFLAGS := $(CFLAGS) \
	-mstackrealign \
	-x objective-c++ \

LDFLAGS := $(LDFLAGS) \
	-lobjc \
	-lstdc++ \
	-framework Foundation \
	-shared \
	-install_name $(DYLIB) \
	-compatibility_version $(COMPATIBILITY_VERSION) \
	-current_version $(CURRENT_VERSION)

all: $(SOURCES) $(DYLIB)

$(DYLIB): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

%.o: %.mm
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJECTS) $(DYLIB)
