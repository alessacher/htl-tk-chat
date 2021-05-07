MAKEFLAGS := -j 1
all : doc

.doxygen:
	doxygen Doxyfile

doc: .doxygen
	cd documentation/latex && ${MAKE} all
	cp documentation/latex/refman.pdf documentation.pdf
	rm -rf documentation
