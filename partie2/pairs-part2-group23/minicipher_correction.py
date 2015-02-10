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
def encrypt_round (input, key, do_perm):
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
   temp = input ^ key

   # Application des 4 S-Boxes
   result = 0
   for i in range (0, 16, 4):
      result |= (s[(temp >> i) & 0xf] << i)
   
   # Si on applique pas la permutation, on peut rendre le résultat
   # tout de suite
   if not do_perm:
      return result
   
   # Sinon, on applique la permutation, en envoyant chaque bit de
   # la sortie des S-Boxes vers sa destination réelle
   temp = result
   result = 0
   p = 1
   for i in range (16):
      if temp & p:
         result |= (1 << perm[i])
      p <<= 1

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

   temp = plaintext

   # Application des 4 étapes de chiffrement
   # (attention à ne pas effectuer la dernière permutation)
   for i in range (4):
      temp = encrypt_round (temp, keys[i], i!=3)
  
   # Enfin, on ajoute la dernière sous-clé à la fin
   temp ^= keys[4]

   return temp





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
   for i in range(16):
      s_inv[s[i]]=i
      perm_inv[perm[i]]=i




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
   
   # On commence par appliquer la permutation si cela est demandé
   if do_perm:
      p = 1
      temp = 0
      for i in range(16):
         if (input & p):
            temp |= (1 << perm_inv[i])
         p <<= 1
   else:
      temp = input
   
   # Ensuite, on applique les S-Boxes inverses
   result = 0
   for i in range (0, 16, 4):
      result |= (s_inv[(temp >> i) & 0xf] << i)
   
   # Addition de la sous-clé d'étape
   result ^= key
   
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

   # On commence par appliquer la dernière sous-clé
   temp = ciphertext ^ keys[4]
   
   # Application des 4 étapes de déchiffrement
   # (attention à ne pas effectuer la première permutation)
   for i in range(4):
      temp = decrypt_round (temp, keys[3-i], i!=0)
   
   return temp
