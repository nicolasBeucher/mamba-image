Rem ## Mamba Documentation generation batch file ##

Rem this batch files is here to produce the documentation in a windows
Rem environment. 

Rem You will need miktek, doxygen, python and mamba installed on your
Rem computer with the appropriate binaries path included in your
Rem PATH environment variable to make it work. Also make sure that
Rem all the files in directory style/ (mamba latex style mamba.sty, logo image
Rem mamba_logo.png and license icon by.pdf) are foundable as a package for miktex

Rem USER MANUAL
copy style\mamba_logo.pdf mamba-um\
copy style\by.pdf mamba-um\
rem copy style\mamba.sty mamba-um\
pushd mamba-um
rem python examples2tex.py
pdflatex mamba-um.tex
pdflatex mamba-um.tex
pdflatex mamba-um.tex
copy mamba-um.pdf ..
del /Q/F mamba_logo.pdf
del /Q/F by.pdf
rem del /Q/F mamba.sty
popd 

Rem PYTHON REFERENCE
copy style\mamba_logo.pdf mamba-pyref\
copy style\by.pdf mamba-pyref\
pushd mamba-pyref
python createPythonRef.py
copy mamba-pyref.pdf ..
python createPythonQuickRef.py
copy mamba-pyquickref.pdf ..
del /Q/F mamba_logo.pdf
del /Q/F by.pdf
popd

Rem STANDARD
copy style\mamba_logo.pdf mamba-std\
copy style\by.pdf mamba-std\
pushd mamba-std
pdflatex mamba-std.tex
pdflatex mamba-std.tex
copy mamba-std.pdf ..
del /Q/F mamba_logo.pdf
del /Q/F by.pdf
popd

Rem API REFERENCE
pushd mamba-cref
doxygen mamba.cfg
rem copy ..\style\mamba_logo.png html
rem python createDoxygenSty.py
cd latex
copy ..\..\style\mamba_logo.pdf .
copy ..\..\style\by.pdf .
pdflatex refman.tex
pdflatex refman.tex
copy refman.pdf ..\..\mambaapi_ref.pdf
del /Q/F mamba_logo.pdf
del /Q/F by.pdf
popd
