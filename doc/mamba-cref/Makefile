DOX = doxygen

all: doc doc_pdf

clean:
	rm -rf html; rm -rf latex
	rm -f *~

doc_pdf: doc
	@cd latex; \
	pdflatex refman.tex; \
	pdflatex refman.tex; \
	latex_count=5 ; \
	while egrep -s 'Rerun (LaTeX|to get cross-references right)' refman.log && [ $$latex_count -gt 0 ] ;\
	    do \
	      echo "Rerunning latex...." ;\
	      pdflatex refman.tex ;\
	      latex_count=`expr $$latex_count - 1` ;\
	    done; \
	cp refman.pdf ../../mamba-cref.pdf
	
doc: 
	$(DOX) mamba.cfg
