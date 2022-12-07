import scrapy
import os
import json


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

    def parse_2(self,response):
        #metavlhth scientist
        scientist = {
            'name' : '',
            'uni' : [],
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
        scientist['name'] = name
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
            almamater = ''
            header = node.css('th::text').get()
            if "mater" in str(header):
                #print("Alma mater")
                #pairnw to table data tou row me to alma mater
                almamater = node.css('td')
                #pairnw to text apo ta links gia ta panepisthmia
                for a in almamater.css('a'):
                    uni = a.css('a::text').get()
                #    print(uni)
                    scientist["uni"].append(uni)
            i+=1
        #end while
        i=0
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
