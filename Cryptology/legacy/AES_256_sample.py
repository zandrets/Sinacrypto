import time
from Crypto.Cipher import AES
import os
from random import randbytes as rng
def encrypt(key, data):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    return cipher.nonce + tag + ciphertext

def decrypt(key, data):
    nonce = data[:AES.block_size]
    tag = data[AES.block_size:AES.block_size * 2]
    ciphertext = data[AES.block_size * 2:]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    
    return cipher.decrypt_and_verify(ciphertext, tag)

def generate_key(size):
    return rng(int(size))

if __name__ == "__main__":
    #tamano de archivo
    org_file=open('test_file.rar', 'rb')
    org_file.seek(0, os.SEEK_END)
    file_size=org_file.tell() #FILE SIZE
    org_file.close
    print(file_size)
    loops=(int(file_size/256)-1)

    #encriptado
    inicio_de_encrypt = time.time()
    newfile=open('Topocrypt.rar', 'wb+')
    org_file=open('test_file.rar', 'rb')
    keys=bytes(generate_key(32))
    crypto=encrypt(keys, org_file.read(256))
    newfile.write(crypto)

    for partition in range(0, loops):
        crypto=encrypt(keys, org_file.read(256))
        newfile.write(crypto)
    #CANT ENCRYPT/DECRYPT CORRECTLY THE LAST ROW
    last_row=org_file.read()
    print(len(last_row))
    newfile.write(last_row)

    newfile.close
    org_file.close
    final_de_encrypt=time.time()
    print('tiempo de encriptado: ', final_de_encrypt - inicio_de_encrypt)
    #encrypted_data=decrypt(keys,encrypt(keys, datas))

    #tamano de archivo encriptado
    #org_file=open('Topocrypt.rar', 'rb')
    #org_file.seek(0, os.SEEK_END)
    #file_size=org_file.tell() #FILE SIZE
    #org_file.close

    #desencriptado
    inicio_unencrypt=time.time()
    newfile=open('Topodecrypt.rar', 'wb+')
    org_file=open('Topocrypt.rar', 'rb')
    loops=(int(file_size/256))

    for partition in range(0, loops):
        decrypto = decrypt(keys, org_file.read(288))
        newfile.write(decrypto)
    #CANT ENCRYPT/DECRYPT CORRECTLY THE LAST ROW
    last_row=org_file.read()
    print(len(last_row))
    newfile.write(last_row)

    newfile.close
    org_file.close
    final_unencrypt=time.time()
    print('tiempo de desencriptado: ', final_unencrypt - inicio_unencrypt)