import scrapy
import os
import json
import re
import pandas as pd
import glob


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    info = []

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/List_of_computer_scientists',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def write_file(self,scientist,name):
        path = os.getcwd()
        try :
            to_write = json.dumps(scientist)
            if os.path.exists(path + "\\scientists"):
                pass
            else:
                os.mkdir(path + "\\scientists")
            f = open(path + "\\scientists\\"+name+".json","w+")
            f.write(to_write)
            f.close()
        except :
            pass

    async def parse_2(self,response):
        #metavlhth scientist
        scientist = {
            'name' : "",
            'awards' : 0,
            'education_text' : None,
        }
        #pairnw to viografiko ka8e scientist
        xp = '//*[@class=\"infobox biography vcard\"]'
        #prpei na parw ke text
        infobox = response.xpath(xp)
        #
        #8elw onoma
        #
        node = infobox.xpath('//*[@class=\"fn\"]')
        name = node.css('div::text').get()
        name2 = None
        try:
            name2 = name.split(' ')
            name2 = name2[len(name2)-1]
            name3 =''.join(list(map(str,map(ord,name2))))
            scientist['name'] = name3
        except:
            pass
        #print(name)
        #input('ftasame sto name')

        #
        #gia na parw info
        #
        i = 1
        while not(node.get()==None):
            #//*[@id="mw-content-text"]/div[1]/table/tbody/tr[4]
            xp = "//table/tbody/tr["+str(i)+"]"
            node = infobox.xpath(xp)
            #8elw alma mater
            header = node.css('th::text').get()
            if "wards" in str(header):
                #pairnw to table data tou row me to awards
                awards = node.css('td')
                #pairnw to ta links gia ta awards...? kane ke su ena search mhn leipei kati...
                for a in awards.css('a'):
                    scientist['awards']+=1
                    '''
                    auto gia na kaneis debugging
                    scientist["awards"].append[a.css('a::text').get()]
                    '''
            i+=1
        #end while
        #prepei na apo8hkeusw plhroforia
        yield self.write_file(scientist,name2)

    async def parse(self, response):
        #
        #/html/body/div[3]/div[3]/div[5]/div[1]/ul[1]
        #
        for i in range(1,25):
            xp = '//*[@id=\"mw-content-text\"]/div[1]/ul['+str(i)+']/li/a[contains(@href, "/wiki/")][1]'
            #exw parei to lis
            lis = response.xpath(xp)
            #pairnw to link apo ka8e li
            #input('prin mpei gia na parei apo ka8e li to link')
            for l in lis :
                link = l.css('a::attr(href)').get()
                if link is not None:
                    #print(link)
                    #print('*' * 30)
                    link = response.urljoin(link)
                    #paw se epomenh selida
                    yield scrapy.Request(link, callback=self.parse_2)
                    #print('*' * 30)
    
    
        # for scientist in scientists:
        #     with open(scientist) as doc:
        #         exp = json.load(doc)
        #         scientists_list.append(exp)
        # path_to_json = 'scientists/'
        # json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
        # print(json_files)  # for me this prints ['foo.json']
