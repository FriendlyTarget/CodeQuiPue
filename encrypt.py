from hashlib import sha256
from os import urandom
import os
import hashlib
import blowfish
import sys

#Gestion des arguments

#Si le fichier de clé est spécifié, on le charge dans dans la variable key
if len(sys.argv) < 4:
    print("Error : wrong script argument or options. Usage is : <option> <Input file> <Output File> [Custom key file]\nOptions :\n-e : Encrypt the input file into the output file\n-d : Decrypt the input file into the output file\n\nIf no custom key is given, it will generate a random string and ask for a filename (only work for -e option ; for -d option, you need to specify a key file for the script to work).")
    exit(-1)
option = sys.argv[1]
if len(sys.argv) == 5 :
    try:
        with open (sys.argv[4], 'rb') as f_key:
            rawkey = f_key.read()
            iv = bytes(rawkey[:8])
            key = bytes(rawkey [8:])
    except EnvironmentError:
        print("Error : key file not found")
        exit(-1)
#Si le fichier de clé n'est pas spécifié, on le génère et on demande à l'user de nommer le fichier
elif len(sys.argv) == 4  and sys.argv[1] == "-e":
    iv = os.urandom(8)                
    key = os.urandom(56)
    keyfile = input("Please enter a filename for the key : ")
    try :
        with open (keyfile, 'wb') as f_keyfile:
            f_keyfile.write(iv + key)
    except EnvironmentError:
        print ("IO Error")
        exit(-1)
#Si le script est lancé avec l'option -d, il doit y avoir un fichier de clé fournis. Si ce n'est pas le cas, on quitte le script et on prévient l'user spécifiquement 
#de ce problème plutot que de lui envoyer l'erreur générale
elif len(sys.argv) == 4  and option == "-d":                
    print("-d option require a key file to be specified in argument")
    exit(-1)
#Erreur générale si le script est lancé avec de mauvais argument
else:
    print("Error : wrong script argument or options. Usage is : <option> <Input file> <Output File> [Custom key file]\nOptions :\n-e : Encrypt the input file into the output file\n-d : Decrypt the input file into the output file\n\nIf no custom key is given, it will generate a random string and ask for a filename (only work for -e option ; for -d option, you need to specify a key file for the script to work).")
    exit(-1)
    
#Initialisation des variables
file_to_encrypt = sys.argv[2]
output = sys.argv[3]

hashnsalt = blowfish.Cipher(key)

#Lecture du fichier d'entrée
try:
    with open (file_to_encrypt, 'rb') as f_file_to_encrypt:
        text_block = f_file_to_encrypt.read()
except EnvironmentError:
    print("IO Error")
    exit(-1)
    
#On chiffre ou déchiffre en fonction de l'option fournie en argument
match option:
    case "-e":
        result = b"".join(hashnsalt.encrypt_cfb(text_block, iv))
    case "-d": 
        result = b"".join(hashnsalt.decrypt_cfb(text_block, iv))

#Ecriture du fichier de sortie
try:
    with open(output, 'wb') as f_output:
        f_output.write(result)
except EnvironmentError:
    print("IO Error")
    exit(-1)