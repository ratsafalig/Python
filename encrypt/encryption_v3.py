# Python 3.10.0

import hashlib
from Crypto.Cipher import AES
from tkinter import *
from tkinter.filedialog import askopenfilename


filename = ""
content = b''

encryptExtension = ".enc"
decryptExtension = ".dec"

root = Tk()

F1 = Frame(root)
F1.pack()
F2 = Frame(root)
F2.pack()
F3 = Frame(root)
F3.pack()

labelSecret = Label(F2, text="secret")
entrySecret = Entry(F2)

labelSecret.pack(side = LEFT)
entrySecret.pack(side = RIGHT)

labelFilename = Label(F1, text="default")
labelFilename.pack(side=RIGHT)

def inflate(data : bytes) -> bytes :
    result = bytes()
    for i in range(len(data)):
        left = ((data[i] & 240) >> 4) | (1 << 6)
        right = (data[i] & 15) | (1 << 6)
        result += (left).to_bytes(1, byteorder="big", signed=False)
        result += (right).to_bytes(1, byteorder="big", signed=False)
    return result

def deflate(data : bytes) -> bytes :
    result = bytes()
    for i in range(len(data)):
        if i % 2 == 0:
            left = data[i] & 15
            right = data[i + 1] & 15
            result += ((left << 4) | right).to_bytes(1, byteorder="big", signed=False)
    return result


def encrypt():
    secret = entrySecret.get()
    if len(secret) != 0:
        md5 = hashlib.md5()
        md5.update(secret.encode("utf-8"))
        secretBytes = md5.digest()
        aes = AES.new(secretBytes, AES.MODE_ECB)
        global content
        while (len(content) % 16) != 0:
            content += b'!'
        encryptedContent = aes.encrypt(content)
        file = open(filename + encryptExtension, "wb+")
        file.write(inflate(encryptedContent))
        file.close()

def decrypt():
    secret = entrySecret.get()
    if len(secret) != 0:
        md5 = hashlib.md5()
        md5.update(secret.encode("utf-8"))
        secretBytes = md5.digest()
        aes = AES.new(secretBytes, AES.MODE_ECB)
        global content
        decryptedContent = aes.decrypt(deflate(content))
        file = open(filename + decryptExtension, "wb+")
        file.write(decryptedContent)
        file.close()

def onButtonAskOpenFilename():
    global filename
    filename = askopenfilename()
    labelFilename.config(text=filename)
    file = open(filename, mode="rb")
    global content
    content = file.read()
    file.close()

buttonAskOpenFilename = Button(F1, text="askOpenFilename", command=onButtonAskOpenFilename)
buttonAskOpenFilename.pack(side=LEFT)

buttonEncrypt = Button(F3, text="encrypt", command=encrypt)
buttonDecrypt = Button(F3, text="decrypt", command=decrypt)

buttonEncrypt.pack(side = LEFT)
buttonDecrypt.pack(side = RIGHT)

root.mainloop()