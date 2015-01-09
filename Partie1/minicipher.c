/*******************************************************
 * minicipher.c : texte à trou pour la première partie *
 *******************************************************/



/***************
 * Chiffrement *
 ***************/


/* Définition des S-Box */
/************************/

int s[16] = {0xe,0x4,0xd,0x1,0x2,0xf,0xb,0x8,
	     0x3,0xa,0x6,0xc,0x5,0x9,0x0,0x7};



/* Définition de la permutation */
/********************************/

int perm[16] = {0,4,8,12,
		1,5,9,13,
		2,6,10,14,
		3,7,11,15};



/* Exécution d'une étape de chiffrement (à faire) */
/**************************************************/

int encrypt_round (int input, int key, int do_perm) {
  /* Paramètres
     ----------
  input   : bloc en entrée de l'étape
  key     : sous-clé de l'étape
  do_perm : si différent de zéro, indique qu'il faut exécuter la
            permutation (permet de gérer la dernière étape sans
            permutation

     Sortie
     ------
  la valeur de sortie de l'étape après calcul
  */

  // Addition de la sous-clé d'étape
  // TODO

  // Application des 4 S-Boxes
  // TODO


  // Si on applique pas la permutation, on peut rendre le résultat
  // tout de suite
  // TODO


  // Sinon, on applique la permutation, en envoyant chaque bit de
  // la sortie des S-Boxes vers sa destination réelle
  // TODO
}



/* Chiffrement complet (à faire) */
/*********************************/

int encrypt (int plaintext, int keys[]) {
  /* Paramètres
     ----------
  plaintext : texte clair en entrée
  keys      : tableau contenant les 5 sous-clés (i.e. la clé complète)

     Sortie
     ------
  la valeur du chiffré
  */

  // TODO
}






/*****************
 * Déchiffrement *
 *****************/


/* Déclaration des opérations inverses des S-Box */
/* et de la permutation                          */
/*************************************************/

int s_inv[16];
int perm_inv[16];


/* Définition des opérations inverses des S-Box */
/* et de la permutation (à faire)               */
/*************************************************/

void init_inverse_ops () {
  // Cette fonction remplit s_inv et perm_inv pour permettre le
  // déchiffrement
  // Il faudra penser à appeler cette fonction AVANT toute
  // opération de déchiffrement

  // TODO
}



/* Exécution d'une étape de déchiffrement (à faire) */
/****************************************************/

int decrypt_round (int input, int key, int do_perm) {
  /* Paramètres
     ----------
  input   : bloc en entrée de l'étape
  key     : sous-clé de l'étape
  do_perm : si différent de zéro, indique qu'il faut exécuter la
            permutation (permet de gérer la première étape sans
            permutation)

     Sortie
     ------
  la valeur de sortie de l'étape après calcul
  */

  // TODO
}



/* Déchiffrement complet (à faire) */
/***********************************/

int decrypt (int ciphertext, int keys[]) {
  /* Paramètres
     ----------
  ciphertext : texte chiffré en entrée
  keys       : tableau contenant les 5 sous-clés (i.e. la clé complète)

     Sortie
     ------  
  la valeur du clair
  */

  // TODO
}





