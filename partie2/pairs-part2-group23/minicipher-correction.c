/*******************************************************
 * minicipher.c : texte � trou pour la premi�re partie *
 *******************************************************/



/***************
 * Chiffrement *
 ***************/


/* D�finition des S-Box */
/************************/

int s[16] = {0xe,0x4,0xd,0x1,0x2,0xf,0xb,0x8,
	     0x3,0xa,0x6,0xc,0x5,0x9,0x0,0x7};



/* D�finition de la permutation */
/********************************/

int perm[16] = {0,4,8,12,
		1,5,9,13,
		2,6,10,14,
		3,7,11,15};



/* Ex�cution d'une �tape de chiffrement (� faire) */
/**************************************************/

int encrypt_round (int input, int key, int do_perm) {
  /* Param�tres
     ----------
  input   : bloc en entr�e de l'�tape
  key     : sous-cl� de l'�tape
  do_perm : si diff�rent de z�ro, indique qu'il faut ex�cuter la
            permutation (permet de g�rer la derni�re �tape sans
            permutation

     Sortie
     ------
  la valeur de sortie de l'�tape apr�s calcul
  */

  int temp, result, i, p;

  // Addition de la sous-cl� d'�tape
  temp = input ^ key;

  // Application des 4 S-Boxes
  result = 0;
  for (i=0; i<16; i+=4)
    result |= (s[(temp >> i) & 0xf] << i);

  // Si on applique pas la permutation, on peut rendre le r�sultat
  // tout de suite
  if (do_perm == 0)
    return result;

  // Sinon, on applique la permutation, en envoyant chaque bit de
  // la sortie des S-Boxes vers sa destination r�elle
  temp = result;
  result = 0;
  p = 1;
  for (i=0; i<16; i++, p<<=1)
    if (temp & p)
      result |= (1 << perm[i]);

  return result;
}



/* Chiffrement complet (� faire) */
/*********************************/

int encrypt (int plaintext, int keys[]) {
  /* Param�tres
     ----------
  plaintext : texte clair en entr�e
  keys      : tableau contenant les 5 sous-cl�s (i.e. la cl� compl�te)

     Sortie
     ------
  la valeur du chiffr�
  */

  int i;
  int temp = plaintext;

  // Application des 4 �tapes de chiffrement
  // (attention � ne pas effectuer la derni�re permutation)
  for (i=0; i<4; i++)
    temp = encrypt_round (temp, keys[i], i!=3);
  
  // Enfin, on ajoute la derni�re sous-cl� � la fin
  temp ^= keys[4];

  return temp;
}






/*****************
 * D�chiffrement *
 *****************/


/* D�claration des op�rations inverses des S-Box */
/* et de la permutation                          */
/*************************************************/

int s_inv[16];
int perm_inv[16];


/* D�finition des op�rations inverses des S-Box */
/* et de la permutation (� faire)               */
/*************************************************/

void init_inverse_ops () {
  // Cette fonction remplit s_inv et perm_inv pour permettre le
  // d�chiffrement
  // Il faudra penser � appeler cette fonction AVANT toute
  // op�ration de d�chiffrement


  int i;
  for (i=0; i<16; i++) {
    s_inv[s[i]]=i;
    perm_inv[perm[i]]=i;
  }
}



/* Ex�cution d'une �tape de d�chiffrement (� faire) */
/****************************************************/

int decrypt_round (int input, int key, int do_perm) {
  /* Param�tres
     ----------
  input   : bloc en entr�e de l'�tape
  key     : sous-cl� de l'�tape
  do_perm : si diff�rent de z�ro, indique qu'il faut ex�cuter la
            permutation (permet de g�rer la premi�re �tape sans
            permutation)

     Sortie
     ------
  la valeur de sortie de l'�tape apr�s calcul
  */


  int temp, result, i, p;

  // On commence par appliquer la permutation si cela est demand�
  if (do_perm != 0) {
    p = 1;
    temp = 0;
    for (i=0; i<16; i++, p<<=1)
      if (input & p)
	temp |= (1 << perm_inv[i]);
  } else {
    temp = input;
  }

  // Ensuite, on applique les S-Boxes inverses
  result = 0;
  for (i=0; i<16; i+=4)
    result |= (s_inv[(temp >> i) & 0xf] << i);
  
  // Addition de la sous-cl� d'�tape
  result ^= key;

  return result;
}



/* D�chiffrement complet (� faire) */
/***********************************/

int decrypt (int ciphertext, int keys[]) {
  /* Param�tres
     ----------
  ciphertext : texte chiffr� en entr�e
  keys       : tableau contenant les 5 sous-cl�s (i.e. la cl� compl�te)

     Sortie
     ------  
  la valeur du clair
  */

  int i;
  int temp = ciphertext;

  // On commence par appliquer la derni�re sous-cl�
  temp ^= keys[4];

  // Application des 4 �tapes de d�chiffrement
  // (attention � ne pas effectuer la premi�re permutation)
  for (i=0; i<4; i++)
    temp = decrypt_round (temp, keys[3-i], i!=0);

  return temp;
}





