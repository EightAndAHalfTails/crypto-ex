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



echo "Test du déchiffrement basique (un mot de 16 bits)"
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do
  get_N_hexa_bytes 20
  KEY=$RESULT
  get_N_hexa_bytes 4
  INPUT=$RESULT
  OUTPUT=$( printf "%s" "${INPUT}" | $PROGNAME -d -k "$KEY" 2>&1 )
  echo "  Test $i"
  echo "    Clé = $KEY"
  echo "    Entrée = $INPUT"
  echo "    Ligne de commande = echo -n $INPUT | $PROGNAME -d -k \"$KEY\" 2>&1"
  echo "    Sortie = $OUTPUT"
  echo
done
