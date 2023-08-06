# cryptools

Python crypto tools designed for ease of use and stability instead of guaranteed performance or cryptographic security.

## Installation
```shell
pip install cryptools
```

## Usage

### Hash

```python
from cryptools import *
sha1('adb')  # 'fa1143dea12bffbbc1aa99d5da2ec811d63b5127'
```

### PRNG

```python
from cryptools import *
# Using Mersenne Twister 19937 and default seed 5489
rand() # 0xD091BB5C
rand() # 0x22AE9EF6
seed(251)
rand() # 0xA33A7D59
rand() # 0x8631FB6B
```

### Cipher
```python
from cryptools import *
aes_ecb_encrypt('adb', 'cryptoolstestkey') # '4547e8e48086047f0e704728f86f1273'
aes_ecb_decrypt(b'EG\xe8\xe4\x80\x86\x04\x7f\x0epG(\xf8o\x12s', 'cryptoolstestkey') # b'adb'
```
