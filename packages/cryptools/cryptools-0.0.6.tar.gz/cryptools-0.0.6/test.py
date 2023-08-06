import os
import sys
from binascii import unhexlify
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/..')
from cryptools import *

from binascii import hexlify, unhexlify

if __name__ == '__main__':
    print(aes_ecb_decrypt(b'EG\xe8\xe4\x80\x86\x04\x7f\x0epG(\xf8o\x12s', 'cryptoolstestkey')) # b'adb'
    # Ciphers
    # AES
    key = 'cryptoolstestkey'
    assert(aes_ecb_encrypt('adb', key) == '4547e8e48086047f0e704728f86f1273')
    assert(aes_ecb_decrypt(
        unhexlify(b'4547e8e48086047f0e704728f86f1273'), 
        key, output='bytes') == b'adb')
    assert(aes_cbc_encrypt('adb', key, key) == 'ea9d645d6a733dfb92604de5eae16a45')
    assert(aes_cbc_decrypt(
        unhexlify(b'ea9d645d6a733dfb92604de5eae16a45'),
        key, key, output='bytes') == b'adb')
    # RSA
    
    

    # HASH
    assert(sha1('adb') == 'fa1143dea12bffbbc1aa99d5da2ec811d63b5127')
    assert(sha1(b'adb') == 'fa1143dea12bffbbc1aa99d5da2ec811d63b5127')
    assert(md4(b'') == unhexlify(b'31d6cfe0d16ae931b73c59d7e0c089c0'))
    assert(md4(b'adb') == unhexlify(b'f431890473794144d657cf396088a473'))

    assert(rand() == 0xD091BB5C)
    assert(rand() == 0x22AE9EF6)
    seed(251)
    assert(rand() == 0xA33A7D59)
    assert(rand() == 0x8631FB6B)
    mt_init()
    seed(213)
    assert(rand() == 0x37EACD2B)
    assert(rand() == 0x956EB4E4)

