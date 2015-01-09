# Makefile pour la partie 1

CC=gcc

PHONY=default clean python c

default:
	@echo "Il vous faut choisir si vous voulez compiler en C ou en Python"
	@echo "Pour cela, veuillez taper make c ou make python"

c: minicipher-c
	rm -f minicipher
	ln -s minicipher-c minicipher

python: main-1.py minicipher.py
	rm -f minicipher
	ln -s main-1.py minicipher
	chmod +x minicipher



minicipher-c: main-1.o minicipher.o
	gcc -o $@ $+

main-1.o: main-1.c minicipher.h




clean:
	rm -f *.o *.pyc minicipher minicipher-c
