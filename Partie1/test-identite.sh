#!/bin/bash

PROGNAME="./minicipher"
GROUP=$1

SEED=$(echo "$GROUP" | sha1sum | dd bs=1 count=32 2> /dev/null)

# Attention, N doit etre inferieur à 32 !
get_N_hexa_bytes () {
    RESULT=$(echo "$SEED 0" | md5sum | dd bs=1 count="$1" 2> /dev/null)
    SEED=$(echo "$SEED 1" | md5sum | dd bs=1 count=32 2> /dev/null)
}


echo "Test de la presence de l'executable"
if [ -x "$PROGNAME" ]; then
  echo "OK"
else
  echo "NOK"
  exit -1
fi



echo "Test d'identité sur des mots de 16 bits"
for i in 1 2 3 4 5 6 7 8 9 10; do
  get_N_hexa_bytes 20
  KEY=$RESULT
  get_N_hexa_bytes 4
  INPUT=$RESULT
  OUTPUT=$( printf "%s" "${INPUT}" | $PROGNAME -k "$KEY" 2>&1 )
  ID=$( printf "%s" "${OUTPUT}" | $PROGNAME -d -k "$KEY" 2>&1 )
  echo "  Test $i"
  echo "    Clé = $KEY"
  echo "    Entrée = $INPUT"
  echo "    Ligne de commande = echo -n $INPUT | $PROGNAME -k \"$KEY\" 2>&1"
  echo "    Sortie = $OUTPUT"
  echo "    Ligne de commande = echo -n $OUTPUT | $PROGNAME -d -k \"$KEY\" 2>&1"
  echo "    Sortie après déchiffrement = $ID"
  if [ "$ID" == "$INPUT" ]; then
      echo "         OK"
  else
      echo "         NOK"
  fi
  echo
done


echo "Test d'identité sur des mots de longueur arbitraire en mode CBC"
for i in 1 2 4 5 25 26 17 18 19 32; do
  get_N_hexa_bytes 20
  KEY=$RESULT
  get_N_hexa_bytes 4
  IV=$RESULT
  get_N_hexa_bytes $i
  INPUT=$RESULT
  OUTPUT=$( echo -n $INPUT | $PROGNAME -M -i "$IV" -k "$KEY" 2>&1 )
  ID=$( echo -n $OUTPUT | $PROGNAME -d -M -i "$IV" -k "$KEY" 2>&1 )
  echo "  Test sur $i octets"
  echo "    Clé = $KEY"
  echo "    IV = $IV"
  echo "    Entrée = $INPUT"
  echo "    Ligne de commande = echo -n $INPUT | $PROGNAME -M -i \"$IV\" -k \"$KEY\" 2>&1"
  echo "    Sortie = $OUTPUT"
  echo "    Ligne de commande = echo -n $OUTPUT | $PROGNAME -d -M -i \"$IV\" -k \"$KEY\" 2>&1"
  echo "    Sortie après déchiffrement = $ID"
  if [ "$ID" == "$INPUT" ]; then
      echo "         OK"
  else
      echo "         NOK"
  fi
  echo
done


echo "Test d'identité sur des fichiers binaires aléatoires en mode CBC"
for i in 10 20 30 40 50 2048; do
  get_N_hexa_bytes 20
  KEY=$RESULT
  get_N_hexa_bytes 4
  IV=$RESULT
  TEMPFILE=$(mktemp tmpXXXXXXXXXXXXXXXXXXX)
  dd if=/dev/urandom of="$TEMPFILE" bs=512 count="$i"
  ID=$( cat $TEMPFILE | $PROGNAME -b -M -i "$IV" -k "$KEY" 2>&1 | $PROGNAME -b -d -M -i "$IV" -k "$KEY" 2>&1 | diff - $TEMPFILE)
  echo "  Test sur $i secteurs de 512 octets"
  echo "    Clé = $KEY"
  echo "    IV = $IV"
  echo "    Ligne de commande = cat <TEMPFILE> | $PROGNAME -b -M -i \"$IV\" -k \"$KEY\" 2>&1 | $PROGNAME -b -d -M -i \"$IV\" -k \"$KEY\" 2>&1 | cmp - <TEMPFILE>"

  if [ "$ID" == "" ]; then
      echo "         OK"
  else
      echo "         NOK"
      echo "$ID"
  fi
  rm -f $TEMPFILE
  echo
done
