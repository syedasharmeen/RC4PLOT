import matplotlib.pyplot as plt
import numpy as np

def key_scheduling(key):
    sched = [i for i in range(0, 256)]
    i = 0
    for j in range(0, 256):
        i = (i + sched[j] + key[j % len(key)]) % 256

        tmp = sched[j]
        sched[j] = sched[i]
        sched[i] = tmp
    return sched
def stream_generation(sched):
    stream = []
    i = 0
    j = 0
    while True:
        i = (1 + i) % 256
        j = (sched[i] + j) % 256
        tmp = sched[j]
        sched[j] = sched[i]
        sched[i] = tmp
        yield sched[(sched[i] + sched[j]) % 256]

def encrypt(text, key):
    text = [ord(char) for char in text]
    key = [ord(char) for char in key]
    sched = key_scheduling(key)
    key_stream = stream_generation(sched)
    plt.plot(np.array(range(256)), np.array(sched))
    plt.show()
    print("Key Stream: " ,sched)
    ciphertext = ''
    for char in text:
        enc = str(hex(char ^ next(key_stream))).upper()
        ciphertext += (enc)
    return ciphertext
def decrypt(ciphertext, key):
    ciphertext = ciphertext.split('0X')[1:]
    ciphertext = [int('0x' + c.lower(), 0) for c in ciphertext]
    key = [ord(char) for char in key]

    sched = key_scheduling(key)
    key_stream = stream_generation(sched)

    plaintext = ''
    for char in ciphertext:
        dec = str(chr(char ^ next(key_stream)))
        plaintext += dec
    return plaintext
if __name__ == '__main__':

        plaintext = input('Enter your plaintext: ')
        key = input('Enter your secret key: ')
        result = encrypt(plaintext, key)
        print('Cipher: ')
        print(result)
        result1 = decrypt(result, key)
        print('Decrypted: ')
        print(result1)
