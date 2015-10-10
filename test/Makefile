
.PHONY: clean play play3

all: clean play

all3: clean play3

clean:
	rm -rf *~ *.html
	rm -rf testmamba3D/*~ testmamba3D/*.pyc
	rm -rf testmamba/*~ testmamba/*.pyc
	rm -rf tools/*.pyc tools/*~
	rm -rf *.jpg
	rm -rf .coverage
	rm -rf *_cov
	

play:
	python runTest.py -v 2 -o test_run.html -c

play3:
	python3 runTest.py -v 2 -o test_run.html -c

