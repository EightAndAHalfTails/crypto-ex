# Makefile pour la partie 3

CC=gcc

PHONY=default clean python c

default:
	@echo "Il vous faut choisir si vous voulez compiler en C ou en Python"
	@echo "Pour cela, veuillez taper make c ou make python"

c: cryptanalysis-c
	rm -f cryptanalysis
	ln -s cryptanalysis-c cryptanalysis

python: minicipher.py cryptanalysis.py
	rm -f cryptanalysis
	ln -s cryptanalysis.py cryptanalysis
	chmod +x cryptanalysis



cryptanalysis-c: minicipher.o cryptanalysis.o
	gcc -o $@ $+

main-1.o: cryptanalysis.c minicipher.h


clean:
	rm -f *.o *.pyc cryptanalysis cryptanalysis-c
