import os
import re
import urllib3
from Crypto.Cipher import AES

'''
raw decryption using AES algorithm
NO FILL
'''
def decryptAes(secret, data):
    key = bytes()
    for i in range(len(secret)):
        key += secret[i].to_bytes(4, "big", signed=True)
    aes = AES.new(key, AES.MODE_ECB)
    decryptedData = aes.decrypt(data)
    return decryptedData

'''
raw encryption using AES algorithm
NO FILL
'''
def encryptAes(secret, data):
    key = bytes()
    for i in range(len(secret)):
        key += secret[i].to_bytes(4, "big", signed=True)
    aes = AES.new(key, AES.MODE_ECB)
    encryptedData = aes.encrypt(data)
    return encryptedData

'''
decrypt html string to 123,456 string
FILL WITH ` 
'''
def decryptString(secret, data):
    n = ""
    encryptedData = bytes()
    decryptedData = ""
    j = 0
    for i in range(len(data)):
        if data[i] == ",":
            try:
                encryptedData += int(n).to_bytes(4, byteorder="big", signed=True)
            except:
                encryptedData += int(n).to_bytes(4, byteorder="big")
            j += 1
            if j % 4 == 0:
                temp = decryptAes(secret=secret, data=encryptedData)
                _1 = str(chr(int.from_bytes(temp[0 : 4], byteorder="big", signed=True)))
                _2 = str(chr(int.from_bytes(temp[4 : 8], byteorder="big", signed=True)))
                _3 = str(chr(int.from_bytes(temp[8 : 12], byteorder="big", signed=True)))
                _4 = str(chr(int.from_bytes(temp[12 : 16], byteorder="big", signed=True)))
                decryptedData += _1 + _2 + _3 + _4
                encryptedData = bytes()
            n = ""
        else:
            n += data[i]
    encryptedData += int(n).to_bytes(4, byteorder="big", signed=True)
    temp = decryptAes(secret=secret, data=encryptedData)
    _1 = str(chr(int.from_bytes(temp[0 : 4], byteorder="big", signed=True)))
    _2 = str(chr(int.from_bytes(temp[4 : 8], byteorder="big", signed=True)))
    _3 = str(chr(int.from_bytes(temp[8 : 12], byteorder="big", signed=True)))
    _4 = str(chr(int.from_bytes(temp[12 : 16], byteorder="big", signed=True)))
    decryptedData += _1 + _2 + _3 + _4
    
    while decryptedData[len(decryptedData) - 1] == '`':
        decryptedData = decryptedData[:-1]
    
    return decryptedData

'''
encrypt 123,456 string to html string
AUTOMATICALLY REMOVE ` FROM TAIL
'''
def encryptString(secret, data):
    if len(data) % 4 != 0:
        i = len(data) % 4
        for j in range(4 - i):
            data += "`"
    decryptedSegment = bytes()
    encryptedString = ""
    for i in range(len(data)):
        decryptedSegment += ord(data[i]).to_bytes(4, byteorder="big", signed=True)
        if len(decryptedSegment) == 16:
            encryptedSegment = encryptAes(secret=secret, data=decryptedSegment)
            _1 = encryptedSegment[0 : 4]
            _2 = encryptedSegment[4 : 8]
            _3 = encryptedSegment[8 : 12]
            _4 = encryptedSegment[12 : 16]
            _1 = str(int.from_bytes(_1, byteorder="big", signed=True))
            _2 = str(int.from_bytes(_2, byteorder="big", signed=True))
            _3 = str(int.from_bytes(_3, byteorder="big", signed=True))
            _4 = str(int.from_bytes(_4, byteorder="big", signed=True))
            if len(encryptedString) != 0:
                encryptedString += ','
            encryptedString += _1 + "," + _2 + "," + _3 + "," + _4
            decryptedSegment = bytes()
    return encryptedString


def walk(root=".",r=r".*md"):
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if re.search(r, filename): 
                pass

def fetch(r, url="http://localhost:9999"):
    http = urllib3.PoolManager()
    result = http.request("GET", url)
    data = result.data.decode("utf-8")
    try:
        return re.search(r, data).group(0)
    except:
        return ""

'''
encrypt Jekyll with given secret 
OR 
change encrypted Jekyll with given secret
'''
def encryptJekyll(srcSecret=[123,123,123,123], dstSecret=[123,123,123,123] ,urls=[], filenames=[]):
    for i in range(len(urls)):
        filename = filenames[i]
        file = open(filename, "r", encoding="utf-8")
        content = file.read()
        file.close()
        frontmatter = re.search(r"---(.|\s|\n)*?---", content).group(0)
        layout = re.search(r"---(.|\s|\n)*?layout\s*?:\s*?encrypt(.|\s|\n)*?---", frontmatter)
        # layout is not "layout: encrypt"
        if layout is None:
            layout = re.search(r"---(.|\s|\n)*?layout\s*?:(.|\s|\n)*?---", frontmatter)
            if layout is None:
                frontmatter = "---\nlayout: article" + frontmatter[3:]
            article = fetch(url=urls[i], r=r"<article(.|\s|\n)*?article>")
            aside = fetch(url=urls[i], r=r"<aside(.|\s|\n)*?aside>")
            encryptedArticle = encryptString(secret=srcSecret, data=article)
            encryptedAside = encryptString(secret=srcSecret, data=aside)
            frontmatter = re.sub(r"layout\s*?:\s*?[A-Za-z0-9_]+", "layout: encrypt", frontmatter)
            content = frontmatter + "\n" + \
            r"`" + encryptedArticle + r"`{:.article}" + "\n" + \
            r"`" + encryptedAside + r"`{:.aside}"
            file = open(filename, "w+", encoding="utf-8") 
            file.write(content)
            file.flush()
            file.close()
        # layout is "layout: encrypt"
        else:
            article = fetch(url=urls[i], r=r"<code[a-zA-Z0-9_=\"\-\s]+article(.|\n|\s)*?code>")
            aside = fetch(url=urls[i], r=r"<code[a-zA-Z0-9_=\"\-\s]+aside(.|\n|\s)*?code>")
            encryptedArticle = ""
            encryptedAside = ""
            decryptedArticle = ""
            decryptedAside = ""
            newEncryptedArticle = ""
            newEncryptedAside = ""
            try:
                encryptedArticle = re.search(r">(.|\s|\n)*?<", article).group(0)[1:-1]
                decryptedArticle = decryptString(secret=srcSecret, data=encryptedArticle)
                encryptedAside = re.search(r">(.|\s|\n)*?<", aside).group(0)[1:-1]
                decryptedAside = decryptString(secret=srcSecret, data=encryptedAside)
                newEncryptedArticle = encryptString(secret=dstSecret, data=decryptedArticle)
                newEncryptedAside = encryptString(secret=dstSecret, data=decryptedAside)
            except:
                pass
            content = frontmatter + "\n" + \
            r"`" + newEncryptedArticle + r"`{:.article}" + "\n" + \
            r"`" + newEncryptedAside + r"`{:.aside}"
            file = open(filename, "w+", encoding="utf-8") 
            file.write(content)
            file.flush()
            file.close()
        

encryptJekyll(
    srcSecret=[123,123,123,123],
    dstSecret=[123,123,123,1234],
    urls=[
        "http://localhost:9999/2021/04/12/liquid.html"], 
    filenames=[
        "C:\\Users\\ratsafalig\\Desktop\\ratsafalig.github.io\\_posts\\4\\2021-04-12-liquid.md"])


        
