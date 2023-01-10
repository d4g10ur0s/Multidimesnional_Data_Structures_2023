import scrapy
import os
import json
import re


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    info = []

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/List_of_computer_scientists',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def write_file(self,scientist):
        path = os.getcwd()
        try :
            to_write = json.dumps(scientist)
            if os.path.exists(path + "\\scientists"):
                pass
            else:
                os.mkdir(path + "\\scientists")
            f = open(path + "\\scientists\\"+scientist['name']+".json","w+")
            f.write(to_write)
            f.close()
        except :
            pass

    async def parse_2(self,response):
        #metavlhth scientist
        scientist = {
            'name' : '',
            'uni' : [],
            'education_text' : None,
            'awards' : 0,
        }
        #pairnw to viografiko ka8e scientist
        xp = '//*[@class=\"infobox biography vcard\"]'
        #prpei na parw ke text
        infobox = response.xpath(xp)
        #8elw onoma
        node = infobox.xpath('//*[@class=\"fn\"]')
        name = node.css('div::text').get()
        scientist['name'] = name
        #input('ftasame sto name')
        #pame gia awards
        i=1
        tr = infobox.xpath("//tr["+str(i)+"]")
        while tr.get() != None :
            #print(str(tr.get()))
            if tr.css('th::text').get()!= None and "Awards" in tr.css('th::text').get():
                ul = tr[0].css('td div ul')
                print(len(ul))
                if len(ul) == 0:
                    print(tr.css('td').get())
                    input('a')
                    print(str(re.compile('[A,a]ward | [F,f]ellow | [M,m]ember | [M,m]edal')))
                    input('a')
                    scientist['awards'] = len(re.match(re.compile('[A,a]ward | [F,f]ellow | [M,m]ember | [M,m]edal'),tr.css('td').get()))-1
                else:
                    scientist['awards'] = len(ul.get().split("</li>"))-1

            i+=1
            tr = infobox.xpath("//tr["+str(i)+"]")
        #end while
        #prepei na apo8hkeusw plhroforia
        yield self.write_file(scientist)

    async def parse(self, response):
        #
        #/html/body/div[3]/div[3]/div[5]/div[1]/ul[1]
        #
        for i in range(1,25):
            xp = '//*[@id=\"mw-content-text\"]/div[1]/ul['+str(i)+']/li/a[contains(@href, "/wiki/")][1]'
            #exw parei to lis
            lis = response.xpath(xp)
            #pairnw to link apo ka8e li
            for l in lis :
                link = l.css('a::attr(href)').get()
                if link is not None:
                    link = response.urljoin(link)
                    #paw se epomenh selida
                    yield scrapy.Request(link, callback=self.parse_2)
