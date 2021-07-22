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

def encryptSingleJekyll(url : str, filename : str, secret : bytes):
    file = open(filename, "r", encoding="utf-8")
    content = file.read()
    file.close()
    frontmatter = re.search(r"---(.|\s|\n)*?---", content).group(0)
    if not (re.search(r"---(.|\s|\n)*?layout\s*?:\s*?encrypt(.|\s|\n)*?---", frontmatter) is None):
        return
    article = fetch(url=url, r=r"<article(.|\s|\n)*?article>")
    encryptedArticle = encryptString(secret=secret, data=article).decode("utf-8")
    frontmatter = re.sub(r"layout\s*?:\s*?[A-Za-z0-9_]+", "layout: encrypt", frontmatter)
    content = "" + \
    frontmatter + "\n" + \
    r"`" + encryptedArticle + r"`{:.article}"
    file = open(filename, "wb+") 
    file.write(content.encode("utf-8"))
    file.flush()
    file.close()

def decryptSingleJekyll(secret : bytes, filename : str):
    file = open(filename, "rb+")
    content = file.read()
    content = content.decode("utf-8")
    file.close()
    frontmatter = re.search(r"---(.|\s|\n)*?---", content).group(0)
    if re.search(r"layout\s*?:\s*?encrypt", frontmatter) is None:
        return
    frontmatter = re.sub(r"layout\s*?:\s*?[a-zA-Z0-9_]+", "layout: article", frontmatter)
    encryptedArticle = re.search(r"`(.|\s|\n)*?`{:.article}", content).group(0)[1 : -12]
    decryptedArticle = decryptString(secret=secret, data=encryptedArticle).decode("utf-8")
    file = open(filename, "wb+")
    content = frontmatter + "\n" + \
    decryptedArticle
    file.write(content.encode("utf-8"))
    file.flush()
    file.close()

def encryptAllJekyll(secret, url, _posts, include = [], exclude = []):
    for dirpath, dirnames, filenames in os.walk(_posts):
        for filename in filenames:
            if len(include) > 0 and not (filename in include):
                continue
            else:
                pass
            if len(exclude) > 0 and filename in exclude:
                continue
            else:
                pass
            year = filename[0 : 4]
            month = filename[5 : 7]
            day = filename[8 : 10]
            blogUrl = url + "/" + year + "/" + month + "/" + day + "/" + filename[11 : -3] + ".html"
            blogPath = dirpath + "\\" + filename
            encryptSingleJekyll(url = blogUrl, filename=blogPath, secret=secret)

def decryptAllJekyll(secret, _posts, include=[], exclude=[]):
    for dirpath, dirnames, filenames in os.walk(_posts):
        for filename in filenames:
            if len(include) > 0 and not (filename in include):
                continue
            else:
                pass
            if len(exclude) > 0 and filename in exclude:
                continue
            else:
                pass
            blogPath = dirpath + "\\" + filename
            decryptSingleJekyll(secret=secret, filename=blogPath)

'''
decryptAllJekyll(
    secret=b"1234123412341234",
    _posts="D:\\Users\\Administrator\\Desktop\\ratsafalig.github.io\\_posts")
'''

encryptAllJekyll(
    secret=b"Free2plays!!!igg",
    url="http://localhost:9999",
    _posts="D:\\Users\\Administrator\\Desktop\\ratsafalig.github.io/_posts/igg")

