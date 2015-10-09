
.PHONY: clean doc

all: doc

clean:
	rm -f *~ *.aux *.lof *.log *.out *.pdf *.toc

doc:
	pdflatex mamba-um.tex
	pdflatex mamba-um.tex
	pdflatex mamba-um.tex
	cp mamba-um.pdf ..
	

