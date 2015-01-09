#!/usr/bin/python
# -*- coding: latin-1 -*-

import sys
import minicipher


###################################
# Gestion de la ligne de commande #
###################################


# Arguments par d�faut #

# Par d�faut, on chiffre
encrypt = True

# Mode de lecture de l'entr�e et d'�criture de la sortie
binary = False

# La cl� par d�faut est la cl� nulle
keys = [0] * 5

# minicipher peut fonctionner en mode monobloc (il ne lit alors que 2
# octets en entr�e) ou en mode CBC avec remplissage (il peut alors
# consid�rer une entr�e de taille quelconque
modeCBC = False

# L'IV, n�cessaire au mode CBC
iv = 0

# Signal de fin de fichier pour le mode CBC
eof = False



# R�cup�ration des arguments sur la ligne de commande #

def usage (msg):
  if len (msg) != 0:
      sys.stderr.write ("%s\n\n" % msg)
  sys.stderr.write ("Usage: %s [-e|-d] [-b] [-1|-M] [-k <key>] [-i <iv>]\n\n" % sys.argv[0])
  sys.stderr.write ("  -e       pour chiffrer les donn�es (par d�faut)\n")
  sys.stderr.write ("  -d       pour d�chiffrer les donn�es\n")
  sys.stderr.write ("  -1       un seul bloc de donn�es sera chiffr� (mode par d�faut)\n")
  sys.stderr.write ("  -b       l'entr�e et la sortie sont binaires (et non des cha�nes hexad�cimales)\n")
  sys.stderr.write ("  -M       l'entr�e peut avoir une taille quelconque (mode CBC)\n")
  sys.stderr.write ("  -k <key> permet de sp�cifier la cl� (80 bits, soit 20 caract�res hexa)\n")
  sys.stderr.write ("           (par d�faut, une cl� nulle est utilis�e)\n")
  sys.stderr.write ("  -i <iv>  permet de sp�cifier l'IV (initial value), dans le cas du mode\n")
  sys.stderr.write ("           CBC (16 bits, soit 4 caract�res hexa)\n")
  sys.stderr.write ("           (par d�faut, un IV nul est utilis�e)\n\n")

  sys.exit (1)


def _4b_from_hexa (c):
  if (c >= '0' and c <= '9'):
    return (ord(c[0]) - ord('0'))
  if (c >= 'A' and c <= 'F'):
    return ((ord(c[0]) - ord ('A')) + 10)
  if (c >= 'a' and c <= 'f'):
    return ((ord(c[0]) - ord ('a')) + 10)
  return 0xff


def read_value (arg, nWords):
  if len (arg) != (nWords * 4):
    raise SyntaxError

  res = [0] * nWords

  for i in range (nWords):
    for j in range (4):
      c = _4b_from_hexa (arg[4*i + j])
      if (c == 0xff):
	raise SyntaxError
      res[i] <<= 4
      res[i] |= c

  return res


def get_opts ():
  global encrypt, binary, keys, modeCBC, iv

  i=1
  while i < len (sys.argv):
    if sys.argv[i][0] != '-':
      usage ("Argument invalide : il doit commencer par un tiret (-).")

    if sys.argv[i][1] == 'e':
      encrypt = True
    elif sys.argv[i][1]=='d':
      encrypt = False
    elif sys.argv[i][1]=='1':
      modeCBC=False
    elif sys.argv[i][1]=='M':
      modeCBC=True
    elif sys.argv[i][1]=='b':
      binary=True

    elif sys.argv[i][1]=='k':
      if len (sys.argv[i]) == 2:
	if len (sys.argv) <= i+1:
	  usage ("L'argument '-k' doit �tre suivi d'une cl� de 20 caract�res hexad�cimaux.")
        i+=1
	argument = sys.argv[i]
      else:
	argument = sys.argv[i][2:]
      try:
        keys = read_value (argument, 5)
      except SyntaxError:
        usage ("Cl� invalide.")
      
    elif sys.argv[i][1]=='i':
      if len (sys.argv[i]) == 2:
	if len (sys.argv) <= i+1:
	  usage ("L'argument '-i' doit �tre suivi d'un IV de 4 caract�res hexad�cimaux.")
        i+=1
	argument = sys.argv[i]
      else:
	argument = sys.argv[i][2:]
      try:
        iv = read_value (argument, 1)[0]
      except SyntaxError:
        usage ("IV invalide.")

    else:
      usage ("Argument inconnu.");

    i+=1



def get_16b_from_stdin (padding):
  global eof, binary

  if not binary:
    input = []
    for i in range (4):
      next = sys.stdin.read(1)
      if (not next) or (_4b_from_hexa (next[0]) == 0xff):
        if padding:
	    eof = True
	    input.append ('8')
            for j in range (4-len (input)):
                input.append ('0')
	    break
        else:
            raise SyntaxError
      input.append (next[0])

    try:
        return read_value (input, 1)[0]
    except SyntaxError:
        if padding:
            eof = True
            return 0x8000
        else:
            raise SyntaxError

  else:
      # encoding == binary
      next = sys.stdin.read (2)
      if len (next) == 2:
          return (ord (next[0]) << 8) | (ord (next[1]))
      elif padding:
          eof=True
          if len (next) == 1:
              return (ord (next[0]) << 8) | 0x80
          else:
              return 0x8000
      else:
          raise SyntaxError


def print_16b (output):
    global binary
    
    if not binary:
        sys.stdout.write ("%4.4x" % output)
    else:
        sys.stdout.write (chr (output >> 8))
        sys.stdout.write (chr (output & 0xff))

  
def print_16b_and_truncate (output):
    global binary

    if not binary:
        if output == 0x8000:
            return
        elif (output & 0xfff) == 0x800:
            sys.stdout.write ("%1.1x" % (output >> 12))
        elif (output & 0xff) == 0x80:
            sys.stdout.write ("%2.2x" % (output >> 8))
        elif (output & 0xf) == 0x8:
            sys.stdout.write ("%3.3x" % (output >> 4))
        else:
            sys.stderr.write ("Erreur de bourrage : le motif de fin n'a pas �t� trouv� !")

    else:
        # encoding == binary
        if output == 0x8000:
            return
        elif (output & 0x00ff) == 0x80:
            sys.stdout.write (chr (output >> 8))
        else:
            sys.stderr.write ("Erreur de bourrage : le motif de fin n'a pas �t� trouv� !")



def main ():
    global encrypt, binary, keys, modeCBC, iv, eof
    
    minicipher.init_inverse_ops ()
    get_opts ()

    if not modeCBC:
        try:
            input = get_16b_from_stdin (False)
        except SyntaxError:
            usage ("L'entr�e doit �tre exprim�e en caract�res hexad�cimaux.")

        if encrypt:
            output = minicipher.encrypt (input, keys)
        else:
            output = minicipher.decrypt (input, keys)

        print_16b (output)

    else:
        # Mode CBC
        if encrypt:
            while not eof:
                input = get_16b_from_stdin (True)
                output = minicipher.encrypt (input ^ iv, keys)
                iv = output ^ input
                print_16b (output)

        else:
            # Decryption
            try:
                input = get_16b_from_stdin (False)
            except SyntaxError:
                return

            while True:
                output = minicipher.decrypt (input, keys) ^ iv
                iv = input ^ output
                try:
                    input = get_16b_from_stdin (False)
                    print_16b (output)
                except SyntaxError:
                    print_16b_and_truncate (output)
                    return

    if not binary:
        sys.stdout.write ('\n')

    sys.exit (0);



main ()
