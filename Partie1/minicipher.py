#!/usr/bin/python
# -*- coding: latin-1 -*-

########################################################
# minicipher.py : texte � trou pour la premi�re partie #
########################################################


###############
# Chiffrement #
###############


# D�finition des S-Box
s = [0xe,0x4,0xd,0x1,0x2,0xf,0xb,0x8,
     0x3,0xa,0x6,0xc,0x5,0x9,0x0,0x7]



# Definition de la permutation
perm = [0,4,8,12,
        1,5,9,13,
        2,6,10,14,
        3,7,11,15]



# Ex�cution d'une �tape de chiffrement (� faire)
def encrypt_round (input, key, do_perm = True):
   """encrypt_round
   Param�tres
   ----------
   input   : bloc en entr�e de l'�tape
   key     : sous-cl� de l'�tape
   do_perm : si True, indique qu'il faut ex�cuter la permutation
             (permet de g�rer la derni�re �tape sans permutation)
   
   Sortie
   ------
   la valeur de sortie de l'�tape apr�s calcul
   """
   
   # Addition de la sous-cl� d'�tape
   prelim = input^key 
   
   # Application des 4 S-Boxes
   inter = s[ (prelim >> 12) ] << 12 
   inter += s[ (prelim >> 8) & 0xF ] << 8
   inter += s[ (prelim >> 4) & 0xF ] << 4
   inter += s[ prelim & 0xF ] 
   
   # Si on applique pas la permutation, on peut rendre le r�sultat
   # tout de suite
   
   result = inter
   # Sinon, on applique la permutation, en envoyant chaque bit de
   # la sortie des S-Boxes vers sa destination r�elle
   if(do_perm):
      result = 0
      for i in range(len(perm)):
         result += ((inter >> i) & 1) << perm[i]
   return result




# Chiffrement complet (� faire) #
def encrypt (plaintext, keys):
   """encrypt
   Param�tres
   ----------
   plaintext : texte clair en entr�e
   keys      : tableau contenant les 5 sous-cl�s (i.e. la cl� compl�te)
   
   Sortie
   ------
   la valeur du chiffr�
   """
   NUM_ROUNDS = 4
   
   result = plaintext
   for i in range(NUM_ROUNDS):
      result = encrypt_round(result, keys[i], i != NUM_ROUNDS-1)
      
   result ^= keys[NUM_ROUNDS] 

   return result


#################
# D�chiffrement #
#################


# D�claration des op�rations inverses des S-Box
# et de la permutation
s_inv = [0] * 16
perm_inv = [0] * 16


# D�finition des op�rations inverses des S-Box
# et de la permutation (� faire)

def init_inverse_ops ():
   """Cette fonction remplit s_inv et perm_inv pour permettre le
      d�chiffrement.
      Il faudra penser � appeler cette fonction AVANT toute
      op�ration de d�chiffrement.
   """

   # Il faut remplir s_inv et perm_inv pour permettre le
   # d�chiffrement
   for i in range(len(s)):
      s_inv[s[i]] = i

   for i in range(len(perm)):
      perm_inv[perm[i]] = i


# Ex�cution d'une �tape de d�chiffrement (� faire)
def decrypt_round (input, key, do_perm):
   """decrypt_round
   Param�tres
   ----------
   input   : bloc en entr�e de l'�tape
   key     : sous-cl� de l'�tape
   do_perm : si True, indique qu'il faut ex�cuter la permutation
             (permet de g�rer la premi�re �tape sans permutation)
   
   Sortie
   ------
   la valeur de sortie de l'�tape apr�s calcul
   """
   post_perm = input
   if(do_perm):
      post_perm = 0
      for i in range(len(perm_inv)):
         post_perm += ((input >> i) & 1) << perm_inv[i]

   post_sub = s_inv[ (post_perm >> 12) ] << 12 
   post_sub += s_inv[ (post_perm >> 8) & 0xF ] << 8
   post_sub += s_inv[ (post_perm >> 4) & 0xF ] << 4
   post_sub += s_inv[ post_perm & 0xF ]

   result = post_sub ^ key

   return result

# D�chiffrement complet (� faire)
def decrypt (ciphertext, keys):
   """decrypt
   Param�tres
   ----------
   ciphertext : texte chiffr� en entr�e
   keys       : tableau contenant les 5 sous-cl�s (i.e. la cl� compl�te)
   
   Sortie
   ------  
   la valeur du clair
   """

   NUM_ROUNDS = 4
   
   result = ciphertext ^ keys[NUM_ROUNDS] 

   for i in range(NUM_ROUNDS):
      result = decrypt_round(result, keys[-2-i], i != 0)

   return result
