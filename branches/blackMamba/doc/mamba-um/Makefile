all: doc examples

clean:
	rm -f *~ *.aux *.lof *.log *.out *.pdf *.toc mamba-examples.tex
	rm -rf examples_icons examples.html examples_list.php

examples:
	python examples2tex.py
	cp mamba-examples.pdf ..

doc: 
	pdflatex mamba-um.tex; \
	pdflatex mamba-um.tex; \
	latex_count=5 ; \
	while egrep -s 'Rerun (LaTeX|to get cross-references right)' mamba-um.log && [ $$latex_count -gt 0 ] ;\
	    do \
	      echo "Rerunning latex...." ;\
	      pdflatex mamba-um.tex ;\
	      latex_count=`expr $$latex_count - 1` ;\
	    done; \
	cp mamba-um.pdf ..
	

