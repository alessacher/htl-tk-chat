MAKEFLAGS := -j 1
all : doc

.doxygen:
	doxygen Doxyfile

doc: .doxygen
	cd documentation/latex && ${MAKE} all
	cp documentation/latex/refman.pdf doc/documentation.pdf
	rm -rf documentation
