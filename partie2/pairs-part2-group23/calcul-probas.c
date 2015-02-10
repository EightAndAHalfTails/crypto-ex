/*******************************************************
 * calcul_probas.c : programme g�n�rant le tableau de  *
 * probabilit�s demand� au d�but de la seconde partie  *
 *******************************************************/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int s[16] = {0xe,0x4,0xd,0x1,0x2,0xf,0xb,0x8,
	     0x3,0xa,0x6,0xc,0x5,0x9,0x0,0x7};


int probas[16][16];


void calcule_probas () {
  // TODO
}


void affiche_probas () {
  int i, delta_in,delta_out;
  char ligne[16*3 + 4 + 1];

  // Affichage de la premi�re ligne
  printf ("   |");
  for (delta_out=0; delta_out<16; delta_out++)
    printf (" %x ", delta_out);
  printf ("\n");

  for (i=0; i<16*3 + 4; i++)
    ligne[i]='-';
  ligne[16*3 + 4] = 0;
  printf ("%s\n", ligne);
  
  for (delta_in=0; delta_in<16; delta_in++) {
    printf (" %x |", delta_in);
    for (delta_out=0; delta_out<16; delta_out++)
      printf ("%2d ", probas[delta_in ][delta_out]);
    printf ("\n");
  }
}


int main () {
  calcule_probas ();
  affiche_probas ();
  return 0;
}
