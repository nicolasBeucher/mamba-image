
.PHONY: clean doc

all: doc

clean:
	rm -f *~ *.aux *.lof *.log *.out *.pdf *.toc *.tex

doc: 
	python createPythonRef.py
	cp mamba-pyref.pdf ..
	python createPythonQuickRef.py
	cp mamba-pyquickref.pdf ..
