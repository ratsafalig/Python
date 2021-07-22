import scrapy
import json

from scrapy.http import request

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    commonId = "27436"
    dataKey = "20210722165920any74357878"
    pluginId = "1"

    def start_requests(self):
        urls = [
            'https://www.uwa4d.com/api/report/pipeline/plugin?commonId=27436&dataKey=20210722165920any74357878&pluginId=1',
        ]
        
        yield scrapy.Request("https://www.uwa4d.com/api/m/signin", "POST", body={
            "account" : "18750016043",
            "auth_code" : "",
            "keep_login" : False,
            "password" : "00d045d080c5a0685994081f379d01d7",
            "redirect" : "https://www.uwa4d.com/u/overview.html",
            "type" : 1,
            "uwaLoginToken" : "",
        },
        callback=self.prt)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def prt(self, response):
        print(" >>>>> ----- <<<<< ")
        print("\n >>>>> " + response.body + " <<<<< \n")
        print(" >>>>> ----- <<<<< ")
        
    def parse(self, response):
        
        bodyAsJson = json.loads(body)
        for rule in bodyAsJson['rules']:
            body = scrapy.Request('https://www.uwa4d.com/api/report/pipeline/rule?' + 'commonId=' + self.commonId + '&dataKey=' + self.dataKey + '&sceneId=' + rule['sceneId'] + '&ruleId=' + rule['ruleId'])
            bodyAsJson = json.loads(body)
            f = open("./" + rule['name'] + ".csv", "rw+")
            f.write('名称,路径,长度\n')
            for d in bodyAsJson['data']:
                f.write(d['name'])
                f.write(d[','])
                f.write(d['dir'])
                f.write(d[','])
                f.write(d['length'])
                f.write('\n')
            f.close()
