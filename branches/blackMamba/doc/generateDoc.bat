Rem ## Mamba Documentation generation batch file ##

Rem this batch files is here to produce the documentation in a windows
Rem environment. 

Rem You will need miktek, doxygen, python and mamba installed on your
Rem computer with the appropriate binaries path included in your
Rem PATH environment variable to make it work. Also make sure that
Rem all the files in directory style/ (mamba latex style mamba.sty, logo image
Rem mamba_logo.png and license icon by.pdf) are foundable as a package for miktex

Rem USER MANUAL
copy style\mamba_logo.pdf userman\
copy style\by.pdf userman\
pushd userman\
python examples2tex.py
pdflatex mamba-um.tex
pdflatex mamba-um.tex
copy mamba-um.pdf ..
del /Q/F mamba_logo.pdf
del /Q/F by.pdf
popd 

Rem PYTHON REFERENCE
copy style\mamba_logo.pdf py_ref\
copy style\by.pdf py_ref\
pushd py_ref
python createPythonRef.py
copy pyref.pdf ..
python createPythonQuickRef.py
copy pyquickref.pdf ..
del /Q/F mamba_logo.pdf
del /Q/F by.pdf
popd

Rem STANDARD
copy style\mamba_logo.pdf standards\
copy style\by.pdf standards\
pushd standards
pdflatex standards.tex
pdflatex standards.tex
copy standards.pdf ..
del /Q/F mamba_logo.pdf
del /Q/F by.pdf
popd

Rem API REFERENCE
pushd mambaapi_ref
doxygen mamba.cfg
copy ..\style\mamba_logo.png html
python createDoxygenSty.py
cd latex
copy ..\..\style\mamba_logo.pdf .
copy ..\..\style\by.pdf .
pdflatex refman.tex
pdflatex refman.tex
copy refman.pdf ..\..\mambaapi_ref.pdf
del /Q/F mamba_logo.pdf
del /Q/F by.pdf
popd
