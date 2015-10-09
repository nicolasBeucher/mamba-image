
.PHONY: clean examples

all: examples

clean:
	rm -f *~ *.aux *.lof *.log *.out *.pdf *.toc mamba-examples.tex
	rm -rf examples_icons examples.html examples_list.php

examples:
	python examples2tex.py
	cp mamba-examples.pdf ..

