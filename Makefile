################################################################
# Mamba make file
################################################################

.PHONY: clean doc test test3

all: clean doc test

test:
	@cd test; ${MAKE}

test3:
	@cd test; ${MAKE} all3

clean:
	@cd test; ${MAKE} clean
	@cd doc; ${MAKE} clean
	find . -name "*~" -exec rm {} \;
	find . -name "*.pyc" -exec rm {} \;
	find . -depth -name "*__pycache__" -exec rm -r {} \;
	
doc:
	@cd doc; ${MAKE} all

