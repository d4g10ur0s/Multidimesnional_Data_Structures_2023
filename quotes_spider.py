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

    def parse_2(self,response):
        #metavlhth scientist
        scientist = {
            'name' : '',
            'uni' : [],
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

        #gia na pairnoume to education
        i=1
        xp = "/html/body/div[3]/div[3]/div[5]/div[1]/h2[1]"

        node = response.xpath(xp)
        ps = node.xpath('//following-sibling::p')

        for p in ps:#pame se ka8e paragrafo
            input('aaa')
            print(str(p.get()))

        #8a grapsoume regex me lekseis oi opoies exoun sxesh me education

        '''
        while node != None :
            #pairnw to text
            input('Edw: ')
            header = node.css('span::text').get()
            print(str(header))
            if(re.search(".*[E|e]du.*",header)):
                print(str(header))

            i+=1
            '''
            #xp = "/html/body/div[3]/div[3]/div[5]/div[1]/h2["+str(i)+"]"
            #node = response.xpath(xp)


        #/html/body/div[3]/div[3]/div[5]/div[1]/h2[1]
        #text
        #regex --> an yparxei edu

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
