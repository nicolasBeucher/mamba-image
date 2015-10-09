DOX = doxygen

.PHONY: clean doc doc_pdf

all: doc doc_pdf

clean:
	rm -rf html; rm -rf latex
	rm -f *~

doc_pdf: doc
	@cd latex; \
	pdflatex refman.tex; \
	pdflatex refman.tex; \
	pdflatex refman.tex; \
	cp refman.pdf ../../mamba-cref.pdf

doc:
	$(DOX) mamba.cfg
