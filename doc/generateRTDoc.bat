Rem ## Mamba RealTime Module Documentation generation batch file ##

Rem this batch files is here to produce the documentation in a windows
Rem environment. 

Rem You will need miktek, doxygen, python and mamba installed on your
Rem computer with the appropriate binaries path included in your
Rem PATH environment variable to make it work. Also make sure that
Rem all the files in directory style/ (mamba latex style mamba.sty, logo image
Rem mamba_logo.png and license icon by.pdf) are foundable as a package for miktex

Rem PYTHON REALTIME REFERENCE
copy style\mamba_logo.pdf rtpy_ref\
copy style\by.pdf rtpy_ref\
pushd rtpy_ref
python createPythonRTRef.py
copy rtpyref-win.pdf ..
del /Q/F mamba_logo.pdf
del /Q/F by.pdf
popd
