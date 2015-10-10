
.PHONY: clean docs

all: docs

DOCS = $(shell ls -d mamba*/)

clean:
	rm -f *~ *.pdf
	@for dir in $(DOCS); do \
		(cd $$dir; ${MAKE} clean); \
	done

docs: 
	@for dir in $(DOCS); do \
		(cd $$dir; ${MAKE}); \
	done
	
