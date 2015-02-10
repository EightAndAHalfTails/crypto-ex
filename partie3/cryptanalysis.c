/*******************************************************
 * main-1.c : squelette gérant la ligne de commande pour
 * la première partie
 *******************************************************/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "minicipher.h"
#include "pairs.c"



int get_k5 (int pairs[][2], int mask, int output_diff) {
  int freqs[65536];
  int i, k5, imax, max;
  int c1, c2;

  for (i=0; i<65536; i++)
    freqs[i] = 0;

  for (k5=0; k5<65536; k5++) {
    if ((k5 & ~ mask) != 0)
      continue;
    i=0;
    while (pairs[i][0] != pairs[i][1]) {
      c1 = pairs[i][0] ^ k5;
      c2 = pairs[i][1] ^ k5;
      c1 = decrypt_round (c1, 0, 0);
      c2 = decrypt_round (c2, 0, 0);
      if (((c1 ^ c2) & mask) == output_diff)
	freqs[k5] += 1;
      i++;
    }
  }
  
  max=0;
  imax=0;
  for (i=0; i<65536; i++) {
    if (freqs[i] > max) {
      imax=i;
      max = freqs[i];
    }
  }
  return imax;
}


int get_k4 (int pairs[][2], int k5, int mask, int mask_key, int output_diff) {
  int freqs[65536];
  int i, k4, imax, max;
  int c1, c2;

  for (i=0; i<65536; i++)
    freqs[i] = 0;

  for (k4=0; k4<65536; k4++) {
    if ((k4 & ~ mask_key) != 0)
      continue;
    i=0;
    while (pairs[i][0] != pairs[i][1]) {
      c1 = pairs[i][0] ^ k5;
      c2 = pairs[i][1] ^ k5;
      c1 = decrypt_round (c1, k4, 0);
      c2 = decrypt_round (c2, k4, 0);
      c1 = decrypt_round (c1, 0, 1);
      c2 = decrypt_round (c2, 0, 1);
      if (((c1 ^ c2) & mask) == output_diff)
	freqs[k4] += 1;
      i++;
    }
  }
  
  max=0;
  imax=0;
  for (i=0; i<65536; i++) {
    if (freqs[i] > max) {
      imax=i;
      max = freqs[i];
    }
  }
  return imax;
}




int main () {
  int k5, k4;

  init_inverse_ops();

  k5 = (get_k5 (pairs_k5_0b00_0606, 0x0f0f, 0x0606) |
	get_k5 (pairs_k5_000d_a0a0, 0xf0f0, 0xa0a0));
  printf ("Cle k5 retrouvee : %4.4x\n", k5);


  k4 = (get_k4 (pairs_k4_delta_in_0040, k5, 0x0f0f, 0x5555, 0x0606) |
	get_k4 (pairs_k4_delta_in_0005, k5, 0xf0f0, 0xaaaa, 0xa0a0));
  printf ("Cle k4 retrouvee : %4.4x\n", k4);

  return 0;
}

