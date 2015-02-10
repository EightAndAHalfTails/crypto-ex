#!/usr/bin/python
# -*- coding: latin-1 -*-

#######################################################
# calcul_probas.py : programme générant le tableau de #
# probabilités demandé au début de la seconde partie  #
#######################################################

import sys


s = [0xe,0x4,0xd,0x1,0x2,0xf,0xb,0x8,
     0x3,0xa,0x6,0xc,0x5,0x9,0x0,0x7]

probas = []

def calcule_probas ():
    global probas, s
    
    pass


def affiche_probas ():
    # Affichage de la première ligne
    sys.stdout.write ("   |")
    for delta_out in range(16):
        sys.stdout.write (" %x " % delta_out)
    sys.stdout.write ("\n")

    sys.stdout.write ('-' * (16*3 + 4))
    sys.stdout.write ("\n")
  
    for delta_in in range (16):
        sys.stdout.write (" %x |" % delta_in)
        for delta_out in range (16):
            sys.stdout.write ("%2d " % probas[delta_in][delta_out])
        sys.stdout.write ("\n")



calcule_probas ()
affiche_probas ()
