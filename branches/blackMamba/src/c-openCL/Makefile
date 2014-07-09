################################################################
# MambaParallel make file
################################################################

all: clean pylib

pylib:
	python encapsulateCL.py
	python setupPL.py build_ext bdist

clean:
	python setupPL.py clean -a
	rm -rf dist
	rm -rf python/mambaParallel/mambaPLCore.py
	rm -rf include-private/cl_srcs.c
	rm -rf swig/mambaPLApi_wrap.c
	find . -name "*~" -exec rm {} \;



