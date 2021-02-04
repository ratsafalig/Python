import scrapy;
import scrapy
import scrapy.spiders
import scrapy.linkextractors 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import sys
import os
import time

rootDir = "C:/"

abc_txt = open("C:/Users/ratsafalig/Desktop/abc.txt", "a")

def walk(rootDir):
    try:
        dirs = os.listdir(rootDir)
    except Exception:
        print("error on path " + rootDir)
    else:
        for i in range(0, len(dirs)):
            path = os.path.join(rootDir, dirs[i])
            if os.path.isdir(path):
                walk(path)
            elif(os.path.isfile(path)):
                modifyTime = time.localtime(os.stat(path).st_mtime)
                if modifyTime.tm_year == 2020 and modifyTime.tm_mon == 12 and modifyTime.tm_mday == 23 and modifyTime.tm_hour >= 22:
                    print(path)
                    abc_txt.write(path)
                    abc_txt.write("\n")
                    abc_txt.flush()

walk("C:\\")

print("end")


