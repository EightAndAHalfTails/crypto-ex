#!/usr/bin/python
# -*- coding: latin-1 -*-

import minicipher

from pairs import *
#from pairs_null_key import *


def get_k5 (pairs, mask, output_diff):
   freqs=[0] * 65536

   for k5 in range (65536):
      if (k5 & ~ mask) != 0:
         continue
      for (output, output2) in pairs:
         c=output ^ k5;
         c2=output2 ^ k5;
         c=minicipher.decrypt_round (c, 0, False)
         c2=minicipher.decrypt_round (c2, 0, False)
         
         if ((c ^ c2) & mask) == output_diff:
            freqs[k5] += 1

   max=0
   imax=0
   for i in range (65536):
      if freqs[i] > max:
         imax=i
         max = freqs[i]
   return imax




def get_k4 (pairs, k5, mask, mask_key, output_diff):
   freqs=[0] * 65536

   for k4 in range (65536):
      if (k4 & ~ mask_key) != 0:
         continue
      for (output, output2) in pairs:
         c=output ^ k5;
         c2=output2 ^ k5;

         c=minicipher.decrypt_round (c, k4, False)
         c2=minicipher.decrypt_round (c2, k4, False)
         c=minicipher.decrypt_round (c, 0, True)
         c2=minicipher.decrypt_round (c2, 0, True)
         
         if ((c ^ c2) & mask) == output_diff:
            freqs[k4] += 1

   max=0
   imax=0
   for i in range (65536):
      if freqs[i] > max:
         imax=i
         max = freqs[i]
   return imax

def get_k3 (pairs, k5, k4, mask, mask_key, output_diff):
   freqs=[0] * 65536

   for k3 in range (65536):
      if (k3 & ~ mask_key) != 0:
         continue
      for (output, output2) in pairs:
         c=output ^ k5;
         c2=output2 ^ k5;

         c=minicipher.decrypt_round (c, k4, False)
         c2=minicipher.decrypt_round (c2, k4, False)
         c=minicipher.decrypt_round (c, k3, True)
         c2=minicipher.decrypt_round (c2, k3, True)
         c=minicipher.decrypt_round (c, 0, True)
         c2=minicipher.decrypt_round (c2, 0, True)
         
         if ((c ^ c2) & mask) == output_diff:
            freqs[k3] += 1

   max=0
   imax=0
   for i in range (65536):
      if freqs[i] > max:
         imax=i
         max = freqs[i]
   return imax


def get_k2 (pairs, k5, k4, k3, mask, mask_key, output_diff):
   freqs=[0] * 65536

   for k2 in range (65536):
      if (k2 & ~mask_key) != 0:
         continue
      for (output, output2) in pairs:
         c=output ^ k5;
         c2=output2 ^ k5;
         c=minicipher.decrypt_round (c, k4, False)
         c2=minicipher.decrypt_round (c2, k4, False)
         c=minicipher.decrypt_round (c, k3, True)
         c2=minicipher.decrypt_round (c2, k3, True)
         c=minicipher.decrypt_round (c, k2, True)
         c2=minicipher.decrypt_round (c2, k2, True)
         c=minicipher.decrypt_round (c, 0, True)
         c2=minicipher.decrypt_round (c2, 0, True)
         
         if ((c ^ c2) & mask) == output_diff:
            freqs[k2] += 1

   max=0
   imax=0
   for i in range (65536):
      if freqs[i] > max:
         imax=i
         max = freqs[i]
   return imax

def get_k1(pair, k5, k4, k3, k2):
   p, c = pair
   c=c ^ k5;
   c=minicipher.decrypt_round (c, k4, False)
   c=minicipher.decrypt_round (c, k3, True)
   c=minicipher.decrypt_round (c, k2, True)
   c=minicipher.decrypt_round (c, 0, True)
   return p ^ c
      
minicipher.init_inverse_ops()

#my_k5 = (get_k5 (pairs_k5_0b00_0606, 0x0f0f, 0x0606) |
#         get_k5 (pairs_k5_000d_a0a0, 0xf0f0, 0xa0a0))

my_k5 = 0xc7f6
#my_k5 = 0x0000

#my_k4 = (get_k4 (pairs_k4_delta_in_0040, my_k5, 0x0f0f, 0x5555, 0x0606) |
#         get_k4 (pairs_k4_delta_in_0005, my_k5, 0xf0f0, 0xaaaa, 0xa0a0))

my_k4 = 0x78fa
#my_k4 = 0x0000

#my_k3 = (get_k3( pairs_k3_delta_in_0220, my_k5, my_k4, 0x0f0f, 0x5555, 0x0606 )|
#         get_k3( pairs_k3_delta_in_1010, my_k5, my_k4, 0xf0f0, 0xaaaa, 0xa0a0 ))

my_k3 = 0x4ea6
#my_k3 = 0x0000

my_k2 = (get_k2( pairs_k2_delta_in_bbbb, my_k5, my_k4, my_k3, 0x0f0f, 0x5555, 0x0b0b )|
         get_k2( pairs_k2_delta_in_bbbb, my_k5, my_k4, my_k3, 0xf0f0, 0xaaaa, 0xb0b0 ))

my_k1 = get_k1( PC, my_k5, my_k4, my_k3, my_k2)

print "K = {0x%4.4x, 0x%4.4x, 0x%4.4x, 0x%4.4x, 0x%4.4x}" % (my_k1, my_k2, my_k3, my_k4, my_k5)

