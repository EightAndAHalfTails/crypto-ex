#!/usr/bin/python
# -*- coding: latin-1 -*-

########################################################
# minicipher.py : texte à trou pour la première partie #
########################################################


###############
# Chiffrement #
###############


# Définition des S-Box
s = [0xe,0x4,0xd,0x1,0x2,0xf,0xb,0x8,
     0x3,0xa,0x6,0xc,0x5,0x9,0x0,0x7]



# Definition de la permutation
perm = [0,4,8,12,
        1,5,9,13,
        2,6,10,14,
        3,7,11,15]



# Exécution d'une étape de chiffrement (à faire)
def encrypt_round (input, key, do_perm = True):
   """encrypt_round
   Paramètres
   ----------
   input   : bloc en entrée de l'étape
   key     : sous-clé de l'étape
   do_perm : si True, indique qu'il faut exécuter la permutation
             (permet de gérer la dernière étape sans permutation)
   
   Sortie
   ------
   la valeur de sortie de l'étape après calcul
   """
   
   # Addition de la sous-clé d'étape
   prelim = input^key 
   
   # Application des 4 S-Boxes
   inter = s[ (prelim >> 12) ] << 12 
   inter += s[ (prelim >> 8) & 0xF ] << 8
   inter += s[ (prelim >> 4) & 0xF ] << 4
   inter += s[ prelim & 0xF ] 
   
   # Si on applique pas la permutation, on peut rendre le résultat
   # tout de suite
   
   result = inter
   # Sinon, on applique la permutation, en envoyant chaque bit de
   # la sortie des S-Boxes vers sa destination réelle
   if(do_perm):
      result = 0
      for i in range(len(perm)):
         result += ((inter >> i) & 1) << perm[i]
   return result




# Chiffrement complet (à faire) #
def encrypt (plaintext, keys):
   """encrypt
   Paramètres
   ----------
   plaintext : texte clair en entrée
   keys      : tableau contenant les 5 sous-clés (i.e. la clé complète)
   
   Sortie
   ------
   la valeur du chiffré
   """
   NUM_ROUNDS = 4
   
   result = plaintext
   for i in range(NUM_ROUNDS):
      result = encrypt_round(result, keys[i], i != NUM_ROUNDS-1)
      
   result ^= keys[NUM_ROUNDS] 

   return result


#################
# Déchiffrement #
#################


# Déclaration des opérations inverses des S-Box
# et de la permutation
s_inv = [0] * 16
perm_inv = [0] * 16


# Définition des opérations inverses des S-Box
# et de la permutation (à faire)

def init_inverse_ops ():
   """Cette fonction remplit s_inv et perm_inv pour permettre le
      déchiffrement.
      Il faudra penser à appeler cette fonction AVANT toute
      opération de déchiffrement.
   """

   # Il faut remplir s_inv et perm_inv pour permettre le
   # déchiffrement
   for i in range(len(s)):
      s_inv[s[i]] = i

   for i in range(len(perm)):
      perm_inv[perm[i]] = i


# Exécution d'une étape de déchiffrement (à faire)
def decrypt_round (input, key, do_perm):
   """decrypt_round
   Paramètres
   ----------
   input   : bloc en entrée de l'étape
   key     : sous-clé de l'étape
   do_perm : si True, indique qu'il faut exécuter la permutation
             (permet de gérer la première étape sans permutation)
   
   Sortie
   ------
   la valeur de sortie de l'étape après calcul
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

# Déchiffrement complet (à faire)
def decrypt (ciphertext, keys):
   """decrypt
   Paramètres
   ----------
   ciphertext : texte chiffré en entrée
   keys       : tableau contenant les 5 sous-clés (i.e. la clé complète)
   
   Sortie
   ------  
   la valeur du clair
   """

   NUM_ROUNDS = 4
   
   result = ciphertext ^ keys[NUM_ROUNDS] 

   for i in range(NUM_ROUNDS):
      result = decrypt_round(result, keys[-2-i], i != 0)

   return result
