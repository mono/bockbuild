ASSEMBLY = Solitary.exe
SOURCE = \
	Solitary.cs \
	Item.cs \
	AssemblyItem.cs \
	NativeLibraryItem.cs \
	Entry.cs \
	Options.cs

all: $(ASSEMBLY)

$(ASSEMBLY): $(SOURCE)
	gmcs -out:$@ -debug $(SOURCE)

Options.cs:
	cp `pkg-config --variable=Sources mono-options` .

clean:
	rm -rf $(ASSEMBLY){,.mdb} Options.cs
