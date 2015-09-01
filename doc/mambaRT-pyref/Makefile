all: doc

clean:
	rm -f *~ *.aux *.lof *.log *.out *.pdf *.toc *.tex

doc: 
	python createPythonRTRef.py
	cp mambaRT-pyref*.pdf ..
