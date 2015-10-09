Rem ## Mamba Documentation generation batch file ##

Rem this batch files is here to produce the documentation in a windows
Rem environment. 

Rem You will need miktek, doxygen, python and mamba installed on your
Rem computer with the appropriate binaries path included in your
Rem PATH environment variable to make it work. Also make sure that
Rem all the files in directory style/ (mamba latex style mamba.sty, logo image
Rem mamba_logo.png and license icon by.pdf) are foundable as a package for miktex

Rem USER MANUAL
pushd mamba-um
pdflatex mamba-um.tex
pdflatex mamba-um.tex
pdflatex mamba-um.tex
copy mamba-um.pdf ..
popd 

Rem EXAMPLES
pushd mamba-examples
python examples2html.py
python examples2tex.py
copy mamba-examples.pdf ..
popd

Rem PYTHON REFERENCE
pushd mamba-pyref
python createPythonRef.py
copy mamba-pyref.pdf ..
python createPythonQuickRef.py
copy mamba-pyquickref.pdf ..
popd

Rem API REFERENCE
Rem This batch works with doxygen 1.8.6 (errors with the latest release)
pushd mamba-cref
doxygen mamba.cfg
cd latex
pdflatex refman.tex
pdflatex refman.tex
pdflatex refman.tex
copy refman.pdf ..\..\mambaapi_ref.pdf
popd
