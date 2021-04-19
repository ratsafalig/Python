import os
import re
import urllib3
from Crypto.Cipher import AES

def fetch(r : str, url : str) -> str:
    http = urllib3.PoolManager()
    result = http.request("GET", url)
    data = result.data.decode("utf-8")
    try:
        return re.search(r, data).group(0)
    except:
        return ""

def decryptAes(secret : bytes, data : bytes) -> bytes :
    aes = AES.new(secret, AES.MODE_ECB)
    decryptedData = aes.decrypt(data)
    return decryptedData

def encryptAes(secret : bytes, data : bytes) -> bytes :
    aes = AES.new(secret, AES.MODE_ECB)
    encryptedData = aes.encrypt(data)
    return encryptedData

def decryptString(secret : bytes, data : str) -> bytes :
    srcBytes = data.encode("utf-8")
    srcBytes = deflateBytes(srcBytes)
    srcBytes = decryptAes(secret=secret, data=srcBytes)
    while srcBytes[-1] == 48:
        srcBytes = srcBytes[ : -1]
    return srcBytes

def encryptString(secret : bytes, data : str) -> bytes :
    srcBytes = data.encode("utf-8")
    if len(srcBytes) % 16 != 0:
        lenOfSrcBytes = len(srcBytes)
        for i in range(16 - (lenOfSrcBytes % 16)):
            srcBytes += b'0'
    srcBytes = encryptAes(secret=secret, data=srcBytes)
    return inflateBytes(srcBytes)

def inflateBytes(data : bytes) -> bytes :
    result = bytes()
    for i in range(len(data)):
        left = ((data[i] & 240) >> 4) | (1 << 6)
        right = (data[i] & 15) | (1 << 6)
        result += (left).to_bytes(1, byteorder="big", signed=False)
        result += (right).to_bytes(1, byteorder="big", signed=False)
    return result

def deflateBytes(data : bytes) -> bytes :
    result = bytes()
    for i in range(len(data)):
        if i % 2 == 0:
            left = data[i] & 15
            right = data[i + 1] & 15
            result += ((left << 4) | right).to_bytes(1, byteorder="big", signed=False)
    return result

#################################################################################################################################

def encryptSingleJekyll(url : str, filename : str, srcSecret : bytes, dstSecret : bytes):
    file = open(filename, "r", encoding="utf-8")
    content = file.read()
    file.close()
    frontmatter = re.search(r"---(.|\s|\n)*?---", content).group(0)
    layoutEncrypt = re.search(r"---(.|\s|\n)*?layout\s*?:\s*?encrypt(.|\s|\n)*?---", frontmatter)
    # ! layout: encrypt
    if layoutEncrypt is None:
        article = fetch(url=url, r=r"<article(.|\s|\n)*?article>")
        encryptedArticle = encryptString(secret=dstSecret, data=article).decode("utf-8")
        frontmatter = re.sub(r"layout\s*?:\s*?[A-Za-z0-9_]+", "layout: encrypt", frontmatter)
        content = "" + \
        frontmatter + "\n" + \
        r"`" + encryptedArticle + r"`{:.article}"
        file = open(filename, "wb+") 
        file.write(content.encode("utf-8"))
        file.flush()
        file.close()
    # layout: encrypt
    else:
        article = fetch(url=url, r=r"<code[a-zA-Z0-9_=\"\-\s]+article(.|\n|\s)*?code>")
        encryptedArticle = ""
        decryptedArticle = ""
        newEncryptedArticle = ""
        try:
            encryptedArticle = re.search(r">(.|\s|\n)*?<", article).group(0)[1:-1]
            decryptedArticle = decryptString(secret=srcSecret, data=encryptedArticle).decode("utf-8")
            newEncryptedArticle = encryptString(secret=dstSecret, data=decryptedArticle).decode("utf-8")
        except:
            pass
        content = "" + \
        frontmatter + "\n" + \
        r"`" + newEncryptedArticle + r"`{:.article}"
        file = open(filename, "wb+") 
        file.write(content)
        file.flush()
        file.close()

def decryptSingleJekyll(secret : bytes, filename : str):
    file = open(filename, "rb+")
    content = file.read()
    content = content.decode("utf-8")
    file.close()
    frontmatter = re.search(r"---(.|\s|\n)*?---", content).group(0)
    frontmatter = re.sub(r"layout\s*?:\s*?[a-zA-Z0-9_]+", "layout: article", frontmatter)
    encryptedArticle = re.search(r"`(.|\s|\n)*?`{:.article}", content).group(0)[1 : -12]
    decryptedArticle = decryptString(secret=secret, data=encryptedArticle).decode("utf-8")
    file = open(filename, "wb+")
    content = frontmatter + "\n" + \
    decryptedArticle
    file.write(content.encode("utf-8"))
    file.flush()
    file.close()

encryptSingleJekyll(url="http://localhost:9999/2021/04/11/todo.html", filename="C:/Users/ratsafalig/Desktop/ratsafalig.github.io/_posts/4/2021-04-11-todo.md", srcSecret=b"1234123412341234", dstSecret=b"1234123412341234")

# decryptSingleJekyll(secret=b"1234123412341234", filename="./test.html")

# print(decryptString(secret=b"1234123412341234", data=encryptString(secret=b"1234123412341234", data="123123123").decode("utf-8")))