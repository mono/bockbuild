ASSEMBLY = Solitary.exe
SOURCE = \
	Solitary.cs \
	Item.cs \
	AssemblyItem.cs \
	NativeLibraryItem.cs \
	DataItem.cs \
	SymlinkItem.cs \
	ProcessTools.cs \
	PathExtensions.cs \
	Entry.cs \
	Options.cs

all: $(ASSEMBLY)

$(ASSEMBLY): $(SOURCE)
	gmcs -out:$@ -debug -r:Mono.Posix $(SOURCE)

Options.cs:
	cp `pkg-config --variable=Sources mono-options` .

clean:
	rm -rf $(ASSEMBLY){,.mdb} Options.cs
